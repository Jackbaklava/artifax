from colours import Colours
from exploration import Combat, Encounters
from items import PlayerInventory, Shop
import objects as o
from setting import Storyline

#temporary
Combat.start(is_players_turn=True)
#brrrrrrrrrrrr


# Storyline.play_intro_storyline()

valid_inputs = ('ex', 'sleep', 'travel', 'inv', 'shop', 'art', 'help')

while o.Player.current_health > 0 and o.Player.artifacts_collected != o.Player.total_artifacts:
  o.display_user_interface()
  player_choice = input(f"{Colours.fg.orange}> ").lower().strip()

  if player_choice == 'ex':
    Combat.start()

  elif player_choice == 'sleep':
    o.Player.sleep_for_health()

  elif player_choice == 'travel':
    o.Player.travel()

  elif player_choice == 'inv':
    PlayerInventory.display_items_dict(clear_the_screen=True)
    player_choice = input(f"{Colours.fg.orange}> ")

  elif player_choice == 'shop':
    Shop.display_shop()

  elif player_choice == 'art':
    o.Player.open_artipedia()

  elif player_choice == 'help':
    o.Player.ask_for_help()

  elif player_choice not in valid_inputs:
    o.clear()
    print(f"{o.Colours.fg.red + o.Colours.underline}INVALID COMMAND, TYPE THE LETTERS IN THE SQUARE BRACKETS.")
    o.sleep_and_clear(2)



o.Player.check_for_death()
