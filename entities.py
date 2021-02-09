from colours import Colours
import exploration
import objects
import operator
import random
import setting
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
common_weapon = Weapon("Common Armour", (5, 10), 5)
rare_weapon = Weapon("Rare Weapon", (20, 30), 10)
epic_weapon = Weapon("Epic Weapon", (30, 50), 15)
dragon_claws = Weapon("Dragon Claws", (35, 60), 25)
doomsblade = Weapon("Doomsblade", (40, 70), 20)

#Player weapons
copper_katana = Weapon("Copper Katana", (3, 20), 7, crit_chance=20)
iron_sword = Weapon("Iron Sword", (10, 25), 12, crit_chance=13, price=75)
great_axe = Weapon("Great Axe", (15, 40), 9, crit_chance=8, price=120)
anduril = Weapon("Andúril", (30, 50), 15, crit_chance=7, price=200)
excalibur = Weapon("Excalibur", (45, 60), 17, crit_chance=5, price=350)

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

    rdm_int = random.randint(1, 100)
    return rdm_int in int_range



#Enemy armour
common_armour = Armour("Common Armour", 0.9, "Light")
rare_armour = Armour("Rare Armour", 0.75, "Medium")
epic_armour = Armour("Epic Armour", 0.65, "Medium")
dragon_skin = Armour("Dragon Skin", 0.6, "Light")
darkmail = Armour("Darkmail", 0.5, "Heavy")

#Player armour
leather_tunic = Armour("Leather Tunic", 1, "Light")
chainmail = Armour("Chanimail", 0.8, "Medium", 100)
mithril_chestplate = Armour("Mithril Chestplate", 0.65, "Light", 175)
guardian_armour = Armour("Guardian Armour", 0.5, "Heavy", 400)

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
      
    self.current_health = round(self.current_health)
      
    clear()
    print(f"{Colours.fg.cyan}{entity} {Colours.fg.cyan}regained {Colours.fg.red + Colours.underline}{percentage_to_heal}%{Colours.reset + Colours.fg.cyan} of {possessive_pronoun} {Colours.fg.green}health{Colours.fg.cyan}.")
    sleep_and_clear(2)


  def take_damage(self, raw_damage, multiplier=1, armour_absorption=True):
    defense = 1
    if armour_absorption:
      defense = self.armour.defense
      
    damage_taken = raw_damage * defense
    damage_taken *= multiplier
    
    damage_taken = round(damage_taken)
    
    self.current_health -= damage_taken

    return damage_taken
  

  is_dead = lambda self: self.current_health <= 0



class TemporaryEnemy(Entity):
  armour = common_armour
  weapon = common_weapon

  attributes = locals()



