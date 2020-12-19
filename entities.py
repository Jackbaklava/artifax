from colours import Colours
import exploration
import objects
import operator
import random as rdm
from setting import all_artifacts, all_locations
from system import System, sleep, clear, sleep_and_clear



class Weapon:
  def __init__(self, name, damage, accuracy, crit_chance=10, price=0, can_drop=False):
    self.name_string = f"{Colours.equipment_colour}{name}"
    self.damage = damage
    self.accuracy = accuracy
    self.crit_chance = crit_chance
    self.price = price
    self.can_drop = can_drop

    #String attributes for displaying stats
    self.str_damage = f"{damage[0]} - {damage[1]} "
    
    first_calc = self.accuracy - 1
    self.str_accuracy = f"{round(first_calc / self.accuracy * 100, 2)}%"
    self.str_crit_chance = f"{round(self.crit_chance ** -1 * 100, 2)}%"

    #Default attributes for every instance
    self.category = 'weapon'
    self.attributes = vars(self)
    self.original_damage = damage
    self.original_accuracy = accuracy
    self.original_crit_chance = crit_chance



#Enemy weapons
rusty_sword = Weapon("Rusty Sword", (3, 19), 7, can_drop=True)
mortemir = Weapon("Mortemir", (12, 30), 15)
doomsblade = Weapon("Doomsblade", (10, 45), 20)

#Player weapons
copper_katana = Weapon("Copper Katana", (3, 19), 8, crit_chance=20)
iron_sword = Weapon("Iron Sword", (7, 25), 13, crit_chance=13, price=75)
great_axe = Weapon("Great Axe", (15, 30), 9, crit_chance=8, price=150)
anduril = Weapon("Andúril", (10, 30), 15, crit_chance=5, price=150)

all_player_weapons = { "insd" : iron_sword,
                       "gtae" : great_axe,
                       "al" : anduril
}



class Armour:
  def __init__(self, name, defense, weight, price=0, can_drop=False):
    self.name_string = f"{Colours.equipment_colour}{name}"
    self.defense = defense
    self.weight = weight
    self.price = price
    self.can_drop = can_drop

    #String attributes for displaying stats
    self.str_defense =  f"{int(100 - self.defense * 100)}%"

    #Default attributes for every instance
    self.category = 'armour'
    self.attributes = vars(self)
    self.original_defense = defense
    self.original_weight = weight


  def is_lighter_than(self, armour_to_compare):
    armour_weight_scores = { "Light" : 3,
                             "Medium" : 2,
                             "Heavy" : 1
    }
    player_armour_score = armour_weight_scores[self.weight]
    enemy_armour_score = armour_weight_scores[armour_to_compare.weight]

    if player_armour_score > enemy_armour_score:
      int_range = range(1, 76)
    elif player_armour_score == enemy_armour_score:
      int_range = range(1, 51)
    elif player_armour_score < enemy_armour_score:
      int_range = range(1, 26)

    rdm_int = rdm.randint(1, 100)
    return rdm_int in int_range



#Enemy armour
darkmail = Armour("Darkmail", 0.8, "Medium", can_drop=True)

#Player armour
leather_tunic = Armour("Leather Tunic", 1, "Light", 0)
chainmail = Armour("Chanimail", 0.75, "Medium", 100)
mithril_chestplate = Armour("Mithril Chestplate", 0.65, "Light", 175)
guardian_armour = Armour("Guardian Armour", 0.4, "Heavy", 200)

all_player_armour = { "cl" : chainmail,
                      "mlce" : mithril_chestplate,
                      "gnar" : guardian_armour
}



