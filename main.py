
#import game
#game.GameState.delete_all_accounts()


from game import Game
from setting import Storyline

Storyline.play_introduction()

Game.play()