class Player(Entity):
  #I didn't put all the attributes as parameters because it looks ugly, and because any instances created from this class will always have these default arguments
  def __init__(self):
    self.main_menu_choice = None
    self.current_health = 100
    self.max_health = 100
    self.armour = leather_tunic
    self.weapon = copper_katana
    self.current_location = setting.all_locations["vod"]
    self.gold_coins = 0

    self.artifacts_collected = []
    self.artifacts_not_collected = list(setting.all_artifacts)
    self.total_artifacts = len(setting.all_artifacts)
    self.has_won = False

    self.is_tired = [False, False, False]
    self.can_travel = True
  
    #Combat variables
    self.current_enemy = TemporaryEnemy
    self.combat_choice = None
    self.has_combat_turn = None
    self.has_escaped = None
    self.items_used = {}
  
    self.attributes = vars(self)


  def travel(self):
    if self.can_travel:
      player_choice = ''
      locations_copy = setting.all_locations.copy()
      del locations_copy['gd']

      while player_choice not in locations_copy and player_choice != 'back':
        clear()
        print(f"{Colours.fg.orange}Where Would You Like To Travel?" + '\n')

        for key in locations_copy:
          location = setting.all_locations[key]

          if location != self.current_location:
            print(f"{Colours.tag(key)} {location.name_string}")

        print('\n' + f"{Colours.tag('back')} {Colours.fg.orange}Go Back" + '\n')
        player_choice = input(f"{Colours.fg.orange}> ")

      if player_choice in setting.all_locations:
        self.current_location = setting.all_locations[player_choice]
        clear()
        print(f"{Colours.fg.orange}You travelled to {self.current_location.name_string}{Colours.fg.orange}.")
        sleep_and_clear(2)
      
      
    else:
      clear()
      print(f"{Colours.fg.orange}You are not allowed to travel anymore because you have arrived at the Final Boss' location. {Colours.fg.red + Colours.bold}Prepare to fight him.{Colours.reset}")
      sleep_and_clear(4)
    

  def open_backpack(self):
    objects.new_inventory.display_items_dict(clear_the_screen=True)
    objects.display_current_equipment_stats("weapon")
    objects.display_current_equipment_stats("armour")

    print('\n')
    input(f"{Colours.input_colour}> ")


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
    player_choice = ''
    valid_inputs = ("short", "long", "back")
    not_tired_string = f"{Colours.alert('You Try To Sleep, But Feel Well Rested. Get Tired By Defeating Enemies In The Wilderness.')}"
    
    while player_choice not in valid_inputs:
      clear()
      player_choice = input(f"""{Colours.fg.orange}Which rest would you like to take?

{Colours.tag("short")} {Colours.fg.yellow}Short Rest {Colours.fg.red + Colours.underline}(Heals 50% of your health){Colours.reset}
{Colours.tag("long")} {Colours.fg.yellow}Long Rest {Colours.fg.red + Colours.underline}(Heals 100% of your health{Colours.reset + Colours.fg.red} + {Colours.fg.red + Colours.underline}Chance to get attacked{Colours.reset + Colours.fg.red})

{Colours.tag('back')} {Colours.fg.yellow} Go Back

{Colours.fg.orange}
> """).lower().strip()

      clear()

      #Player is taking short rest
      if player_choice == "short":
        if self.is_tired[0] and self.is_tired[1]:
          self.is_tired[0] = False
          self.is_tired[1] = False
          
          self.heal(50)

        else:
          print(not_tired_string)
          sleep_and_clear(3)


      #Player is taking long rest
      elif player_choice == "long":
        if False not in self.is_tired:
          self.is_tired = [False, False, False]
          
          self.heal(100)

          rdm_int = random.randint(1,5)
          #Player got a nightmare
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
    rdm_int = random.randint(1, self.weapon.accuracy)

    #Player missed attack
    if rdm_int == 1:
      rdm_int = random.randint(1,2)
      if rdm_int == 1:
        print(f"{self.current_enemy.name_string}{Colours.fg.cyan} dodged your attack.")
      else:
        print(f"{Colours.fg.lightblue}You missed your attack.")
      sleep_and_clear(1.5)

    #Player hit attack
    else:
      multiplier = 1
      damage_range = self.weapon.damage
      raw_damage = random.randint(damage_range[0], damage_range[1])

      rdm_int = random.randint(1, self.weapon.crit_chance)

      #Player hit a critical hit (double damage)
      if rdm_int == 1:
        print(f"{Colours.fg.orange + Colours.bold + Colours.underline}It's a critical hit!!!{Colours.reset}")
        multiplier *= 2
        sleep_and_clear(1)
  
  
      damage_dealt = self.current_enemy.take_damage(raw_damage, multiplier)
      
      print(f"{Colours.fg.cyan}You attacked {self.current_enemy.name_string} {Colours.fg.cyan} and dealt {Colours.fg.orange}{damage_dealt} damage{Colours.fg.cyan}.")
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


  def lock_location(self, location="gd"):
    location = setting.all_locations[location]
    
    self.current_location = location
    self.can_travel = False


  @staticmethod
  def ask_for_help():
    clear()
    print(f"{Colours.fg.orange}You are stuck inside the game of {Colours.fg.green + Colours.underline}Artifax{Colours.reset + Colours.fg.orange} and in order to escape, you need to beat the game's boss, {talgrog_the_giant.name_string}{Colours.fg.orange}. But first, you need to explore each location to beat their respective {Colours.fg.red + Colours.bold}Artifact Keepers{Colours.reset + Colours.fg.orange}, who will drop artifacts upon dying. After you have collected all the artifacts, you will automatically be teleported to the final location, {setting.grimsden.name_string}{Colours.fg.orange}." + '\n')

    print(f"{Colours.tag('ProTip')} {Colours.fg.lightblue}Type '{Colours.fg.green}tip{Colours.fg.lightblue}'' in the main menu for a useful game tip." + '\n')

    input(f"{Colours.input_colour}> ")


  @staticmethod
  def get_tip():
    tips = ("Buy and use different types of items to gain an edge in combat.",
            "Sleep to regenerate upto 100% of your health. But be aware of nightmares!",
            "When in doubt, escape from combat.",
            "Type 'bkp' in the main menu to access your inventory, weapon, and armour.",
            "Try out all the different commands in the main menu.",
            "Weapons with higher crit chance increase the chance of landing a double damage hit on your enemy.",
            "Read this amazing article on how to be the best at this game: https://bit.ly/3bim457"
    )

    rdm_tip = random.choice(tips)

    clear()
    print(f"{Colours.fg.yellow}{rdm_tip}" + '\n')
    input(f"{Colours.input_colour}> ")

    
  has_all_artifacts = lambda self: len(self.artifacts_collected) == self.total_artifacts
  
  check_artifacts_amount = lambda self: len(self.artifacts_collected)