class Entity:
  def get_attribute(self, mode="current", attribute=None, need_value=True):
    object_chain = attribute.split(".")

    if mode == "original":
      object_chain[1] = "original_" + object_chain[1]

    if need_value:
      return self.attributes[object_chain[0]].attributes[object_chain[1]]
    else:
      return object_chain[-1]


  def update_attribute(self, attribute, operate, percentage):
    if attribute == "current_health":
      self.heal(percentage)

    else:
      #Getting the original value
      total = self.get_attribute("original", attribute)
      update_by = System.calculate_percentage(percentage=percentage, total=total)

      numbers_to_round = ("weapon.accuracy", "weapon.crit_chance")
      if attribute in numbers_to_round:
        update_by = round(update_by)
        
      object_chain = attribute.split(".")
 
      #Incrementing/Decrementing the current value
      #Rounding to avoid nums like 0.800000000002
      self.attributes[object_chain[0]].attributes[object_chain[1]] = round(operate(self.get_attribute(attribute=attribute), update_by), 2)
      
      
  def apply_item_effects(self, mode, attributes_to_update):
    #Opposite operators because defense and crit chance are better when subtracted (inverse)
    operators_dict = { "Increase" : operator.sub, 
                       "Decrease" : operator.add
    }
    operate = operators_dict[mode]

    inverse_attributes = ("accuracy")
    inverse_operate = list(filter(lambda value: not value is operate, operators_dict.values()))[0]

    for attribute in attributes_to_update:
      equipment_attribute = self.get_attribute(attribute=attribute, need_value=False)

      if equipment_attribute in inverse_attributes:
        operate = inverse_operate

      self.update_attribute(attribute, operate, attributes_to_update[attribute])


  def heal(self, percentage_to_heal):
    if isinstance(self, Player):
      entity = "You"
      possessive_pronoun = "your"
    else:
      entity = self.name_string
      possessive_pronoun = "its"

    value_to_heal = System.calculate_percentage(percentage_to_heal, total=self.max_health)
    
    self.current_health += value_to_heal
    
    if self.current_health > self.max_health:
      self.current_health = self.max_health
      
    clear()
    print(f"{Colours.fg.cyan}{entity} regained {Colours.fg.red + Colours.underline}{percentage_to_heal}%{Colours.reset + Colours.fg.cyan} of {possessive_pronoun} {Colours.fg.green}health{Colours.fg.cyan}.")
    sleep_and_clear(2)

  Need to make this func to complete Boss.stun()
  def take_damage(self, damage):
    pass


  is_dead = lambda self: self.current_health <= 0



class TemporaryEnemy(Entity):
  armour = darkmail
  weapon = rusty_sword

  attributes = locals()



