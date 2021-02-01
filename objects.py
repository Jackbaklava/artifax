from colours import Colours
import entities
from system import System, clear, sleep, sleep_and_clear



class Object:
  def set_description(self, attributes_dict):
    word = lambda string, colour=Colours.fg.orange: f"{colour}{string}"
    comma = word(", ")

    updates = {True : {"dict" : self.increases,
                       "name" : "Player ",
                       "update_type" : "Increased"
               },

               False : {"dict" : self.decreases,
                        "name" : "Enemy ",
                        "update_type" : "Decreased"
               },
    }
    updates = updates[attributes_dict is self.increases]
    updates_dict, entity, update_type = updates["dict"], updates["name"], updates["update_type"]

    #Increased effects AKA description[0]
    updated_attributes = ' '
    updated_by = ' ' 
    
    for attribute in updates_dict:
      updated_attributes += word(entity, Colours.attribute_colour) + word(System.remove_unwanted_chars(attribute), Colours.attribute_colour)

      updated_by += word(updates_dict[attribute], Colours.attribute_colour) + word('%', Colours.attribute_colour)
      
      if attribute != list(updates_dict.keys())[-1]:
        updated_attributes += comma
        updated_by += comma
      else:
        updated_attributes += ' '
        updated_by += ' '
        
    if len(updated_attributes) > 1:
      string_to_add = word(update_type) + updated_attributes + word("by") + updated_by
      self.description.append(string_to_add)
    


class Item(Object):
  def __init__(self, name, price, affected_turns=0, increases={}, decreases={}):
    self.name = name
    self.name_string = f"{Colours.equipment_colour}{name}"
    self.price = price
    
    self.affected_turns = affected_turns
    self.increases = increases
    self.decreases = decreases

    self.category = "item"
    
    #Setting item's description
    self.description = []
    self.set_description(self.increases)
    self.set_description(self.decreases)

    if self.affected_turns > 0:
      self.description.append(f"{Colours.fg.red}Affected Turns: {self.affected_turns}")

           

vial_of_healing = Item("Vial of Healing", price=25, increases={"current_health" : 25})

flask_of_healing = Item("Flask of Healing", price=25, increases={"current_health" : 50})

kings_elixir = Item("King's Elixir", 25, 2, increases={"armour.defense" : 25, "weapon.accuracy" : 50})

dragons_amulet = Item("Dragon's Amulet", 25, 2, decreases={"armour.defense" : 50})


all_items = { "vlohg" : vial_of_healing,
              "fkohg" : flask_of_healing,
              "kser" : kings_elixir,
              "dsat" : dragons_amulet
}


def display_equipment_stats(key,  display_price=True, display_name=True, item_quantity='', extra_text=None):
  #jUST MAKE A COLLECTION!!!
  if key in entities.all_player_weapons or key in entities.all_player_armour or key in all_items or key in PlayerInventory.items_dict:
    key_to_display = Colours.tag(key) + ' '
    space_to_display = System.indent(key)

  else:
    key_to_display = ''
    space_to_display = ''
    specific_equipment = key


  if key in entities.all_player_weapons:
    specific_equipment = entities.all_player_weapons[key]

  elif key in entities.all_player_armour:
    specific_equipment = entities.all_player_armour[key]

  elif key in all_items:
    specific_equipment = all_items[key]

  elif key in PlayerInventory.items_dict:
    specific_equipment = PlayerInventory.items_dict[key][0]
    item_quantity = PlayerInventory.items_dict[key][1]


  if display_price:
    price_string = f"{space_to_display}{Colours.fg.yellow}Price: {specific_equipment.price}"
  else:
    price_string = ''
    
  if display_name:
    name_to_display = specific_equipment.name_string
  else:
    name_to_display = ''

  if type(item_quantity) == int:
    item_quantity = str(item_quantity) + ' '


  if isinstance(specific_equipment, entities.Weapon):
    print(f"""{key_to_display}{name_to_display}
{space_to_display}{Colours.fg.red}Damage: {specific_equipment.str_damage}
{space_to_display}{Colours.fg.orange}Crit Chance: {specific_equipment.str_crit_chance}
{space_to_display}{Colours.fg.cyan}Accuracy: {specific_equipment.str_accuracy}
{price_string}""")

  elif isinstance(specific_equipment, entities.Armour):
    print(f"""{key_to_display}{name_to_display}
{space_to_display}{Colours.fg.red}Defense: {specific_equipment.str_defense}
{space_to_display}{Colours.fg.cyan}Weight: {specific_equipment.weight}
{price_string}""")
    
  elif isinstance(specific_equipment, Item):
    if display_name:
      print(f"{key_to_display}{name_to_display}")
    else:
      space_to_display = System.indent(extra_text)
    
    for line in specific_equipment.description:
      print(space_to_display + line)
    
    if price_string != '':
      print(price_string)
      
  print('\n')


