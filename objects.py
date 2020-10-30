from colours import Colours
import exploration
import items
from setting import rune_of_daylight, primal_shard, tablet_of_destiny, azures_gauntlet, all_artifacts, all_locations
from system import sleep, clear, sleep_and_clear, print_heading
import random as rdm



class Weapon:
  def __init__(self, name, damage, accuracy, crit_chance=1, price=0, can_drop=False):
    self.name_string = f"{Colours.equipment_colour}{name}"
    self.damage = damage
    self.accuracy = accuracy
    self.crit_chance = crit_chance
    self.price = price
    self.can_drop = can_drop
    
    self.category = 'weapon'

    self.str_damage = f"{damage[0]} - {damage[1]} "
    first_calc = self.accuracy - 1
    self.str_accuracy = f"{round(first_calc / self.accuracy * 100, 2)}%"
    self.str_crit_chance = f"{round(self.crit_chance ** -1 * 100, 2)}%"



#Enemy weapons
rusty_sword = Weapon("Rusty Sword", (3, 19), 7, can_drop=True)
mortemir = Weapon("Mortemir", (12, 30), 15)
doomsblade = Weapon("Doomsblade", (10, 45), 20)

#Player weapons
copper_katana = Weapon("Copper Katana", (3, 19), 8, 20, 0)
iron_sword = Weapon("Iron Sword", (7, 25), 13, 13, 75)
great_axe = Weapon("Great Axe", (15, 30), 9, 8, 150)
anduril = Weapon("Andúril", (10, 30), 15, 5, 150)

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
    
    self.category = 'armour'

    self.str_defense =  f"{int(100 - self.defense * 100)}%"


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



class TemporaryEnemy:
  armour = darkmail
  weapon = rusty_sword



class Player:
  current_health = 100
  max_health = 100
  armour = leather_tunic
  weapon = anduril
  current_location = all_locations["vod"]
  gold_coins = 50

  artifacts_collected = []
  artifacts_not_collected = [rune_of_daylight, primal_shard, tablet_of_destiny, azures_gauntlet]
  number_of_artifacts_collected = len(artifacts_collected)
  total_artifacts = 3

  is_tired = [False, False, False]
  
  #Combat variables
  current_enemy = TemporaryEnemy
  has_escaped = None
  current_item_effects = { "King's Elixir" : 0,
                           "Dragon's Amulet" : 0
  }


  @classmethod
  def travel(cls):
    player_choice = ''
    locations_copy = all_locations.copy()
    del locations_copy['gd']

    while player_choice not in locations_copy and player_choice != 'back':
      clear()
      print(f"{Colours.fg.orange}Where Would You Like To Travel?" + '\n')

      for key in locations_copy:
        location = all_locations[key]

        if location != Player.current_location:
          print(f"{Colours.fg.green + Colours.underline}[{key}]{Colours.reset}{location.colour} {location.name}")

      print('\n' + f"{Colours.fg.green + Colours.underline}[back]{Colours.reset + Colours.fg.yellow} Go Back" + '\n')
      player_choice = input(f"{Colours.fg.orange}> ")


    if player_choice in all_locations:
      cls.current_location = all_locations[player_choice]

      clear()
      print(f"{Colours.fg.orange}You successfully travelled to {Player.current_location.colour + Colours.underline + Colours.bold}{Player.current_location.name}{Colours.reset + Colours.fg.orange}.")

      sleep_and_clear(2)


  @classmethod
  def open_artipedia(cls):
    clear()
    
    print(f"{Colours.fg.orange + Colours.bold}Artifacts Collected:{Colours.reset}")
    for artifact in cls.artifacts_collected:
      artifact.display_artifact()
    print('\n')

    print(f"{Colours.fg.orange + Colours.bold}Artifacts Not Collected:{Colours.reset}")
    for artifact in cls.artifacts_not_collected:
      artifact.display_artifact()
    print('\n')

    input(f"{Colours.fg.orange}> ")
    

  @classmethod
  def heal(cls, percentage_to_heal):
    value_to_heal = percentage_to_heal / 100 * cls.max_health
    cls.current_health += value_to_heal
    
    if cls.current_health > cls.max_health:
      cls.current_health = cls.max_health
      
    clear()
    print(f"{Colours.fg.cyan}You regained {Colours.fg.red + Colours.underline}{percentage_to_heal}%{Colours.reset + Colours.fg.cyan} of your {Colours.fg.green}health{Colours.fg.cyan}.")
    sleep_and_clear(2)


  @classmethod
  def get_tired(cls):
    for index, value in enumerate(cls.is_tired):
      if value == False:
        cls.is_tired[index] = True
        break


  @classmethod
  def sleep_for_health(cls):
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
        if cls.is_tired[0] and cls.is_tired[1]:
          cls.is_tired[0] = False
          cls.is_tired[1] = False
          
          cls.heal(50)

        else:
          print(not_tired_string)
          sleep_and_clear(3)


      elif player_choice == 'long':
        if False not in cls.is_tired:
          cls.is_tired = [False, False, False]
          
          cls.heal(100)

          rdm_int = rdm.randint(1,5)
          if rdm_int == 5:
            exploration.Combat.start(goblin, is_players_turn=False)
            
        else:
          print(not_tired_string)
          sleep_and_clear(3)


  @classmethod
  def equip(cls, equipment_to_equip):
    if equipment_to_equip.category == 'weapon':
      cls.weapon = equipment_to_equip

    elif equipment_to_equip.category == 'armour':
      cls.armour = equipment_to_equip

    clear()
    print(f"{Colours.fg.orange}You equipped {equipment_to_equip.name_string}{Colours.fg.orange}.")
    sleep_and_clear(1)


  @classmethod
  def attack(cls):
    clear()
    rdm_int = rdm.randint(1, cls.weapon.accuracy)

    if rdm_int == 1:
      rdm_int = rdm.randint(1,2)
      if rdm_int == 1:
        print(f"{Player.current_enemy.name_string}{Colours.fg.cyan} dodged your attack.")
      else:
        print(f"{Colours.fg.lightblue}You missed your attack.")
      sleep_and_clear(1.5)

    else:
      player_attack_damage = cls.weapon.damage
      damage_taken = round(rdm.randint(player_attack_damage[0], player_attack_damage[1]) * cls.current_enemy.armour.defense)

      rdm_int = rdm.randint(1, cls.weapon.crit_chance)

      if rdm_int == 1:
        print(f"{Colours.fg.orange + Colours.bold + Colours.underline}It's a critical hit!!!{Colours.reset}")
        damage_taken = damage_taken * 2
        sleep_and_clear(1)

  
      cls.current_enemy.current_health -= damage_taken
      print(f"{Colours.fg.cyan}You attacked {cls.current_enemy.name_string}{Colours.fg.cyan} with your {cls.weapon.name_string}{Colours.fg.cyan},and dealt {Colours.fg.orange}{damage_taken} damage{Colours.fg.cyan}.")
      sleep_and_clear(1.5)


  @classmethod
  def escape_from_combat(cls):
    cls.has_escaped = Player.armour.is_lighter_than(Player.current_enemy.armour)

    clear()
    if cls.has_escaped:
      print(f"{Colours.fg.cyan}You successfully escaped from {Player.current_enemy.name_string}{Colours.fg.cyan}.")   

    else:
      print(f"""{Colours.fg.cyan}You tried to escape from {Player.current_enemy.name_string}{Colours.fg.cyan}, but failed.

{Player.current_enemy.name_string} {Colours.fg.cyan} gets another turn.
""")
    sleep_and_clear(2)


  @staticmethod
  def ask_for_help():
    pass


  @classmethod
  def check_for_death(cls):
    if cls.current_health <= 0:
      print(f"{Colours.fg.red + Colours.bold + Colours.underline}RIP")
      


