from colours import Colours
from exploration import Combat, Encounters
from items import PlayerInventory, Shop
import objects as o
from setting import Storyline

#temporary
Combat.start_combat(is_players_turn=True)
#brrrrrrrrrrr


# Storyline.play_intro_storyline()

valid_inputs = ("ex", "slep", "trv", "inv", "shp", "art", "help")

#This is a MESS
while o.new_player.is_dead() != True:
  o.display_user_interface()
  player_choice = input(f"{Colours.fg.orange}> ").lower().strip()

  if player_choice == 'ex':
    Combat.start_combat()

  elif player_choice == "slep":
    o.new_player.sleep_for_health()

  elif player_choice == "trv":
    o.new_player.travel()

  elif player_choice == "inv":
    PlayerInventory.display_items_dict(clear_the_screen=True)
    player_choice = input(f"{Colours.fg.orange}> ")

  elif player_choice == "shp":
    Shop.display_shop()

  elif player_choice == "art":
    o.new_player.open_artipedia()

  elif player_choice == "help":
    o.new_player.ask_for_help()

  elif player_choice not in valid_inputs:
    o.clear()
    print(f"{o.Colours.fg.red + o.Colours.underline}INVALID COMMAND, TYPE THE LETTERS IN THE SQUARE BRACKETS.")
    o.sleep_and_clear(2)
    
    
  if o.new_player.is_dead():
    o.new_player.display_death_message()
