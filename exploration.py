from colours import Colours
from objects import PlayerInventory, all_items, display_equipment_stats
from entities import new_player, all_enemies
from setting import all_artifacts
from system import System, clear, sleep_and_clear
import random as rdm



class Combat:

  @staticmethod
  def choose_enemy(enemy_chosen=None):
    if enemy_chosen == None:
      rdm_int = rdm.randint(1, 200)

      #filters
      enemies_filtered_by_location = list(filter(lambda x: new_player.current_location in all_enemies[x].spawn_location, all_enemies))

      specific_enemy = list(filter(lambda x: rdm_int in all_enemies[x].spawn_range, enemies_filtered_by_location))

      
      if len(specific_enemy) > 1:
        artifact_needed = list(filter(lambda x: x.location is new_player.current_location, all_artifacts))

        if artifact_needed[0] in new_player.artifacts_collected:
          specific_enemy.pop()
        else:
          specific_enemy.pop(0)

      enemy_chosen = specific_enemy[0]


    new_player.current_enemy = all_enemies[enemy_chosen]

    clear()
    print(f"{Colours.fg.cyan}You encountered {new_player.current_enemy.name_string}{Colours.fg.cyan}.")   
    sleep_and_clear(1)


  @staticmethod
  def set_effects():
    new_player.current_enemy.current_health = new_player.current_enemy.max_health


  @staticmethod
  def reset_item_effects(item_name):
    item = System.get_object(item_name, all_items)

    new_player.apply_item_effects("Decrease", item.increases)
    new_player.current_enemy.apply_item_effects("Increase", item.decreases)


  @classmethod
  def update_items_used(cls):
    for item_name in new_player.items_used:
      turns_left = new_player.items_used[item_name]

      if turns_left > 0:
        if turns_left == 1:
          clear()
          print(f"{System.get_object(item_name, all_items).name_string}{Colours.fg.orange}'s effects ran out.")
          sleep_and_clear(1.5)

          cls.reset_item_effects(item_name)

        new_player.items_used[item_name] -= 1


  @classmethod
  def reset_combat(cls):
    for item_name in new_player.items_used:
      turns_left = new_player.items_used[item_name]

      new_player.items_used[item_name] = 0
      if turns_left > 0:
        cls.reset_item_effects(item_name)

      #No need to reset enemy health because we are already setting it in cls.set_effects()

  
  @staticmethod
  def display_items_used():
    filtered_items = list(filter(lambda item: new_player.items_used[item] > 0, new_player.items_used))
    
    if len(filtered_items) > 0:
      print(f"{Colours.fg.lightgreen + Colours.underline}Current Item Effects:{Colours.reset}")
    
    for index, filtered_item in enumerate(filtered_items):
      # use line 76 for getting in items!!!!!!!!!!!! 
      item_used = list(filter(lambda item: item.name == filtered_item, all_items.values()))
      item_number = index + 1
      turns_left = new_player.items_used[filtered_item]
      
      print(f"{Colours.tag(item_number)} {item_used[0].name_string}{Colours.equipment_colour}: {Colours.fg.red}({turns_left} turns left)")
      
      display_equipment_stats(item_used[0], display_price=False, display_name=False, extra_text=item_number)


  @classmethod
  def display_user_interface(cls):
    clear()
    print(f"""
{new_player.current_enemy.name_string + Colours.fg.red}'s Health:{Colours.fg.green} {new_player.current_enemy.current_health}{Colours.fg.red} / {Colours.fg.green}{new_player.current_enemy.max_health}

{Colours.fg.lightgreen + Colours.underline}Your Health:{Colours.reset}{Colours.fg.green} {new_player.current_health}{Colours.fg.red} / {Colours.fg.green}{new_player.max_health}

{Colours.fg.orange}
What Would You Like To Do?
{Colours.tag('a') + Colours.description_colour} Attack {new_player.current_enemy.name_string}
{Colours.tag('u') + Colours.description_colour} Use Item
{Colours.tag('e') + Colours.description_colour} Escape From Combat{Colours.fg.orange}


""")
    cls.display_items_used()


  @classmethod
  def start_combat(cls, enemy=None, is_players_turn=None):
    #Choose enemy
    if enemy == None:
      cls.choose_enemy()
    else:
      cls.choose_enemy(enemy)

    #Initialize combat effects
    cls.set_effects()

    #Choose first turn
    if is_players_turn == None:
      cls.is_players_turn = new_player.armour.is_lighter_than(new_player.current_enemy.armour)
    else:
      cls.is_players_turn = is_players_turn

    while new_player.current_health > 0 and new_player.current_enemy.current_health > 0:
      clear()
      cls.update_items_used()

      #Player's turn
      if cls.is_players_turn:
        player_choice = ''
        valid_inputs = ('a', 'u', 'e')

        while player_choice not in valid_inputs:
          cls.display_user_interface()

          player_choice = input(f"{Colours.input_colour}> ").lower().strip()

        cls.is_players_turn = False

        #Player attacking
        if player_choice == 'a':
          new_player.attack()

        #Player using items
        elif player_choice == 'u':
          wants_to_use_item = PlayerInventory.use_item()
          cls.is_players_turn = wants_to_use_item == False

        #Player escaping from combat
        elif player_choice == 'e':
          new_player.escape_from_combat()

          if new_player.has_escaped:
            break 
          elif not new_player.has_escaped:
            new_player.current_enemy.attack()


      #Enemy's turn
      if not cls.is_players_turn:
        cls.is_players_turn = True
        #Currently, enemies can only attack
        new_player.current_enemy.attack()


    new_player.get_tired()
    cls.reset_combat()
    
    if new_player.current_enemy.is_dead():
      new_player.current_enemy.drop_loot()



class Encounters:
  pass
  