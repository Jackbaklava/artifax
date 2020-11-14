from colours import Colours
import objects as o
import os
from time import sleep


def clear():
  os.system('clear')


def sleep_and_clear(seconds=1):
  sleep(seconds)
  clear()


def calculate_percentage(percentage, current=None, total=None):
  if current == None:
    res = total * percentage / 100
  else:
    res = current * 100 / percentage
    
  return res


def remove_unwanted_chars(string_to_clean, unwanted_chars=('.', '_'), replace_with=' '):
  res = string_to_clean
  
  for char in unwanted_chars:
    if char in string_to_clean:
      res = res.replace(char, replace_with)
      
  return res


print_one_liner = lambda string: print(string * 130)


line_break = lambda: f'{o.Player.current_location.line_colour}{"_" * 130}{Colours.reset}'


def print_heading(title):
  print(f"""{line_break()}{Colours.fg.orange + Colours.bold}

  {title.center(130) + Colours.reset}

{line_break()}
""")
