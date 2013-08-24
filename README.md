What is Wex?
============

Wex is a library for using [Skadi](https://github.com/onethirtyfive/skadi)
which is a [DOTA2](http://www.dota2.com) replay parser.

Wex is an SDL used to define a python object model from raw parser data.


What does that mean?
====================

[Skadi](https://github.com/onethirtyfive/skadi) provides access to all of
the raw parsed data of a DOTA2 replay. For example, if you want to
list the current life regen rates heroes in a particular replay you could 
do the following using Skadi: 

```python
# Skip Skadi initialization code

for tick, string_tables, world in demo.stream(tick=10000):

  # world contains information about all the entities:
  for ehandle, state in world.find_all_by_dt('DT_DOTA_Unit_Hero*').iteritems():
    print state[(u'DT_DOTA_BaseNPC', u'm_flHealthThinkRegen')]
  break
```

And the output would look something like:

```
1.00122100122
1.53846153846
0.732600732601
1.26984126984
1.26984126984
8.79120879121
0.732600732601
2.61294261294
7.98534798535
1.00122100122
```

Wex was created in order to be a layer of abstraction on top of this
raw acces by providing the ability to declare a python object model.
Using Wex you could retrieve the same information as above and it
would look like this:

```python
# Skip Skadi initialization code

for snap in wex.stream(replay, tick=10000):
  for hero in snap.Hero.all():
    print hero.life_regen
  break
```


How do I use Wex?
=================

Wex is a python package that contains a number of object definitions 
(individually called a wex). Each of these wexes describes a mapping of
raw Skadi data to python class structure. In order to use Wex I will
assume you already have some code that is set up to use Skadi. All
you need is to include the Wex package into your python path and
import the wex package. After that you just use the Wex stream iterator
wrapper to wrap the Skadi iterator and you're good to go. It looks
something like this:

```python
# Skadi initialization stuff

import wex

for snap in wex.stream(replay, tick=10000):
  for hero in snap.Hero.all():
    print hero.hero_type
```


Can I still access the raw data?
================================

Yes! The Wex stream wrapper also provides direct access to the underlying
raw Skadi data as returned by the stream in the variable 'raw'.

```python
for snap in wex.stream(replay, tick=10000):

  # access raw Skadi data from the 'raw' var
  for ehandle, state in snap.raw.world.find_all_by_dt('DT_DOTA_Unit_Hero*').iteritems():
    print state[(u'DT_DOTA_BaseNPC', u'm_flHealthThinkRegen')]
```


How do I know what Wex objects look like?
=========================================

Wex automatically loads wex definitions from the wex package directory.
In order to see what these wex definitions look like just browse to
that directory. You can see the base definitions in 
[base.py](https://github.com/skadistats/wex/blob/master/wex/base.py).
You can access any of the wexes for a given game state by using the format:

```
<wexsnapshot>.<Wex>.all()

# for example
snap.Hero.all()
snap.Player.all()
```


How do I make my own Wex?
=========================

Wex was written with the idea that we don't know exactly how you want
your object model to look but here are some convenient implementations.
This means that it was written to be as simple as possible for users
to create a wex that looks like whatever they need for their particular
use-case. Here are the steps to create your own wex.

All wexes are loaded at runtime from the wex package directory. Simply
create a new file under wex named <newfile>.py since it has to be a
valid python file.

The first line of your file will be

```python
from wex import *
```

and then you can start your wex definition. A wex definition is a
python class declaration that extends from the base Wex object with
a special decorator that describes what the source DataType is for
the class. It looks like this

```python
@source('PlayerResource')
class Player(Wex):
  pass
```

Now if you're familiar with the DOTA2 replay datatypes you may notice
that there is no datatype called PlayerResource. However there is
one called DT_DOTA_PlayerResource. Since every DOTA2 datatype is
prefixed with either DT_ or DT_DOTA you can leave it off and Wex
will fill it in as necessary.

The next step is to define the attributes that your class will have.
Simply declare them as class-level variables and assign them values
using the special Wex keywords.

```python
@source('PlayerResource')
class Player(Wex):
  name = valueOf('m_iszPlayerNames')
```

The string 'm_iszPlayerNames' is the key in the underlying datatype
that you want to assign to the variable. See the excellent Skadi
[documentation](https://github.com/onethirtyfive/skadi/wiki) for a
description of the keys that each datatype contains. 


Wex Keywords
============

```
valueOf( <DataType key> )
Returns raw value that is contained in that key

asWex( <Wex class> )
Assumes that the previous value refers to an eHandle and attempts
to find and return the Wex instance of that class that is pointed 
to by that eHandle. The eHandle must point to the correct type of
DataType for this to work.

var( <variable name> )
This allows you to map the value of other wexes to a variable in
your current definition. An example of this might be that you want
to map the Hero's current life and mana to life and mana variables
in the Player class.
```

See [base.py](https://github.com/skadistats/wex/blob/master/wex/base.py)
for examples of how the keyword syntex works.


Help?
=====

Wex is still a work in progress and new functionality is still
being added. If you have any questions about how to use it or run
into any problems ask mugsy in #dota2replay / quakenet.