class Enemy:
  def __init__(self, name, max_health, armour, weapon, spawn_location, spawn_range, gold_coins_drop=(1,50)):
    self.name_string = f"{Colours.enemy_colour}{name}{Colours.reset}"
    self.max_health = max_health
    
    self.armour = armour
    self.weapon = weapon
    
    self.spawn_location = list(map(lambda key: all_locations[key], spawn_location))
    self.spawn_range = range(spawn_range[0], spawn_range[1])
    
    self.gold_coins_drop = gold_coins_drop


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
      damage_taken = round(rdm.randint(enemy_attack_damage[0], enemy_attack_damage[1]) * Player.armour.defense)

      Player.current_health -= damage_taken

      print(f"{self.name_string + Colours.fg.cyan} attacked you, and dealt{Colours.fg.orange} {damage_taken} damage{Colours.fg.cyan}.")

    sleep_and_clear(1.5)


  def is_dead(self):
    if self.current_health <= 0:
      return True
    else:
      return False


  def drop_gold_coins(self):
    gold_coins_dropped = rdm.randint(self.gold_coins_drop[0], self.gold_coins_drop[1])
    Player.gold_coins += gold_coins_dropped
    
    print(f"{Colours.fg.lightblue}You recieved {Colours.fg.yellow}{gold_coins_dropped} gold coins{Colours.fg.lightblue}.")
  
  
  def drop_equipment(self, equipment_to_drop):
    valid_inputs = ('y', 'n')
    player_choice = ''

    while player_choice not in valid_inputs:
      clear()
      print(f"""{Colours.fg.orange}You found {equipment_to_drop.name_string}{Colours.fg.orange}.

      """)
      sleep(1)

      items.display_current_equipment_stats(equipment_to_drop.category)

      print(f"{Colours.fg.green + Colours.underline}{equipment_to_drop.category.capitalize()} you found:{Colours.reset}""")
      items.display_equipment_stats(equipment_to_drop, display_price=False)

      print(f"""{Colours.fg.orange}Are you sure you want to equip {equipment_to_drop.name_string} {Colours.fg.orange}?
      
{Colours.tag("y")} {Colours.fg.blue}Yes
{Colours.tag('n')} {Colours.fg.blue}No  
      """)

      player_choice = input(f"{Colours.input_colour}> ")

    if player_choice == 'y':
      Player.equip(equipment_to_drop)

    elif player_choice == 'n':
      pass

  
    
  def drop_loot(self):
    clear()
    print(f"{Colours.fg.green}You defeated {Player.current_enemy.name_string}{Colours.fg.green}!!!")
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
      filtered_artifacts = list(filter(lambda artifact: artifact.location is Player.current_location, all_artifacts))
      
      artifact_to_add = filtered_artifacts[0]
      Player.artifacts_collected.append(artifact_to_add)
      Player.artifacts_not_collected.remove(artifact_to_add)

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


