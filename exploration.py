from colours import Colours
from items import PlayerInventory
from objects import Player, all_enemies
from setting import all_locations, all_artifacts
from system import clear, sleep, sleep_and_clear
import random as rdm



class Combat:
  @staticmethod
  def choose_enemy(enemy_chosen=None):
    if enemy_chosen == None:
      rdm_int = rdm.randint(1, 200)

      #filters
      enemies_filtered_by_location = list(filter(lambda x: Player.current_location in all_enemies[x].spawn_location, all_enemies))

      specific_enemy = list(filter(lambda x: rdm_int in all_enemies[x].spawn_range, enemies_filtered_by_location))

      
      if len(specific_enemy) > 1:
        artifact_needed = list(filter(lambda x: x.location is Player.current_location, all_artifacts))

        if artifact_needed[0] in Player.artifacts_collected:
          specific_enemy.pop()
        else:
          specific_enemy.pop(0)

      enemy_chosen = specific_enemy[0]


    Player.current_enemy = all_enemies[enemy_chosen]


    clear()
    

    print(f"{Colours.fg.cyan}You encountered {Player.current_enemy.name_string}{Colours.fg.cyan}.")   
    sleep_and_clear(1)


  @staticmethod
  def set_effects():
    Player.current_enemy.current_health = Player.current_enemy.max_health


  @staticmethod
  def reset_effects():
    Player.current_enemy.current_health = Player.current_enemy.max_health


  @classmethod
  def start(cls, enemy=None, is_players_turn=None):
    description_colour = Colours.fg.lightblue

    #Choose enemy
    if enemy == None:
      cls.choose_enemy()
    else:
      cls.choose_enemy(enemy)

    #Initialize combat effects
    cls.set_effects()

    #Choose first turn
    if is_players_turn == None:
      cls.is_players_turn = Player.armour.is_lighter_than(Player.current_enemy.armour)
    else:
      cls.is_players_turn = is_players_turn

    while Player.current_health > 0 and Player.current_enemy.current_health > 0:
      clear()

      if cls.is_players_turn:
        player_choice = ''
        valid_inputs = ('a', 'u', 'e')

        while player_choice not in valid_inputs:
          clear()
          player_choice = input(f"""
{Player.current_enemy.name_string + Colours.fg.red}'s Health:{Colours.fg.green} {Player.current_enemy.current_health}{Colours.fg.red} / {Colours.fg.green}{Player.current_enemy.max_health}

{Colours.fg.lightgreen + Colours.underline}Your Health:{Colours.reset}{Colours.fg.green} {Player.current_health}{Colours.fg.red} / {Colours.fg.green}{Player.max_health}

{Colours.fg.orange}
What Would You Like To Do?
{Colours.tag('a') + description_colour} Attack {Player.current_enemy.name_string}
{Colours.tag('u') + description_colour} Use Item
{Colours.tag('e') + description_colour} Escape From Combat{Colours.fg.orange}


> """).lower().strip()

        cls.is_players_turn = False

        if player_choice == 'a':
          Player.attack()
          continue

        elif player_choice == 'u':
          wants_to_use_item = PlayerInventory.use_item()
          cls.is_players_turn = wants_to_use_item != True

        elif player_choice == 'e':
          Player.escape_from_combat()

          if Player.has_escaped:
            break 
          elif not Player.has_escaped:
            Player.current_enemy.attack()
            continue


      if not cls.is_players_turn:
        cls.is_players_turn = True
        Player.current_enemy.attack()


    Player.get_tired()
    
    if Player.current_enemy.is_dead():
      Player.current_enemy.drop_loot()

    cls.reset_effects()



class Encounters:
  pass
  