new_player = Player()



class Enemy(Entity):
  def __init__(self, name, max_health, armour, weapon, spawn_location, spawn_range, gold_coins_drop=(1, 2)):
    self.name_string = f"{Colours.enemy_colour}{name}{Colours.reset}"
    self.max_health = max_health
    self.armour = armour
    self.weapon = weapon
    
    self.spawn_location = list(map(lambda key: setting.all_locations[key], spawn_location))
    self.spawn_range = range(spawn_range[0], spawn_range[1])
    
    self.gold_coins_drop = gold_coins_drop
    self.attributes = vars(self)


  def choose_combat_action(self):
    #Boss
    if isinstance(self, Boss):
      rdm_int = random.randint(1, 100)
      
      if rdm_int in self.attacking_chance:
        self.attack()

      else:
        #Heal 50% health
        if self.current_health <= System.calculate_percentage(total=self.max_health, percentage=50) and self.has_healed == False:
          self.heal(50)
          self.has_healed = True

        #Stun player (10 damage + extra turn)
        else:
          self.stun()
          
    #Normal Enemy
    else:
      self.attack()


  def attack(self):
    clear()
    rdm_int = random.randint(1, self.weapon.accuracy)

    #Enemy missed its attack
    if rdm_int == 1:
      rdm_int = random.randint(1,2)
      if rdm_int == 1:
        print(f"{Colours.fg.cyan}You dodged {self.name_string}{Colours.fg.cyan}'s attack.")
      else:
        print(f"{self.name_string}{Colours.fg.cyan} missed it's attack.")

    #Enemy hit attack
    else:
      damage_range = self.weapon.damage
      raw_damage = random.randint(damage_range[0], damage_range[1])

      damage_dealt = new_player.take_damage(raw_damage)

      print(f"{self.name_string + Colours.fg.cyan} attacked you, and dealt{Colours.fg.orange} {damage_dealt} damage{Colours.fg.cyan}.")

    sleep_and_clear(1.5)


  def drop_gold_coins(self):
    gold_coins_dropped = random.randint(self.gold_coins_drop[0], self.gold_coins_drop[1])
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
      
