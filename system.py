from colours import Colours
import objects as o
import os
from time import sleep


def clear():
  os.system('clear')


def sleep_and_clear(seconds=1):
  sleep(seconds)
  clear()

#Need to fix this mess
# def check_for_vowel(string_to_check):
#   vowels = ('a', 'e', 'i', 'o', 'u')
#   res = 'a'

#   if string_to_check[0] in vowels:
#     res += 'n'
    
#   res += ' '
#   return res + string_to_check


print_one_liner = lambda string: print(string * 130)


line_break = lambda: f'{o.Player.current_location.line_colour}{"_" * 130}{Colours.reset}'


def print_heading(title):
  print(f"""{line_break()}{Colours.fg.orange + Colours.bold}

  {title.center(130) + Colours.reset}

{line_break()}
""")
