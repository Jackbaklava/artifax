from colours import Colours
from exploration import Combat, Encounters
from objects import PlayerInventory, Shop
import entities as e
from setting import Storyline

#temporary
Combat.start_combat(is_players_turn=True)
#brrrrrrrrrrr


# Storyline.play_intro_storyline()

valid_inputs = ("ex", "slep", "trv", "inv", "shp", "art", "help")

#This is a MESS
while e.new_player.is_dead() != True:
  e.display_user_interface()
  player_choice = input(f"{Colours.fg.orange}> ").lower().strip()

  if player_choice == 'ex':
    Combat.start_combat()

  elif player_choice == "slep":
    e.new_player.sleep_for_health()

  elif player_choice == "trv":
    e.new_player.travel()

  elif player_choice == "inv":
    PlayerInventory.display_items_dict(clear_the_screen=True)
    player_choice = input(f"{Colours.fg.orange}> ")

  elif player_choice == "shp":
    Shop.display_shop()

  elif player_choice == "art":
    e.new_player.open_artipedia()

  elif player_choice == "help":
    e.new_player.ask_for_help()

  elif player_choice not in valid_inputs:
    e.clear()
    print(f"{e.Colours.fg.red + e.Colours.underline}INVALID COMMAND, TYPE THE LETTERS IN THE SQUARE BRACKETS.")
    e.sleep_and_clear(2)
    
    
  if e.new_player.is_dead():
    e.new_player.display_death_message()