{Colours.tag('y')} {Colours.fg.blue}Yes
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

    if not self is artifact_keeper and not self is talgrog_the_giant:
      rdm_int = random.randint(1, 100)

      #Drop gold coins
      if rdm_int in range(1, 91):
        self.drop_gold_coins()

      #Drop weapon
      elif rdm_int in range(91, 96):
        if self.weapon.can_drop:
          self.drop_equipment(self.weapon)
        else:
          self.drop_gold_coins()

      #Drop armour
      elif rdm_int in range(96, 101):
        if self.armour.can_drop:
          self.drop_equipment(self.armour)
        else:
          self.drop_gold_coins()


    #Drop artifact
    elif self is artifact_keeper:
      filtered_artifacts = list(filter(lambda artifact: artifact.location is new_player.current_location, setting.all_artifacts))
      
      artifact_to_add = filtered_artifacts[0]
      new_player.artifacts_collected.append(artifact_to_add)
      new_player.artifacts_not_collected.remove(artifact_to_add)

      print(f"{Colours.fg.green}You received {artifact_to_add.name_string}{Colours.fg.green}.")


    sleep_and_clear(1)



#Enemies that spawn in Valley of Dawn
bandit = Enemy("Bandit", 65, common_armour, common_weapon, ["vod"], (1, 191), gold_coins_drop=(1, 5))
goblin = Enemy("Goblin", 50, common_armour, common_weapon, ["vod"], (191, 201), gold_coins_drop=(1, 10))

#Enemies that spawn in Forest of Fangarr
orc = Enemy("Orc", 90, common_armour, common_weapon, ["fof"], (1, 71), gold_coins_drop=(5, 15))
bone_bat = Enemy("Bone Bat", 50, common_armour, rare_weapon, ["fof"], (71, 161), gold_coins_drop=(1, 6))
owl_bear = Enemy("Owlbear", 120, rare_armour, epic_weapon, ["fof"], (161, 196), gold_coins_drop=(30, 50))
ashwing = Enemy("Ashwing", 120, dragon_skin, dragon_claws, ["fof"], (196, 201), gold_coins_drop=(80, 200))

#Enemies that spawn in Iron Mountains
highland_orc = Enemy("Highland Orc", 100, rare_armour, rare_weapon, ["im"], (1, 71), gold_coins_drop=(2, 15))
gargoyle = Enemy("Gargoyle", 80, epic_armour, rare_weapon, ["im"], (71, 161), gold_coins_drop=(20, 30))
night_hunter = Enemy("Night Hunter", 110, darkmail, epic_weapon, ["im"], (161, 196), gold_coins_drop=(50, 100))
kavauri = Enemy("Kavauri", 150, dragon_skin, dragon_claws, ["im"], (196, 201), gold_coins_drop=(150, 300))

#Artifact Keeper can spawn in any location
artifact_keeper = Enemy("Artifact Keeper", 15, darkmail, doomsblade, ["vod", "fof", "im"], (191, 201))


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



class Boss(Enemy):
  def __init__(self, name, max_health, armour, weapon):
    self.name_string = f"{Colours.enemy_colour}{name}{Colours.reset}"
    self.max_health = max_health
    self.armour = armour
    self.weapon = weapon
    self.attacking_chance = range(1, 81)

    self.has_healed = False

    self.attributes = vars(self)


  def stun(self):
    raw_damage = int(System.calculate_percentage(total=new_player.max_health, percentage=5))
    
    new_player.take_damage(raw_damage, armour_absorption=False)

    clear()
    print(f"{self.name_string}{Colours.fg.orange} stunned you for {Colours.fg.red}{raw_damage}{Colours.fg.orange} damage.")
    print(f"{self.name_string}{Colours.fg.lightblue} gained an extra turn.")
    sleep_and_clear(2)

    self.attack()



talgrog_the_giant = Boss("Talgrog The Giant", 200, darkmail, doomsblade)