def display_current_equipment_stats(category):
  System.print_one_liner(f"{Colours.fg.blue}-")
  print(f"{Colours.fg.green + Colours.underline}Your {category.capitalize()}:{Colours.reset}")

  if category == "weapon":
    display_equipment_stats(entities.new_player.weapon, display_price=False)
      
  elif category == "armour":
    display_equipment_stats(entities.new_player.armour, display_price=False)

  System.print_one_liner(f"{Colours.fg.blue}-")



class PlayerInventory:
  items_dict = { '1' : [None, 0],
                 '2' : [flask_of_healing, 1],
                 '3' : [dragons_amulet, 23],
                 '4' : [kings_elixir, 2],
                 '5' : [None, 0]
  }
  total_slots = len(items_dict)


  @classmethod
  def display_items_dict(cls, clear_the_screen):
    if clear_the_screen:
      clear()
    else:
      sleep(1)

    for key in cls.items_dict:
      if cls.items_dict[key] == [None, 0]:
        print(f"{Colours.tag(key)} {Colours.none_string}")
        print('\n')
      else:
        display_equipment_stats(key, display_price=False, item_quantity=cls.items_dict[key][1])


  @classmethod
  def item_exists(cls, target_item):
    item_found = False
    
    for key in cls.items_dict:
      if target_item is cls.items_dict[key][0]:
        item_found = True
        break
      
    return item_found


  @classmethod
  def empty_slot_exists(cls):
    empty_slot_found = False
    
    for key in cls.items_dict:
      if cls.items_dict[key] == [None, 0]:
        empty_slot_found = True
        cls.empty_slot_key = key
        break

    return empty_slot_found
  

  @classmethod
  def add_item(cls, item_key, quantity=1):
    item_to_add = all_items[item_key]

    if cls.item_exists(item_to_add):
      for key in cls.items_dict:
        if cls.items_dict[key][0] == item_to_add:
          cls.items_dict[key][1] += quantity

    else:
      if cls.empty_slot_exists():
        cls.items_dict[cls.empty_slot_key] = [item_to_add, quantity]

      else:
        player_choice = ''
        clear()
        print(f"{Colours.fg.orange + Colours.bold + Colours.underline}Your inventory is currently full.{Colours.reset}")
        sleep(1.5)

        while player_choice not in cls.items_dict:
          clear()
          print(f"""{Colours.fg.red}Which item would you like to remove?   
{Colours.reset + Colours.fg.cyan}(Type a number from  1 to {cls.total_slots}, according to the item number you want to replace){Colours.fg.yellow}

{Colours.fg.orange + Colours.underline}Item you want to buy:
""")
          display_equipment_stats(item_key, item_quantity=quantity)
          print('\n')
          
          cls.display_items_dict(clear_the_screen=False)
          
          player_choice = input(f"{Colours.input_colour}> ")

          if player_choice not in cls.items_dict:
            clear()
            print(f"{Colours.fg.red + Colours.underline}Please enter a number from 1 to {cls.total_slots}.{Colours.reset}")
            sleep(2)

        cls.items_dict[player_choice] = [item_to_add, quantity]

    clear()
    print(f"{Colours.fg.orange}You received {Colours.bold + Colours.fg.red}{quantity} {Colours.fg.green}{item_to_add.name}{Colours.reset + Colours.fg.orange}.")
    sleep_and_clear(1.5)


  @classmethod
  def remove_item(cls, item_slot=None, mode=1):
    #Remove one item from one slot
    if mode == 1:
      item_quantity = cls.items_dict[item_slot][1]
    
      if item_quantity > 1:
        cls.items_dict[item_slot][1] -= 1
      
      else:
        cls.items_dict[item_slot] = [None, 0]
    
    #Clear whole inventory
    elif mode == "all":
      for key in cls.items_dict:
        cls.items_dict[key] = [None, 0]


  @classmethod
  def use_item(cls):
    item_to_use = ''

    while not item_to_use in cls.items_dict and item_to_use != "back":
      clear()
      print(f"""{Colours.fg.orange}Which item would you like to use?
{Colours.fg.lightblue}(Type the inventory slot number of the item you want to use)
{Colours.fg.cyan}(Type '{Colours.fg.green}back{Colours.fg.cyan}' to go back)

""")
      cls.display_items_dict(clear_the_screen=False)
      item_to_use = input(f"{Colours.input_colour}> ").lower().strip()
    

    if item_to_use != "back" and cls.items_dict[item_to_use] != [None, 0]:
      item_to_use = cls.items_dict[item_to_use][0]

      #Applying item effects to player
      entities.new_player.apply_item_effects("Increase", item_to_use.increases)

      #Applying item effects to enemy
      entities.new_player.current_enemy.apply_item_effects("Decrease", item_to_use.decreases)

     
      #Incrementing turns
      entities.new_player.items_used[item_to_use.name] = item_to_use.affected_turns
      
      clear()
      print(f"{Colours.fg.orange}You used {item_to_use.name_string}{Colours.fg.orange}.")
      sleep_and_clear(2)


    return item_to_use in cls.items_dict and cls.items_dict[item_to_use] != [None, 0]

    if item_to_use != "back":
      cls.remove_item(item_to_use)



