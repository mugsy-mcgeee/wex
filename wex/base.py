from wex import *


@source('PlayerResource')
class Player(Wex):
  name      = valueOf('m_iszPlayerNames')
  hero      = valueOf('m_hSelectedHero').asWex('Hero')
  hero_dt   = valueOf('m_hSelectedHero').asWex('Hero').var('hero_type')

  team = valueOf('m_iPlayerTeams') # 2: Radiant
                                   # 3: Dire
                                   # 5: Spectator

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

  state = valueOf('DT_DOTA_BaseNPC m_lifeState') # 0: Alive
                                                 # 1: Dying
                                                 # 2: Dead

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

  state = valueOf('DT_DOTAGamerules m_nGameState') # 1: Players loading
                                                   # 2: Pick/Ban in CM
                                                   # 4: Pre-game 
                                                   # 5: Game clock hist 0:00
                                                   # 6: End game (scoreboard)

  mode = valueOf('DT_DOTAGamerules m_iGameMode') # 1: All pick
                                                 # 2: Captain's Mode
                                                 # 3: Random draft
                                                 # 4: Single draft
                                                 # 5: All random
                                                 # 8: Reverse captain's mode

  first_pick = valueOf('DT_DOTAGamerules m_iStartingTeam') # 0: Not CM game
                                                           # 2: Radiant first 
                                                           # 3: Dire first 

  active_pick = valueOf('DT_DOTAGamerules m_ActiveTeam') # 2: Radiant
                                                         # 3: Dire

  winner = valueOf('DT_DOTAGamerules m_nGameWinner') # 5: No winner
                                                     # 2: Radiant
                                                     # 3: Dire


@source('Team')
class Team(Wex):
  side = valueOf('DT_Team m_iTeamNum') # 2: Radiant
                                       # 3: Dire
  name    = valueOf('DT_Team m_szTeamname')
  tag     = valueOf('DT_DOTATeam m_szTag')
  team_id = valueOf('DT_DOTATeam m_unTournamentTeamID')
  kills   = valueOf('DT_DOTATeam m_iHeroKills')

