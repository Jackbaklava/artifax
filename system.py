from colours import Colours
import entities
import os
from time import sleep


class System:
    @staticmethod
    def calculate_percentage(percentage, current=None, total=None):
        if current == None:
            res = total * percentage / 100
        else:
            res = current * 100 / percentage

        return res

    @staticmethod
    def remove_unwanted_chars(
        string_to_clean, unwanted_chars=(".", "_"), replace_with=" "
    ):
        res = string_to_clean

        for char in unwanted_chars:
            if char in string_to_clean:
                res = res.replace(char, replace_with)

        return res

    @staticmethod
    def get_object(string, dictionary):
        res = list(filter(lambda obj: obj.name == string, dictionary.values()))[0]

        return res

    print_one_liner = lambda string: print(string * 130)

    line_break = (
        lambda: f'{entities.new_player.current_location.line_colour}{"_" * 130}{Colours.reset}'
    )

    indent = lambda text: " " * len(list(str(text))) + "   "

    @classmethod
    def print_title(cls, title):
        print(
            f"""{cls.line_break()}{Colours.fg.orange + Colours.bold}

  {title.center(130) + Colours.reset}

{cls.line_break()}
"""
        )


def clear():
    os.system("clear")


def sleep_and_clear(seconds=1):
    sleep(seconds)
    clear()
