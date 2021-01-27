from colours import Colours
import objects
import entities
import exploration
import pickle
from system import System, clear, sleep_and_clear


class Game:
  main_menu_choices = { "ex" : exploration.Combat.start_combat,
                        "slp" : entities.new_player.sleep_for_health,
                        "trv" : entities.new_player.travel,
                        "inv" : objects.PlayerInventory.display_items_dict,
                        "shp" : objects.Shop.display_menu,
                        "art" : entities.new_player.open_artipedia
  }


  @staticmethod
  def display_main_menu():
    tags_explanation_colour = Colours.fg.yellow

    clear()
    System.print_title('ARTIFAX')

    print(f"""
{Colours.heading("Your Health:")} {Colours.fg.green}{entities.new_player.current_health} / {entities.new_player.max_health}
{Colours.heading("Your Location:")} {entities.new_player.current_location.name_string}
{Colours.heading("Your Armour:")} {entities.new_player.armour.name_string}
{Colours.heading("Your Weapon:")} {entities.new_player.weapon.name_string}
{Colours.heading("Gold Coins:")} {Colours.fg.yellow}{entities.new_player.gold_coins}
{Colours.heading("Artifacts Collected:")} {Colours.fg.orange}{entities.new_player.check_artifacts_amount()} / {entities.new_player.total_artifacts}

{Colours.fg.orange + Colours.underline}
Things You Can Do:{Colours.reset}
{Colours.tag("ex")} {tags_explanation_colour}Explore The Wilderness
{Colours.tag("slep")} {tags_explanation_colour}Sleep To Regenerate Your Health
{Colours.tag("trv")} {tags_explanation_colour}Travel To A Different Location
{Colours.tag("inv")} {tags_explanation_colour}Open Your Inventory
{Colours.tag("shp")} {tags_explanation_colour}Open The Shop
{Colours.tag("art")} {tags_explanation_colour}Open Artipedia

{Colours.tag("help")} {Colours.fg.red}What am I supposed to do?
{Colours.input_colour + Colours.bold}
What Would You Like To Do?{Colours.reset}""")


  @staticmethod
  def display_death_message():
    print(f"{Colours.fg.red + Colours.bold + Colours.underline}RIP")
    input(f"{Colours.input_colour}")


  @staticmethod
  def display_win_message():
    print(f"{Colours.fg.green + Colours.bold}Congratulation!!! You completed the game and successfully escaped from it.")
    input(f"{Colours.input_colour}")


  @classmethod
  def play(cls):
    while not entities.new_player.is_dead() and not entities.new_player.current_enemy is entities.talgrog_the_giant:
      if entities.new_player.main_menu_choice == None:
        cls.display_main_menu()
        entities.new_player.main_menu_choice = input(f"{Colours.input_colour}> ").lower().strip()

      GameState.save_account()

      try:
        if entities.new_player.main_menu_choice == "inv":
          cls.main_menu_choices[entities.new_player.main_menu_choice](clear_the_screen=True)
          input(f"{Colours.fg.orange}> ")
        else:
          cls.main_menu_choices[entities.new_player.main_menu_choice]()

      except KeyError:
        clear()
        print(f"{Colours.alert('INVALID COMMAND, TYPE THE LETTERS IN THE SQUARE BRACKETS.')}")
        sleep_and_clear(2)

      entities.new_player.main_menu_choice = None

      GameState.save_account()
    

    if entities.new_player.current_enemy is entities.talgrog_the_giant:
      exploration.Combat.start_combat()

    if entities.new_player.is_dead():
      cls.display_death_message()
      GameState.reset_account()

    else:
      cls.diplay_win_message()
      GameState.reset_account()


    GameState.save_account()

  
  
class GameState:
  #Accounts.pkl structure:

  #accounts_dict = {(username, password) : {"Player" : object,
  #                                         "PlayerInventory" : object
  #                }
  #}
  @classmethod
  def get_accounts(cls):
    with open("accounts.pkl", "rb") as f:
      cls.accounts_dict = pickle.load(f)

  
  @classmethod
  def connect_account(cls):
    cls.get_accounts()
    
    valid_inputs = {'1' : cls.create_account,
                    '2' : cls.load_account
    }
    player_choice = ''
    
    while player_choice not in valid_inputs:
      clear()
      print(f"""{Colours.fg.orange}
Which of the following would you like to do?
{Colours.fg.lightblue}(Type the number in the square brackets)

{Colours.tag('1')} {Colours.fg.orange}Sign up for a new, fresh account
{Colours.tag('2')} {Colours.fg.orange}Login into an existing account to load epic progress
""")
      player_choice = input(f"{Colours.input_colour}> ")
      
    valid_inputs[player_choice]()

  
  @classmethod
  def create_account(cls):
    chosen_username, chosen_password, confirmed_password = None, None, None
    
    while (chosen_username, chosen_password) in cls.accounts_dict or chosen_password != confirmed_password:
      cls.get_accounts()
      clear()
      
      chosen_username = input(f"{Colours.fg.orange}Username: ")
      chosen_password = input(f"{Colours.fg.red}Password: ")
      confirmed_password = input(f"{Colours.fg.red}Confirm Password: ")

      #Exceptions
      #Everyone has unique accounts because username AND password are hashed to objects
      if (chosen_username, chosen_password) in cls.accounts_dict:
        clear()
        print(f"{Colours.fg.red}An account with the username '{chosen_username}' and password '{chosen_password}' already exists. Please Sign In.")
        sleep_and_clear(2)
        
      elif chosen_password != confirmed_password:
        clear()
        print(f"{Colours.fg.red}Your password '{chosen_password}' doesn't match your confirmed password '{confirmed_password}'. Please try again.")
        sleep_and_clear(2)
   
    cls.account = (chosen_username, chosen_password)

    cls.save_account()

  
  @classmethod
  def load_account(cls):
    username, password = None, None
    while not (username, password) in cls.accounts_dict:
      #Getting accounts again if new account is made from another device during this while loop
      cls.get_accounts()
      clear()
      
      username = input(f"{Colours.fg.orange}Username: ")
      password = input(f"{Colours.fg.red}Password: ")
      
      #Exceptions
      if not (username, password) in cls.accounts_dict:
        clear()
        print(f"{Colours.alert('Invalid username or password.')}")
        sleep_and_clear(2)
        
    cls.account = (username, password)
    
    entities.new_player = cls.accounts_dict[cls.account]["Player"]
    objects.PlayerInventory = cls.accounts_dict[cls.account]["PlayerInventory"]

  
  @classmethod
  def save_account(cls):
    #Getting the accounts again because saving may rewrite over new accounts in the file
    cls.get_accounts()
    
    cls.accounts_dict[cls.account] = {}
    cls.accounts_dict[cls.account]["Player"] = entities.new_player
    cls.accounts_dict[cls.account]["PlayerInventory"] = objects.PlayerInventory
    
    with open("accounts.pkl", "wb") as f:
      pickle.dump(cls.accounts_dict, f)
      
  
  @classmethod
  def reset_account(cls):
    clear()
    print(f"{Colours.alert('Your account has now been resetted.')}")
    input(f"{Colours.input_colour}")

    entities.new_player = entities.Player()
    objects.PlayerInventory.remove_item(mode="all")

    cls.save_account()
  