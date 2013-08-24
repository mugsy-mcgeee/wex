from wex import *


@source('PlayerResource')
class Player(Wex):
  name      = valueOf('m_iszPlayerNames')
  hero      = valueOf('m_hSelectedHero').asWex('Hero')
  hero_dt   = valueOf('m_hSelectedHero').asWex('Hero').var('hero_type')
  level     = valueOf('m_iLevel')
  metalevel = valueOf('m_iMetaLevel')

  conn_state = valueOf('m_iConnectionState')
  steam_id   = valueOf('m_iPlayerSteamIDs')

  randomed = valueOf('m_bHasRandomed')
  repicked = valueOf('m_bHasRepicked')
  banned   = valueOf('m_bVoiceChatBanned')

  bb_cooldown = valueOf('m_flBuybackCooldownTime')

  cur_mana   = valueOf('m_hSelectedHero').asWex('Hero').var('cur_mana')
  max_mana   = valueOf('m_hSelectedHero').asWex('Hero').var('max_mana')
  mana_regen = valueOf('m_hSelectedHero').asWex('Hero').var('mana_regen')

  kills   = valueOf('m_iKills')
  deaths  = valueOf('m_iDeaths')
  assists = valueOf('m_iAssists')

  lasthits = valueOf('m_iLastHitCount')
  denies   = valueOf('m_iDenyCount')

  r_gold   = valueOf('m_iReliableGold')
  u_gold   = valueOf('m_iUnreliableGold')
  tot_gold = valueOf('m_iTotalEarnedGold')



@source('Unit_Hero_*')
class Hero(Wex):
  hero_type = myDatatype()

  state = valueOf('DT_DOTA_BaseNPC m_lifeState')

  max_health = valueOf('DT_DOTA_BaseNPC m_iHealth')

  cur_mana = valueOf('DT_DOTA_BaseNPC m_flMana')
  max_mana = valueOf('DT_DOTA_BaseNPC m_flMaxMana')
  mana_regen = valueOf('DT_DOTA_BaseNPC m_flManaThinkRegen')
