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

flask_of_healing = Item("Flask of Healing", price=50, increases={"current_health" : 50})

purple_slush = Item("Purple Slush", 50, 3, increases={"armour.defense" : 10, "weapon.accuracy" : 20, "weapon.crit_chance" : 10})

kings_elixir = Item("King's Elixir", 70, 2, increases={"armour.defense" : 25, "weapon.accuracy" : 50})

golems_breath = Item("Dragon's Amulet", 200, 2, increases={"weapon.accuracy" : 50}, decreases={"armour.defense" : 40})


all_items = { "vlohg" : vial_of_healing,
              "fkohg" : flask_of_healing,
              "purp" : purple_slush,
              "kser" : kings_elixir,
              "gsbh" : golems_breath
}


def display_equipment_stats(key,  display_price=True, display_name=True, item_quantity='', extra_text=None):
  if key in entities.all_player_weapons or key in entities.all_player_armour or key in all_items or key in new_inventory.items_dict:
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

  elif key in new_inventory.items_dict:
    specific_equipment = new_inventory.items_dict[key][0]
    item_quantity = new_inventory.items_dict[key][1]


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
      print(f"{key_to_display}{Colours.fg.red}{item_quantity}{name_to_display}")
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
  def __init__(self):
    self.items_dict = { '1' : [None, 0],
                        '2' : [None, 0],
                        '3' : [None, 0],
                        '4' : [None, 0],
                        '5' : [None, 0]
    }
    self.total_slots = len(self.items_dict)


  def display_items_dict(self, clear_the_screen):
    if clear_the_screen:
      clear()
    else:
      sleep(1)

    for key in self.items_dict:
      if self.items_dict[key] == [None, 0]:
        print(f"{Colours.tag(key)} {Colours.none_string}")
        print('\n')
      else:
        display_equipment_stats(key, display_price=False, item_quantity=self.items_dict[key][1])


  def item_exists(self, target_item):
    item_found = False
    
    for key in self.items_dict:
      if target_item is self.items_dict[key][0]:
        item_found = True
        break
      
    return item_found


  def empty_slot_exists(self):
    empty_slot_found = False
    
    for key in self.items_dict:
      if self.items_dict[key] == [None, 0]:
        empty_slot_found = True
        self.empty_slot_key = key
        break

    return empty_slot_found
  

  def add_item(self, item_key, quantity=1):
    item_to_add = all_items[item_key]

    if self.item_exists(item_to_add):
      for key in self.items_dict:
        if self.items_dict[key][0] == item_to_add:
          self.items_dict[key][1] += quantity

    else:
      if self.empty_slot_exists():
        self.items_dict[self.empty_slot_key] = [item_to_add, quantity]

      else:
        player_choice = ''
        clear()
        print(f"{Colours.fg.orange + Colours.bold + Colours.underline}Your inventory is currently full.{Colours.reset}")
        sleep(1.5)

        while player_choice not in self.items_dict:
          clear()
          print(f"""{Colours.fg.red}Which item would you like to remove?   
{Colours.reset + Colours.fg.cyan}(Type a number from  1 to {self.total_slots}, according to the item number you want to replace){Colours.fg.yellow}

{Colours.fg.orange + Colours.underline}Item you want to buy:
""")
          display_equipment_stats(item_key, item_quantity=quantity)
          print('\n')
          
          self.display_items_dict(clear_the_screen=False)
          
          player_choice = input(f"{Colours.input_colour}> ")

          if player_choice not in self.items_dict:
            clear()
            print(f"{Colours.fg.red + Colours.underline}Please enter a number from 1 to {self.total_slots}.{Colours.reset}")
            sleep(2)

        self.items_dict[player_choice] = [item_to_add, quantity]

    clear()
    print(f"{Colours.fg.orange}You received {Colours.bold + Colours.fg.red}{quantity} {Colours.fg.green}{item_to_add.name}{Colours.reset + Colours.fg.orange}.")
    sleep_and_clear(1.5)


  def remove_item(self, item_slot=None):
    item_quantity = self.items_dict[item_slot][1]
    
    if item_quantity > 1:
      self.items_dict[item_slot][1] -= 1
      
    else:
      self.items_dict[item_slot] = [None, 0]
    


  def use_item(self):
    player_choice = ''
    player_used_item = False

    while not player_choice in self.items_dict and player_choice != "back":
      clear()
      print(f"""{Colours.fg.orange}Which item would you like to use?
{Colours.fg.lightblue}(Type the inventory slot number of the item you want to use)
{Colours.fg.cyan}(Type '{Colours.fg.green}back{Colours.fg.cyan}' to go back)

""")
      self.display_items_dict(clear_the_screen=False)
      player_choice = input(f"{Colours.input_colour}> ").lower().strip()
    

    if player_choice != "back" and self.items_dict[player_choice] != [None, 0]:
      #Set to True
      player_used_item = True
      
      #Get item object from inventory slot
      item_object = self.items_dict[player_choice][0]
      
      #Remove item
      self.remove_item(player_choice)

      #Applying item effects
      entities.new_player.apply_item_effects("Increase", item_object.increases)

      entities.new_player.current_enemy.apply_item_effects("Decrease", item_object.decreases)

      #Incrementing turns
      entities.new_player.items_used[item_object.name] = item_object.affected_turns
      
      clear()
      print(f"{Colours.fg.orange}You used {item_object.name_string}{Colours.fg.orange}.")
      sleep_and_clear(1.5)
    
      
    return player_used_item



