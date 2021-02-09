
#import game
#game.GameState.delete_all_accounts()


from game import Game
from setting import Storyline

# Game.display_screen_alert()

Storyline.play_introduction()

Game.play()