class Player(Entity):
  #I didn't put all the attributes as parameters because it looks ugly, and because any instances created from this object will always have these default arguments
  def __init__(self):
    self.current_health = 100
    self.max_health = 100
    self.armour = leather_tunic
    self.weapon = anduril
    self.current_location = all_locations["vod"]
    self.gold_coins = 50

    self.artifacts_collected = []
    self.artifacts_not_collected = list(all_artifacts)
    self.num_of_artifacts_collected = len(self.artifacts_collected)
    self.total_artifacts = len(all_artifacts)

    self.is_tired = [False, False, False]
  
    #Combat variables
    self.current_enemy = TemporaryEnemy
    self.has_escaped = None
    self.items_used = { "King's Elixir" : 0,
                        "Dragon's Amulet" : 0
    }
  
    self.attributes = vars(self)


  def travel(self):
    player_choice = ''
    locations_copy = all_locations.copy()
    del locations_copy['gd']

    while player_choice not in locations_copy and player_choice != 'back':
      clear()
      print(f"{Colours.fg.orange}Where Would You Like To Travel?" + '\n')

      for key in locations_copy:
        location = all_locations[key]

        if location != self.current_location:
          print(f"{Colours.fg.green + Colours.underline}[{key}]{Colours.reset}{location.colour} {location.name}")

      print('\n' + f"{Colours.fg.green + Colours.underline}[back]{Colours.reset + Colours.fg.yellow} Go Back" + '\n')
      player_choice = input(f"{Colours.fg.orange}> ")


    if player_choice in all_locations:
      self.current_location = all_locations[player_choice]

      clear()
      print(f"{Colours.fg.orange}You travelled to {self.current_location.colour + Colours.underline + Colours.bold}{self.current_location.name}{Colours.reset + Colours.fg.orange}.")

      sleep_and_clear(2)


  def open_artipedia(self):
    clear()
    print(f"{Colours.fg.orange + Colours.bold}Artifacts Collected:{Colours.reset}")
    
    for artifact in self.artifacts_collected:
      artifact.display_artifact()

    print('\n')
    print(f"{Colours.fg.orange + Colours.bold}Artifacts Not Collected:{Colours.reset}")
    
    for artifact in self.artifacts_not_collected:
      artifact.display_artifact()
      
    print('\n')
    input(f"{Colours.fg.orange}> ")


  def get_tired(self):
    for index, value in enumerate(self.is_tired):
      if value == False:
        self.is_tired[index] = True
        break


  def sleep_for_health(self):
    player_choice = ""
    valid_inputs = ('short', 'long', 'back')
    not_tired_string = f"{Colours.fg.red + Colours.underline}You Try To Sleep, But Feel Well Rested. Get Tired By Defeating Enemies In The Wilderness."
    
    while player_choice not in valid_inputs:
      clear()
      player_choice = input(f"""{Colours.fg.orange}Which rest would you like to take?

{Colours.fg.green + Colours.underline}[short]{Colours.reset + Colours.fg.yellow} Short Rest {Colours.fg.red + Colours.underline}(Heals 50% of your health){Colours.reset}
{Colours.fg.green + Colours.underline}[long]{Colours.reset + Colours.fg.yellow} Long Rest {Colours.fg.red + Colours.underline}(Heals 100% of your health{Colours.reset + Colours.fg.red} + {Colours.fg.red + Colours.underline}Chance to get attacked{Colours.reset + Colours.fg.red})

{Colours.tag('back')} {Colours.fg.yellow} Go Back

{Colours.fg.orange}
> """).lower().strip()

      clear()

      if player_choice == 'short':
        if self.is_tired[0] and self.is_tired[1]:
          self.is_tired[0] = False
          self.is_tired[1] = False
          
          self.heal(50)

        else:
          print(not_tired_string)
          sleep_and_clear(3)


      elif player_choice == 'long':
        if False not in self.is_tired:
          self.is_tired = [False, False, False]
          
          self.heal(100)

          rdm_int = rdm.randint(1,5)
          if rdm_int == 5:
            exploration.Combat.start(goblin, is_players_turn=False)
            
        else:
          print(not_tired_string)
          sleep_and_clear(3)


  def equip(self, equipment_to_equip):
    if equipment_to_equip.category == "weapon":
      self.weapon = equipment_to_equip

    elif equipment_to_equip.category == "armour":
      self.armour = equipment_to_equip

    clear()
    print(f"{Colours.fg.orange}You equipped {equipment_to_equip.name_string}{Colours.fg.orange}.")
    sleep_and_clear(1)


  def attack(self):
    clear()
    rdm_int = rdm.randint(1, self.weapon.accuracy)

    if rdm_int == 1:
      rdm_int = rdm.randint(1,2)
      if rdm_int == 1:
        print(f"{self.current_enemy.name_string}{Colours.fg.cyan} dodged your attack.")
      else:
        print(f"{Colours.fg.lightblue}You missed your attack.")
      sleep_and_clear(1.5)

    else:
      player_attack_damage = self.weapon.damage
      damage_taken = round(rdm.randint(player_attack_damage[0], player_attack_damage[1]) * self.current_enemy.armour.defense)

      rdm_int = rdm.randint(1, self.weapon.crit_chance)

      if rdm_int == 1:
        print(f"{Colours.fg.orange + Colours.bold + Colours.underline}It's a critical hit!!!{Colours.reset}")
        damage_taken = damage_taken * 2
        sleep_and_clear(1)
  
  
      self.current_enemy.current_health -= damage_taken
      
      print(f"{Colours.fg.cyan}You attacked {self.current_enemy.name_string} {Colours.fg.cyan} and dealt {Colours.fg.orange}{damage_taken} damage{Colours.fg.cyan}.")
      sleep_and_clear(1.5)


  def escape_from_combat(self):
    print(self)
    self.has_escaped = self.armour.is_lighter_than(self.current_enemy.armour)

    clear()
    if self.has_escaped:
      print(f"{Colours.fg.cyan}You successfully escaped from {self.current_enemy.name_string}{Colours.fg.cyan}.")   

    else:
      print(f"""{Colours.fg.cyan}You tried to escape from {self.current_enemy.name_string}{Colours.fg.cyan}, but failed.

{self.current_enemy.name_string} {Colours.fg.cyan} gets another turn.
""")
    sleep_and_clear(2)


  @staticmethod
  def ask_for_help():
    pass


  @staticmethod
  def display_death_message():
    print(f"{Colours.fg.red + Colours.bold + Colours.underline}RIP")
      


new_player = Player()



