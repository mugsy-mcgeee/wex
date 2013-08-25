import imp
import os.path
import inspect
from glob import glob

from skadi.engine.world import from_ehandle

DEBUG = False

OFFSET_BASED = ['DT_DOTA_PlayerResource']
OFFSET_ARRAY_SIZE = 32


class PropertyNotFound(Exception):
  pass
class WexNotFound(Exception):
  pass


def dprint(msg):
  if DEBUG:
    print msg

PT_UNKNOWN=-1
PT_HANDLE=0
PT_BOOTEAN=1
PT_NUMBER=2
def prop_type(prop_str):
  if len(prop_str.split()) == 2:
    prop_str = prop_str.split()[1]
  if prop_str.startswith('m_h'):
    return PT_HANDLE
  elif prop_str.startswith('m_b'):
    return PT_BOOLEAN
  elif prop_str.startswith('m_n') or prop_str.startswit('m_i') or prop_str.startswith('m_f'):
    return PT_NUMBER
  else:
    return PT_UNKNOWN


def wex_files():
  wex_dir = os.path.dirname(os.path.abspath(__file__))
  return [f for f in glob(os.path.join(wex_dir, '*.py')) if not f.endswith('__init__.py')]


def load_wex():
  wex_pkgs = []

  print 'Loading wex files'
  for filename in wex_files():
    mod_name = 'wex.{}'.format(os.path.basename(filename)[:-3])
    mod = imp.load_source(mod_name, filename)
    for name,cls in inspect.getmembers(mod, inspect.isclass):
      # Lists all classes in module namespace, we are only looking for
      # the classes declared IN this module
      if cls.__module__ == mod_name:
        print '\t{} -> {}'.format(mod_name, cls.__name__)
        wex_pkgs.append(cls()) # instantiate class
  return wex_pkgs


class WexSnapshot(object):
  def __init__(self, wex_pkgs):
    self.wex_pkgs = wex_pkgs
    self.raw = None

  def get_wex_inst(self, cls):
    cls_str = '{}.{}'.format(cls.__module__, cls.__name__)
  
    for wex in self.wex_pkgs:
      wex_str = '{}.{}'.format(wex.__class__.__module__, wex.__class__.__name__)
      if wex_str == cls_str:
        return wex
    print '{} not found in wex_pkgs:\n'.format(cls_name)
    print 'wex_pkgs={}'.format(wex_pkgs)
    return None
  
  def find_wex_class(self, cls_name):
    for wex in self.wex_pkgs:
      if wex.__class__.__name__ == cls_name:
        return wex
    return None


def stream(demo, tick=0):
  wex_pkgs = load_wex()

  for data in demo.stream(tick=tick):
    world = data[2]

    snap = WexSnapshot(wex_pkgs)
    snap.raw = data
    snap._world = world
    for wex in wex_pkgs:
      # pass world state to wex classes
      wex._world = world
      wex._snap = snap

      # add wex classes to WexSnapshot obj
      snap.__dict__[wex.__class__.__name__] = wex
    yield snap


class Enum(object):
  def __init__(self, key, val):
    self.key = key
    self.val = val

  def __eq__(self, other):
    if isinstance(other, Enum):
      return self.key == other.key and self.val == other.val
    elif isinstance(other, self.val.__class__):
      return self.val == other
    else:
      raise Exception('Invalid comparison type {} == {}'.format(self, other))

  def __ne__(self, other):
    return not self.__eq__(other)

  def __str__(self):
    return '<{}:{}>'.format(self.key, self.val)


class AsWex(object):
  def __init__(self, wex_cls_str, chain=None):
    self.wex_cls_str = wex_cls_str
    self.chain = chain or []
    dprint('{}AsWex({}, chain={})'.format('\t'*len(self.chain), wex_cls_str, chain))

  def valueOf(self, prop_str):
    o_chain = self.chain
    o_chain.append(self)
    self.chain = []
    return valueOf(prop_str, o_chain)

  def var(self, var_name):
    o_chain = self.chain
    o_chain.append(self)
    self.chain = []
    return valueOf(var_name, o_chain, True)

  def __call__(self, ctx, snap):
    dprint('AsWex.call({}, ctx={}, chain={})'.format(self.wex_cls_str, ctx, self.chain))
    for _func in self.chain:
      ctx = _func(ctx, snap)
    prop_val = ctx

    other_wex = snap.find_wex_class(self.wex_cls_str)
    if other_wex is not None:
      index,serial = from_ehandle(prop_val)
      if index == 2047: # undefined object
        return None
      else:
        if len(other_wex._obj_list) == 0:
          other_wex.all() # call this to create objs if needed
        return other_wex._obj_list[prop_val]
    else:
      obj_name = wex_obj.__class__.__name__
      msg = '{} not found as referenced in {}'.format(wex_cls_str, obj_name)
      raise WexNotFound(msg)


