"""
import pickle
with open("accounts.pkl", "wb") as f:
  pickle.dump({(None, None) : None}, f)
int("j")
"""
  
from game import Game
from setting import Storyline

Storyline.play_introduction()

Game.play()