class Enemy(Entity):
  def __init__(self, name, max_health, armour, weapon, spawn_location, spawn_range, gold_coins_drop=(1,50)):
    self.name_string = f"{Colours.enemy_colour}{name}{Colours.reset}"
    self.max_health = max_health
    self.armour = armour
    self.weapon = weapon
    
    self.spawn_location = list(map(lambda key: all_locations[key], spawn_location))
    self.spawn_range = range(spawn_range[0], spawn_range[1])
    
    self.gold_coins_drop = gold_coins_drop
    self.attributes = vars(self)


  def choose_combat_action(self):
    #Normal enemy
    if isinstance(self, Enemy):
      self.attack()

    #Boss
    else:
      rdm_int = rdm.randint(1, 100)
      if rdm_int in self.attacking_chance:
        self.attack()

      else:
        if self.current_health <= System.get_percentage(total=self.max_health, percentage=50) and self.has_healed == False:
          self.heal(50)

        else:
          self.stun()


  def attack(self):
    clear()
    rdm_int = rdm.randint(1, self.weapon.accuracy)

    #Enemy missed its attack
    if rdm_int == 1:
      rdm_int = rdm.randint(1,2)
      if rdm_int == 1:
        print(f"{Colours.fg.cyan}You dodged {self.name_string}{Colours.fg.cyan}'s attack.")
      else:
        print(f"{self.name_string}{Colours.fg.cyan} missed it's attack.")

    #Enemy hit its attack
    else:
      enemy_attack_damage = self.weapon.damage
      damage_taken = round(rdm.randint(enemy_attack_damage[0], enemy_attack_damage[1]) * new_player.armour.defense)

      new_player.current_health -= damage_taken

      print(f"{self.name_string + Colours.fg.cyan} attacked you, and dealt{Colours.fg.orange} {damage_taken} damage{Colours.fg.cyan}.")

    sleep_and_clear(1.5)


  def drop_gold_coins(self):
    gold_coins_dropped = rdm.randint(self.gold_coins_drop[0], self.gold_coins_drop[1])
    new_player.gold_coins += gold_coins_dropped
    
    print(f"{Colours.fg.lightblue}You recieved {Colours.fg.yellow}{gold_coins_dropped} gold coins{Colours.fg.lightblue}.")
  
  
  def drop_equipment(self, equipment_to_drop):
    valid_inputs = ('y', 'n')
    player_choice = ''

    while player_choice not in valid_inputs:
      clear()
      print(f"""{Colours.fg.orange}You found {equipment_to_drop.name_string}{Colours.fg.orange}.

      """)
      sleep(1)

      objects.display_current_equipment_stats(equipment_to_drop.category)

      print(f"{Colours.fg.green + Colours.underline}{equipment_to_drop.category.capitalize()} you found:{Colours.reset}""")
      objects.display_equipment_stats(equipment_to_drop, display_price=False)

      print(f"""{Colours.fg.orange}Are you sure you want to equip {equipment_to_drop.name_string} {Colours.fg.orange}?
      
{Colours.tag("y")} {Colours.fg.blue}Yes
{Colours.tag('n')} {Colours.fg.blue}No  
      """)

      player_choice = input(f"{Colours.input_colour}> ")

    if player_choice == 'y':
      new_player.equip(equipment_to_drop)

    elif player_choice == 'n':
      pass

  
    
  def drop_loot(self):
    clear()
    print(f"{Colours.fg.green}You defeated {new_player.current_enemy.name_string}{Colours.fg.green}!!!")
    sleep_and_clear(2)

    if not self is artifact_keeper:
      rdm_int = rdm.randint(1, 100)

      #drop gold coins
      if rdm_int in range(1, 91):
        self.drop_gold_coins()

      #drop weapon
      elif rdm_int in range(91, 96):
        if self.weapon.can_drop:
          self.drop_equipment(self.weapon)
        else:
          self.drop_gold_coins()

      #drop armour
      elif rdm_int in range(96, 101):
        if self.armour.can_drop:
          self.drop_equipment(self.armour)
        else:
          self.drop_gold_coins()


    #drop artifact
    else:
      filtered_artifacts = list(filter(lambda artifact: artifact.location is new_player.current_location, all_artifacts))
      
      artifact_to_add = filtered_artifacts[0]
      new_player.artifacts_collected.append(artifact_to_add)
      new_player.artifacts_not_collected.remove(artifact_to_add)

      print(f"{Colours.fg.green}You received {artifact_to_add.name_string}{Colours.fg.green}.")


    sleep_and_clear(1)



#Enemies that spawn in Valley of Dawn
bandit = Enemy("Bandit", 65, darkmail, rusty_sword, ["vod"], (1, 191))
goblin = Enemy("Goblin", 50, darkmail, rusty_sword, ["vod"], (191, 201))