class valueOf(object):
  def __init__(self, prop_str, chain=None, var_access=False):
    self.chain = chain or []
    dprint('{}valueOf({}, chain={})'.format('\t'*len(self.chain), prop_str, chain))
    self.var_access = var_access
    self.merge_func = None
    self._rhs = None
    self._enum_dict = None

    if len(prop_str.split()) == 2:
      self.prop_key = tuple(prop_str.split())
      if self.prop_key[1].startswith('m_h'):
        self.is_handle = True
      else:
        self.is_handle = False
    else:
      self.prop_key = prop_str
      if self.prop_key.startswith('m_h'):
        self.is_handle = True
      else:
        self.is_handle = False

  def __add__(self, other):
    if not isinstance(other, valueOf):
      raise Exception('Unsupported type ({}) for + operator'.format(other.__class__))
    dprint('__add__({}, {})'.format(self, other))
    self._rhs = other
    self.merge_func = lambda l_val,r_val:l_val+r_val
    return  self

  def asWex(self, wex_cls_str):
    o_chain = self.chain
    o_chain.append(self)
    self.chain = []
    return AsWex(wex_cls_str, o_chain)

  def asEnum(self, enum_dict):
    """ Since this is called during definition time not eval time
        we don't have access to the variable we are being assigned
        to or the object we reside in. Because of this we must
        enqueue the enum creation step until after the class has
        been instantiated. Since the Enum values could be accessed
        before any Wex variables are evaluated we should do the
        enqued operations the first call to __getattribute__. """
    self._enum_dict = enum_dict
    return self
      

  def __call__(self, ctx, snap):
    dprint('valueOf.call({}, ctx={}, chain={})'.format(self.prop_key, ctx, self.chain))
    for _func in self.chain:
      ctx = _func(ctx, snap)
    wex_obj = ctx

    result = None
    if self.var_access:
      result = getattr(wex_obj, self.prop_key)
    else:
      if wex_obj._offset_based:
        try:
          ehandle, offset = wex_obj.id
        except:
          raise Exception('Expected id tuple(ehandle,offset), not {}'.format(wex_obj.id))
        # offset based instances
        data_set = snap._world.by_ehandle[ehandle]
        key = (self.prop_key, str(offset).zfill(4))
        result = data_set[key]
      else: 
        # object based instances
        prop_val = snap._world.by_ehandle[wex_obj.id][self.prop_key]
        result = prop_val

    # Handle any merging due to operator overloads (__add__, etc)
    if self._rhs is not None:
      r_val = self._rhs(ctx, snap)
      result = self.merge_func(result, self._rhs(ctx, snap))
    # Handle returning Enum if we are asEnum
    if self._enum_dict is not None and result in self._enum_dict:
      result = Enum(self._enum_dict[result], result)
    return result

class var(valueOf):
  def __init__(self, prop_str, chain=None, var_access=True):
    super(var, self).__init__(prop_str, chain, var_access)


class myDatatype(object):
  def __call__(self, wex_obj, snap):
    if wex_obj._offset_based:
      try:
        ehandle, offset = wex_obj.id
      except:
        raise Exception('Expected id tuple(ehandle,offset), not {}'.format(wex_obj.id))
      return snap._world.fetch_recv_table(ehandle).dt
    else:
      return snap._world.fetch_recv_table(wex_obj.id).dt


class source(object):
  """ @source decorator """
  def __init__(self, type_str):
    self.type_str = type_str

  def __call__(self, cls):
    setattr(cls, 'src_table', self.type_str)
    return cls


class Wex(object):
  def __init__(self, ehandle=None, offset_based=False):
    # META
    self._obj_list = {}
    self._snap = None
    self._offset_based = offset_based

    # INSTANCE
    self.id = ehandle
    self._props = {}
    for member in inspect.getmembers(self):
      name,func = member
      if isinstance(func, AsWex) or \
         isinstance(func, valueOf) or \
         isinstance(func, myDatatype):
        self._props[name] = func
        
    self._initialize_enums()

  # META
  def _initialize_enums(self):
    cls = self.__class__
    for name,prop in self._props.iteritems():
      if hasattr(prop, '_enum_dict') and prop._enum_dict is not None:
        for v,k in prop._enum_dict.iteritems():
          if k not in cls.__dict__:
            setattr(cls, k, Enum(k,v))
          elif cls.__dict__[k] != Enum(k,v):
            msg = 'Conflicting Enum values declared for {}.{} ({}/{})'.format(cls, k, cls.__dict__[k], Enum(k,v))
            raise Exception(msg)

  # META
  def _find_my_entities(self):
    ents = []

    # If entity_str is shortname, perform prefix search
    if not self.src_table.startswith('DT_'):
      # try DT_DOTA_ 
      search_str = 'DT_DOTA_{}'.format(self.src_table)
      self._offset_based = search_str in OFFSET_BASED
      ents = self._snap._world.find_all_by_dt(search_str).keys()
      if len(ents) == 0: 
        # try DT_DOTA 
        search_str = 'DT_DOTA{}'.format(self.src_table)
        self._offset_based = search_str in OFFSET_BASED
        ents = self._snap._world.find_all_by_dt(search_str).keys()
        if len(ents) == 0: 
          # try DT_ 
          search_str = 'DT_{}'.format(self.src_table)
          self._offset_based = search_str in OFFSET_BASED
          ents = self._snap._world.find_all_by_dt(search_str).keys()
    else:
      ents = self._snap._world.find_all_by_dt(self.src_table).keys()
      self._offset_based = self.src_table in OFFSET_BASED
    return ents

  # META
  def all(self):
    # find the instance of our own class in wex_pkgs
    obj = self._snap.get_wex_inst(self.__class__)

    ents = obj._find_my_entities()
    for ehandle in ents:
      if obj._offset_based:
        for offset in range(OFFSET_ARRAY_SIZE):
          key = '{}_{}'.format(ehandle, offset)
          if key not in obj._obj_list:
            obj._obj_list[key] = obj.__class__((ehandle,offset), obj._offset_based)
            obj._obj_list[key]._snap = obj._snap
      else:
        if ehandle not in obj._obj_list:
          obj._obj_list[ehandle] = obj.__class__(ehandle, obj._offset_based)
          obj._obj_list[ehandle]._snap = obj._snap

    return obj._obj_list.values()

  # INSTANCE
  def __getattribute__(self, name):
    _props = object.__getattribute__(self, '_props')

    if name in _props:
      func = _props[name]
      return func(self, object.__getattribute__(self, '_snap'))
    else:
      return object.__getattribute__(self, name)
