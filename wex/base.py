from wex import *


@source('PlayerResource')
class Player(Wex):
  name      = valueOf('m_iszPlayerNames')
  hero      = valueOf('m_hSelectedHero').asWex('Hero')
  hero_dt   = valueOf('m_hSelectedHero').asWex('Hero').var('hero_type')

  team = valueOf('m_iPlayerTeams').asEnum({2: 'RADIANT',
                                           3: 'DIRE',
                                           5: 'SPECTATOR'})

  conn_state = valueOf('m_iConnectionState')
  steam_id   = valueOf('m_iPlayerSteamIDs')

  randomed = valueOf('m_bHasRandomed')
  repicked = valueOf('m_bHasRepicked')
  banned   = valueOf('m_bVoiceChatBanned')

  bb_cooldown = valueOf('m_flBuybackCooldownTime')

  level     = valueOf('m_hSelectedHero').asWex('Hero').var('level')
  cur_xp    = valueOf('m_hSelectedHero').asWex('Hero').var('cur_xp')

  cur_life   = valueOf('m_hSelectedHero').asWex('Hero').var('cur_life')
  max_life   = valueOf('m_hSelectedHero').asWex('Hero').var('max_life')
  cur_mana   = valueOf('m_hSelectedHero').asWex('Hero').var('cur_mana')
  max_mana   = valueOf('m_hSelectedHero').asWex('Hero').var('max_mana')
  life_regen = valueOf('m_hSelectedHero').asWex('Hero').var('life_regen')
  mana_regen = valueOf('m_hSelectedHero').asWex('Hero').var('mana_regen')

  kills   = valueOf('m_iKills')
  deaths  = valueOf('m_iDeaths')
  assists = valueOf('m_iAssists')

  lasthits = valueOf('m_iLastHitCount')
  denies   = valueOf('m_iDenyCount')

  gold     = var('r_gold') + var('u_gold')
  r_gold   = valueOf('m_iReliableGold')
  u_gold   = valueOf('m_iUnreliableGold')
  net_gold = valueOf('m_iTotalEarnedGold')



@source('Unit_Hero_*')
class Hero(Wex):
  hero_type = myDatatype()

  state = valueOf('DT_DOTA_BaseNPC m_lifeState').asEnum({0: 'ALIVE',
                                                         1: 'DYING',
                                                         2: 'DEAD'})

  cur_xp = valueOf('DT_DOTA_BaseNPC_Hero m_iCurrentXP')
  level  = valueOf('DT_DOTA_BaseNPC m_iCurrentLevel')

  cur_life = valueOf('DT_DOTA_BaseNPC m_iHealth')
  max_life = valueOf('DT_DOTA_BaseNPC m_iMaxHealth')
  cur_mana = valueOf('DT_DOTA_BaseNPC m_flMana')
  max_mana = valueOf('DT_DOTA_BaseNPC m_flMaxMana')
  life_regen = valueOf('DT_DOTA_BaseNPC m_flHealthThinkRegen')
  mana_regen = valueOf('DT_DOTA_BaseNPC m_flManaThinkRegen')


@source('GamerulesProxy')
class GameRules(Wex):
  match_id = valueOf('DT_DOTAGamerules m_unMatchID')

  time       = valueOf('DT_DOTAGamerules m_fGameTime')
  load_time  = valueOf('DT_DOTAGamerules m_flGameLoadTime')
  start_time = valueOf('DT_DOTAGamerules m_flGameStartTime')
  end_time   = valueOf('DT_DOTAGamerules m_flGameEndTime')

  state = valueOf('DT_DOTAGamerules m_nGameState').asEnum({1: 'LOADING',
                                                           2: 'CM_PICK',
                                                           4: 'PRE_GAME',
                                                           5: 'STARTED',   # After 0:00
                                                           6: 'END_GAME'}) # scoreboard

  mode = valueOf('DT_DOTAGamerules m_iGameMode').asEnum({1: 'MODE_ALL',
                                                         2: 'MODE_CM',
                                                         3: 'MODE_RANDOM',
                                                         4: 'MODE_DRAFT',
                                                         5: 'MODE_ALL_RANDOM',
                                                         8: 'MODE_REVERSE_CM'})

  first_pick = valueOf('DT_DOTAGamerules m_iStartingTeam').asEnum({0: 'NOT_CM',
                                                                   2: 'RADIANT',
                                                                   3: 'DIRE'})

  active_pick = valueOf('DT_DOTAGamerules m_ActiveTeam').asEnum({2: 'RADIANT',
                                                                 3: 'DIRE'})

  winner = valueOf('DT_DOTAGamerules m_nGameWinner').asEnum({5: 'NO_WINNER',
                                                             2: 'RADIANT',
                                                             3: 'DIRE'})


@source('Team')
class Team(Wex):
  side = valueOf('DT_Team m_iTeamNum').asEnum({2: 'RADIANT',
                                               3: 'DIRE'})
  name    = valueOf('DT_Team m_szTeamname')
  tag     = valueOf('DT_DOTATeam m_szTag')
  team_id = valueOf('DT_DOTATeam m_unTournamentTeamID')
  kills   = valueOf('DT_DOTATeam m_iHeroKills')