#Enemies that spawn in Forest of Fangarr
orc = Enemy("Orc", 90, darkmail, rusty_sword, ["fof"], (1, 81))
bone_bat = Enemy("Bone Bat", 50, darkmail, rusty_sword, ["fof"], (81, 131))
owl_bear = Enemy("Owlbear", 120, darkmail, rusty_sword, ["fof"], (161, 191))
ashwing = Enemy("Ashwing", 50, darkmail, rusty_sword, ["fof"], (191, 201))

#Enemies that spawn in Iron Mountains
highland_orc = Enemy("Highland Orc", 100, darkmail, rusty_sword, ["im"], (1, 71))
gargoyle = Enemy("Gargoyle", 70, darkmail, rusty_sword, ["im"], (71, 121))
night_hunter = Enemy("Night Hunter", 100, darkmail, rusty_sword, ["im"], (121, 161))
kavauri = Enemy("Kavauri", 150, darkmail, rusty_sword, ["im"], (191, 201))

#Artifact Keeper can spawn in any location
artifact_keeper = Enemy("Artifact Keeper", 150, darkmail, rusty_sword, ["vod", "fof", "im"], (191, 201))

all_enemies = { "goblin" : goblin,
                "bandit" : bandit,

                "orc" : orc,
                "bone_bat" : bone_bat,
                "owl_bear" : owl_bear,
                "ashwing" : ashwing,

                "highland_orc" : highland_orc,
                "gargoyle" : gargoyle,
                "night_hunter" : night_hunter,
                "kavauri" : kavauri,

                "artifact_keeper" : artifact_keeper
}



class Boss(Entity):
  def __init__(self, name, max_health, armour, weapon):
    self.name_string = f"{Colours.enemy_colour}{name}{Colours.reset}"
    self.max_health = max_health
    self.armour = armour
    self.weapon = weapon
    self.attacking_chance = range(1, 81)

    self.has_healed = False

    self.attributes = vars(self)


  def stun(self):
    damage = System.get_percentage(total=new_player.max_health, percentage=5)
    #Damage Player

    clear()
    print(f"{self.name_string}{Colours.fg.orange} stunned you for {Colours.fg.red}{damage}{Colours.fg.orange} damage.")
    print(f"{self.name_string}{Colours.fg.lightblue} gained an extra turn.")
    sleep_and_clear(2)

    self.attack()



talgrog_the_giant = Boss("Talgrog The Giant", 200, darkmail, doomsblade)


#Colour mess, need dict of valid_inputs
def display_user_interface():
  headings_colour = Colours.fg.red + Colours.underline
  gold_colour = Colours.fg.yellow + Colours.underline
  tags_explanation_colour = Colours.reset + Colours.fg.yellow
  ask_for_choice_colour = Colours.fg.orange

  clear()
  System.print_title('ARTIFAX')

  print(
f"""{headings_colour}Your Health:{Colours.reset}{Colours.fg.green} {new_player.current_health} / {new_player.max_health} {Colours.reset}
{headings_colour}
Your Location:{Colours.reset + Colours.fg.orange} {new_player.current_location.name}{Colours.reset}
{headings_colour}
Your Armour:{Colours.reset} {new_player.armour.name_string}{Colours.reset}
{headings_colour}
Your Weapon:{Colours.reset} {new_player.weapon.name_string}{Colours.reset}
{gold_colour}
Gold Coins:{Colours.reset + Colours.fg.yellow} {new_player.gold_coins}{Colours.reset}
{headings_colour}
Artifacts Collected:{Colours.reset + Colours.fg.orange} {new_player.num_of_artifacts_collected} / {new_player.total_artifacts}
{headings_colour}
{Colours.reset + Colours.fg.orange + Colours.underline}
Things You Can Do:
{Colours.tag('ex')} {tags_explanation_colour}Explore The Wilderness
{Colours.tag('slep')} {tags_explanation_colour}Sleep To Regenerate Your Health
{Colours.tag('trv')} {tags_explanation_colour}Travel To A Different Location
{Colours.tag('inv')} {tags_explanation_colour}Open Your Inventory
{Colours.tag('shp')} {tags_explanation_colour}Open The Shop
{Colours.tag('art')} {tags_explanation_colour}Open Artipedia{Colours.fg.lightblue + Colours.underline}

[help]{Colours.reset + Colours.fg.red} What am I supposed to do?
{ask_for_choice_colour + Colours.bold}
What Would You Like To Do?{Colours.reset}""")