#Enemies that spawn in Wompy Willows
phantom = Enemy("Phantom", 70, darkmail, rusty_sword, ["ww"], (1,61))
ghoul = Enemy("Ghoul", 90, darkmail, rusty_sword, ["ww"], (61, 121))
bane_cat = Enemy("Bane Cat", 50, darkmail, rusty_sword, ["ww"], (121, 151))
beshtrauming = Enemy("Beshtrauming", 150, darkmail, rusty_sword, ["ww"], (151, 181)) 
flagercroc = Enemy("Flagercroc", 150, darkmail, rusty_sword, ["ww"], (191, 201))

#Enemies that spawn in Iron Mountains
highland_orc = Enemy("Highland Orc", 100, darkmail, rusty_sword, ["im"], (1, 71))
gargoyle = Enemy("Gargoyle", 70, darkmail, rusty_sword, ["im"], (71, 121))
night_hunter = Enemy("Night Hunter", 100, darkmail, rusty_sword, ["im"], (121, 161))
kavauri = Enemy("Kavauri", 150, darkmail, rusty_sword, ["im"], (191, 201))

#Artifact Keeper can spawn in any location
artifact_keeper = Enemy("Artifact Keeper", 150, darkmail, rusty_sword, ["vod", "fof", "ww", "im"], (191, 201))

all_enemies = { "goblin" : goblin,
                "bandit" : bandit,

                "orc" : orc,
                "bone_bat" : bone_bat,
                "owl_bear" : owl_bear,
                "ashwing" : ashwing,

                "phantom" : phantom,
                "ghoul" : ghoul,
                "bane_cat" : bane_cat,
                "beshtrauming" : beshtrauming,
                "flagercroc" : flagercroc,

                "highland_orc" : highland_orc,
                "gargoyle" : gargoyle,
                "night_hunter" : night_hunter,
                "kavauri" : kavauri,

                "artifact_keeper" : artifact_keeper
}


def display_user_interface():
  headings_colour = Colours.fg.red + Colours.underline
  gold_colour = Colours.fg.yellow + Colours.underline
  tags_colour = Colours.fg.green + Colours.underline
  tags_explanation_colour = Colours.reset + Colours.fg.yellow
  ask_for_choice_colour = Colours.fg.orange

  clear()
  print_heading('ARTIFAX')

  print(
f"""{headings_colour}Your Health:{Colours.reset}{Colours.fg.green} {Player.current_health} / {Player.max_health} {Colours.reset}
{headings_colour}
Your Location:{Colours.reset + Colours.fg.orange} {Player.current_location.name}{Colours.reset}
{headings_colour}
Your Armour:{Colours.reset} {Player.armour.name_string}{Colours.reset}
{headings_colour}
Your Weapon:{Colours.reset} {Player.weapon.name_string}{Colours.reset}
{gold_colour}
Gold Coins:{Colours.reset + Colours.fg.yellow} {Player.gold_coins}{Colours.reset}
{headings_colour}
Artifacts Collected:{Colours.reset + Colours.fg.orange} {Player.number_of_artifacts_collected} / {Player.total_artifacts}
{headings_colour}
{Colours.reset + Colours.fg.orange + Colours.underline}
Things You Can Do:{tags_colour}
[ex]{tags_explanation_colour} Explore The Wilderness{tags_colour}
[sleep]{tags_explanation_colour} Sleep To Regenerate Your Health{tags_colour}
[travel]{tags_explanation_colour} Travel To A Different Location{tags_colour}
[inv]{tags_explanation_colour} Open Your Inventory{tags_colour}
[shop]{tags_explanation_colour} Open The Shop{tags_colour}
[art]{tags_explanation_colour} Open Artipedia{Colours.fg.lightblue + Colours.underline}

[help]{Colours.reset + Colours.fg.red} What am I supposed to do?
{ask_for_choice_colour + Colours.bold}
What Would You Like To Do?{Colours.reset}""")