new_inventory = PlayerInventory()



class Shop:
  @staticmethod
  def display_initial_message(category):
    clear()
    print(f"""{Colours.fg.red + Colours.bold}Which {category} would you like to buy?{Colours.reset}

{Colours.fg.orange}(Type the {Colours.fg.green}green letters {Colours.fg.orange}in square brackets according to the {category} you want to buy)
(Type '{Colours.fg.red}back{Colours.fg.orange}' to go back){Colours.fg.yellow}

{f"{Colours.fg.yellow + Colours.underline}You have {entities.new_player.gold_coins} gold coins{Colours.reset + Colours.fg.yellow}".center(110, "|")}
""")


  @classmethod
  def display_confirmation_message(cls):
    cls.equipment_quantity = 1
    cls.total_price = cls.equipment_to_purchase.price
    player_choice = ''

    if isinstance(cls.equipment_to_purchase, Item):
      while type(player_choice) != int:
        clear()
        player_choice = input(f"""{Colours.fg.yellow}How many {Colours.fg.orange + 
Colours.underline}{cls.equipment_to_purchase.name}s{Colours.reset + Colours.fg.yellow} would you like to buy?

{Colours.fg.cyan}(Type a {Colours.fg.green}number{Colours.fg.cyan})
{Colours.fg.orange}
> """)
        try:
          player_choice = int(player_choice)
        except ValueError:
           clear()
           print(f"{Colours.alert('PLEASE ENTER A NUMBER!!!')}")
           sleep(2)

      cls.equipment_quantity = player_choice
      cls.total_price = cls.equipment_to_purchase.price * cls.equipment_quantity


    clear()
    print(f"""{Colours.fg.yellow}Are you sure you want to buy {Colours.fg.red + 
Colours.underline}{cls.equipment_quantity}{Colours.reset} {cls.equipment_to_purchase.name_string}{Colours.fg.yellow} for {Colours.fg.red + Colours.underline}{cls.total_price} gold coins{Colours.reset + Colours.fg.yellow}?

{Colours.fg.yellow}(Type {Colours.fg.green}y{Colours.fg.yellow} to {Colours.fg.green}confirm your purchase{Colours.fg.yellow})
{Colours.fg.yellow}(Type '{Colours.fg.red}back{Colours.fg.yellow}' to go back)

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
        new_inventory.add_item(cls.key_of_equipment_to_purchase, cls.equipment_quantity)
      
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

    #Initialize equipment_dict
    if category == "weapon":
      cls.equipment_dict = entities.all_player_weapons
    elif category == "armour":
      cls.equipment_dict = entities.all_player_armour
    elif category == "item":
      cls.equipment_dict = all_items

    #main shop loop
    while first_player_choice not in valid_inputs_to_go_back and cls.has_made_purchase == False:

      cls.display_initial_message(category)

      if category == "weapon" or category == "armour":
        display_current_equipment_stats(category)

      for key in cls.equipment_dict: 
        display_equipment_stats(key)

      first_player_choice = input(f"{Colours.fg.orange}> ").lower().strip()

      #Check if player wants to buy something
      if first_player_choice in cls.equipment_dict:
        cls.key_of_equipment_to_purchase = first_player_choice
        cls.equipment_to_purchase = cls.equipment_dict[first_player_choice]
        second_player_choice = ''

        #Ask for confirmation
        while second_player_choice not in valid_inputs_to_go_back and cls.has_made_purchase == False:

          cls.display_confirmation_message()

          if category == "weapon" or category == "armour":
            display_current_equipment_stats(category)
          
          second_player_choice = input(f"{Colours.fg.orange}> ").lower().strip()

          #Check if player has confirmed purchase confirmation
          if second_player_choice == "y":
            cls.handle_money()
            cls.has_made_purchase = True


  @classmethod
  def display_menu(cls):
    player_choice = ''

    while player_choice != "back":
      valid_inputs = ("weapon", "armour", "item")
      clear()
      System.print_title("SHOP")

      player_choice = input(f"""{Colours.fg.orange + Colours.bold}What would you like to buy?{Colours.reset}

{Colours.tag("weapon") + Colours.fg.red} Weapons
{Colours.tag("armour") + Colours.fg.blue} Armour
{Colours.tag("item") + Colours.fg.pink} Special Items
{Colours.tag("back") + Colours.fg.yellow} Go Back

{Colours.fg.orange}> """).lower().strip()

      if player_choice in valid_inputs:
        cls.handle_purchase(player_choice)