class Shop:
  @staticmethod
  def display_initial_message(category):
    clear()
    print(f"""{Colours.fg.orange}Which {category} would you like to buy?
{Colours.fg.cyan}(Type the {Colours.fg.green}green letters {Colours.fg.cyan}in square brackets according to the {category} you want to buy)
(Type '{Colours.fg.red}back{Colours.fg.cyan}' to go back){Colours.fg.yellow}

{f"{Colours.fg.yellow + Colours.underline}You have {entities.new_player.gold_coins} gold coins{Colours.reset + Colours.fg.yellow}".center(130, "|")}
""")#need to make this better


  @classmethod
  def display_confirmation_message(cls):
    cls.equipment_quantity = 1
    cls.total_price = cls.equipment_to_purchase.price
    player_choice = ''

    if isinstance(cls.equipment_to_purchase, Item):
      while type(player_choice) != int:
        clear()
        player_choice = input(f"""{Colours.fg.blue}How many {Colours.fg.orange + 
Colours.underline}{cls.equipment_to_purchase.name}s{Colours.reset + Colours.fg.blue} would you like to buy?

{Colours.fg.cyan}(Type a {Colours.fg.green}number{Colours.fg.cyan})
{Colours.fg.orange}
> """)
        try:
          player_choice = int(player_choice)
        except ValueError:
           clear()
           print(f"{Colours.fg.red + Colours.underline}Please enter a number.{Colours.reset}")
           sleep(2)

      cls.equipment_quantity = player_choice
      cls.total_price = cls.equipment_to_purchase.price * cls.equipment_quantity


    clear()
    print(f"""{Colours.fg.blue}Are you sure you want to buy {Colours.fg.red + 
Colours.underline}{cls.equipment_quantity}{Colours.reset} {cls.equipment_to_purchase.name_string}{Colours.fg.blue} for {Colours.fg.yellow + Colours.underline}{cls.total_price} gold coins{Colours.reset + Colours.fg.blue}?

{Colours.fg.cyan}(Type the {Colours.fg.green}green letters {Colours.fg.cyan}in square brackets to {Colours.fg.green}confirm your purchase{Colours.fg.cyan})
{Colours.fg.cyan}(Type '{Colours.fg.red}back{Colours.fg.cyan}' to go back)

{Colours.fg.green + Colours.underline}{cls.equipment_to_purchase.category.capitalize()} you want to buy:{Colours.reset}""")

    display_equipment_stats(cls.key_of_equipment_to_purchase, display_price=False)


  @classmethod
  def handle_money(cls):
    clear()
    if entities.new_player.gold_coins >= cls.total_price:
      if isinstance(cls.equipment_to_purchase, entities.Weapon) or isinstance(cls.equipment_to_purchase, entities.Armour):
        print(f"{Colours.fg.pink}You bought {Colours.fg.orange + Colours.underline}{cls.equipment_to_purchase.name}{Colours.reset} {Colours.fg.pink}for {Colours.fg.yellow + Colours.underline}{cls.equipment_to_purchase.price} gold coins{Colours.reset + Colours.fg.pink}.")
        sleep(2)

      if isinstance(cls.equipment_to_purchase, entities.Weapon):
        entities.new_player.weapon = cls.equipment_to_purchase

      elif isinstance(cls.equipment_to_purchase, entities.Armour):
        entities.new_player.armour = cls.equipment_to_purchase

      elif isinstance(cls.equipment_to_purchase, Item):
        PlayerInventory.add_item(cls.key_of_equipment_to_purchase, cls.equipment_quantity)
      
      entities.new_player.gold_coins -= cls.total_price

    else:
      print(f"{Colours.fg.red + Colours.underline + Colours.bold}YOU DON'T HAVE ENOUGH GOLD COINS{Colours.reset}")
      sleep(2)
    

  @classmethod
  def handle_purchase(cls, category):
    first_player_choice = ''
    second_player_choice = ''
    valid_inputs_to_go_back = ["back", "'back'"]

    cls.has_made_purchase = False

    if category == "weapon":
      cls.equipment_dict = entities.all_player_weapons
    elif category == "armour":
      cls.equipment_dict = entities.all_player_armour
    elif category == "item":
      cls.equipment_dict = all_items

    while first_player_choice not in valid_inputs_to_go_back and cls.has_made_purchase == False:

      cls.display_initial_message(category)

      if category == "weapon" or category == "armour":
        display_current_equipment_stats(category)

      for key in cls.equipment_dict: 
        display_equipment_stats(key)

      first_player_choice = input(f"{Colours.fg.orange}> ").lower().strip()

      if first_player_choice in cls.equipment_dict:
        cls.key_of_equipment_to_purchase = first_player_choice
        cls.equipment_to_purchase = cls.equipment_dict[first_player_choice]
        second_player_choice = ''

        while second_player_choice not in valid_inputs_to_go_back and cls.has_made_purchase == False:

          cls.display_confirmation_message()

          if category == "weapon" or category == "armour":
            display_current_equipment_stats(category)
          
          second_player_choice = input(f"{Colours.fg.orange}> ").lower().strip()

          if second_player_choice == cls.key_of_equipment_to_purchase:
            cls.handle_money()
            cls.has_made_purchase = True


  @classmethod
  def display_menu(cls):
    player_choice = ''

    while player_choice != "back":
      valid_inputs = ("weapon", "armour", "item")
      clear()
      System.print_title("SHOP")

      player_choice = input(f"""{Colours.fg.orange}What would you like to buy?

{Colours.tag("weapon") + Colours.fg.red} Weapons
{Colours.tag("armour") + Colours.fg.blue} Armour
{Colours.tag("item") + Colours.fg.pink} Special Items
{Colours.tag("back") + Colours.fg.yellow} Go Back

{Colours.fg.orange}> """).lower().strip()

      if player_choice in valid_inputs:
        cls.handle_purchase(player_choice)
