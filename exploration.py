from colours import Colours
import game
import objects
import entities
from setting import all_artifacts, grimsden
from system import System, clear, sleep_and_clear
import random



class Combat:
  @staticmethod
  def choose_enemy(enemy_chosen):
    if enemy_chosen == None:
      rdm_int = random.randint(1, 200)

      #filters
      enemies_filtered_by_location = list(filter(lambda x: entities.new_player.current_location in entities.all_enemies[x].spawn_location, entities.all_enemies))

      specific_enemy = list(filter(lambda x: rdm_int in entities.all_enemies[x].spawn_range, enemies_filtered_by_location))
  
      
      if len(specific_enemy) > 1:
        artifact_needed = list(filter(lambda x: x.location is entities.new_player.current_location, all_artifacts))[0]

        if artifact_needed in entities.new_player.artifacts_collected:
          specific_enemy.pop()
        else:
          specific_enemy.pop(0)

      enemy_chosen = specific_enemy[0]

    
    try:  
      entities.new_player.current_enemy = entities.all_enemies[enemy_chosen]
    except KeyError:
      entities.new_player.current_enemy = enemy_chosen


    clear()
    print(f"{Colours.fg.cyan}You encountered {entities.new_player.current_enemy.name_string}{Colours.fg.cyan}.")
    sleep_and_clear(1)


  @staticmethod
  def set_effects():
    entities.new_player.current_enemy.current_health = entities.new_player.current_enemy.max_health


  @staticmethod
  def reset_item_effects(item_name):
    item = System.get_object(item_name, objects.all_items)

    entities.new_player.apply_item_effects("Decrease", item.increases)
    entities.new_player.current_enemy.apply_item_effects("Increase", item.decreases)


  @classmethod
  def update_items_used(cls):
    for item_name in entities.new_player.items_used:
      turns_left = entities.new_player.items_used[item_name]

      if turns_left > 0:
        if turns_left == 1:
          clear()
          print(f"{System.get_object(item_name, objects.all_items).name_string}{Colours.fg.orange}'s effects ran out.")
          sleep_and_clear(1.5)

          cls.reset_item_effects(item_name)

        entities.new_player.items_used[item_name] -= 1


  @classmethod
  def reset_combat(cls):
    #Resetting item effects
    for item_name in entities.new_player.items_used:
      turns_left = entities.new_player.items_used[item_name]

      entities.new_player.items_used[item_name] = 0
      if turns_left > 0:
        cls.reset_item_effects(item_name)

    #Resetting enemy + turn + choice
    if not entities.new_player.current_enemy is entities.talgrog_the_giant:
      entities.new_player.current_enemy = entities.TemporaryEnemy
    
    else:
      entities.new_player.has_won = True
      
    entities.new_player.has_combat_turn = None
    entities.new_player.combat_choice = None

    #No need to reset enemy health because we are already setting it in cls.set_effects()

  
  @staticmethod
  def display_items_used():
    filtered_items = list(filter(lambda item: entities.new_player.items_used[item] > 0, entities.new_player.items_used))
    
    if len(filtered_items) > 0:
      print(f"{Colours.fg.lightgreen + Colours.underline}Current Item Effects:{Colours.reset}")
    
    for index, filtered_item in enumerate(filtered_items):
      item_used = System.get_object(filtered_item, objects.all_items)
      item_number = index + 1
      turns_left = entities.new_player.items_used[filtered_item]
      
      print(f"{Colours.tag(item_number)} {item_used.name_string}{Colours.equipment_colour}: {Colours.fg.red}({turns_left} turns left)")
      
      objects.display_equipment_stats(item_used, display_price=False, display_name=False, extra_text=item_number)


  @classmethod
  def display_user_interface(cls):
    clear()
    print(f"""
{entities.new_player.current_enemy.name_string + Colours.fg.red}'s Health:{Colours.fg.green} {entities.new_player.current_enemy.current_health}{Colours.fg.red} / {Colours.fg.green}{entities.new_player.current_enemy.max_health}

{Colours.fg.lightgreen + Colours.underline}Your Health:{Colours.reset}{Colours.fg.green} {entities.new_player.current_health}{Colours.fg.red} / {Colours.fg.green}{entities.new_player.max_health}

{Colours.fg.orange}
What Would You Like To Do?
{Colours.tag('a') + Colours.description_colour} Attack {entities.new_player.current_enemy.name_string}
{Colours.tag('u') + Colours.description_colour} Use Item
{Colours.tag('e') + Colours.description_colour} Escape From Combat{Colours.fg.orange}


""")
    cls.display_items_used()


  @classmethod
  def start_combat(cls, enemy=None, is_players_turn=None):
    #Choose enemy
    if entities.new_player.current_enemy is entities.TemporaryEnemy:
      if entities.new_player.current_location is grimsden:
        enemy = entities.talgrog_the_giant
      
      cls.choose_enemy(enemy)

      #Initialize combat effects
      cls.set_effects()

    #Choose first turn
    if is_players_turn == None:
      if entities.new_player.has_combat_turn == None:
        entities.new_player.has_combat_turn = entities.new_player.armour.is_lighter_than(entities.new_player.current_enemy.armour)
    else:
      if entities.new_player.has_combat_turn == None:
        entities.new_player.has_combat_turn = is_players_turn

    while entities.new_player.current_health > 0 and entities.new_player.current_enemy.current_health > 0:
      clear()
      game.GameState.save_account()
      
      #Only update item effects if enemy has attacked
      if not entities.new_player.has_combat_turn:
        entities.new_player.has_combat_turn = True
        cls.update_items_used()


      #Player's turn
      if entities.new_player.has_combat_turn:
        if entities.new_player.combat_choice == None:
          entities.new_player.combat_choice = ''
          valid_inputs = ('a', 'u', 'e')

          while entities.new_player.combat_choice not in valid_inputs:
            cls.display_user_interface()

            entities.new_player.combat_choice = input(f"{Colours.input_colour}> ").lower().strip()

        entities.new_player.has_combat_turn = False

        #Player attacking
        if entities.new_player.combat_choice == 'a':
          entities.new_player.attack()
          entities.new_player.combat_choice = None
          
          if entities.new_player.current_enemy.is_dead():
            break

        #Player using items
        elif entities.new_player.combat_choice == 'u':
          player_used_item = objects.new_inventory.use_item()
          entities.new_player.has_combat_turn = player_used_item == False
          entities.new_player.combat_choice = None

        #Player escaping from combat
        elif entities.new_player.combat_choice == 'e':
          entities.new_player.escape_from_combat()
          entities.new_player.combat_choice = None

          if entities.new_player.has_escaped:
            break 
          elif not entities.new_player.has_escaped:
            entities.new_player.current_enemy.attack()
      

      game.GameState.save_account()

      #Enemy's turn
      if not entities.new_player.has_combat_turn:
        entities.new_player.current_enemy.choose_combat_action()

    
    entities.new_player.get_tired()
    
    if entities.new_player.current_enemy.is_dead():
      entities.new_player.current_enemy.drop_loot()
    
    if entities.new_player.has_all_artifacts():
      entities.new_player.lock_location()
    
    cls.reset_combat()

    game.GameState.save_account()
