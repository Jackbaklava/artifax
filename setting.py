from colours import Colours
from system import clear



class Location:
  def __init__(self, name, colour, line_colour):
    self.name = name
    self.colour = colour
    self.line_colour = line_colour



valley_of_dawn = Location("Valley of Dawn", Colours.fg.cyan, Colours.fg.green + Colours.bg.cyan)

forest_of_fangarr = Location("Forest of Fangarr", Colours.fg.blue, Colours.fg.blue + Colours.bg.green)

wompy_willows = Location("Wompy Willows", forest_of_fangarr.colour, Colours.fg.blue + Colours.bg.green)

iron_mountains = Location("Iron Mountains", Colours.fg.yellow, Colours.fg.yellow + Colours.bg.red)

grimsden = Location("Grimsden", Colours.fg.red, Colours.fg.red + Colours.bg.purple)

all_locations = {"vod" : valley_of_dawn,
                 "fof" : forest_of_fangarr,
                 "ww" : wompy_willows,
                 "im" : iron_mountains,
                 "gd" : grimsden
}



class Artifact:
  def __init__(self, name, location):
    self.name_string = f"{Colours.fg.red}{name}"
    self.location = location
    self.description = f"(Found in {self.location.name})"

  
  def display_artifact(self):
    print(f"{self.name_string} {Colours.fg.green}{self.description} ")


rune_of_daylight = Artifact("Rune of Daylight", valley_of_dawn)
primal_shard = Artifact("Primal Shard", forest_of_fangarr)
tablet_of_destiny = Artifact("Tablet of Destiny", wompy_willows)
azures_gauntlet = Artifact("Azure's Gauntlet", iron_mountains)

all_artifacts = [rune_of_daylight, primal_shard, tablet_of_destiny, azures_gauntlet]



class Character:
  def __init__(self, name_string, name_colour, speech_colour):
    self.name_colour = name_colour + Colours.underline + Colours.bold
    self.name_string = f"{self.name_colour}{name_string}:{Colours.reset}"
    self.speech_colour = speech_colour


  def speak(self, dialogue):
    clear()
    print(f"{self.name_string} {self.speech_colour}{dialogue}" + '\n')
    input(f"{Colours.fg.orange}> ")



you = Character("You", Colours.fg.orange, Colours.fg.lightblue)
old_man = Character("Old Man", Colours.fg.green, Colours.fg.pink)



class Storyline:
  description_colour =  Colours.fg.cyan
  alert_colour = Colours.fg.lightgreen


  @classmethod
  def print_description(cls, description):
    clear()
    print(f"{cls.description_colour}*{description}*" + '\n')
    input(f"{Colours.fg.orange}> ")
    

  @classmethod
  def print_alert(cls, alert):
    clear()
    print(f"{Colours.underline + cls.alert_colour}*{alert.upper()}*{Colours.reset}" + '\n')
    input(f"{Colours.fg.orange}> ")


  @classmethod
  def play_intro_storyline(cls):
    cls.print_description("It's a lazy Sunday evening and you're playing video games on your PS1, when suddenly your game starts to glitch.")

    you.speak("Why is the game not working?")

    cls.print_description("You try fixing the problem by kicking the console.")

    cls.print_alert("zoop")

    cls.print_description("In the blink of an eye, the world fades away before you in a series of sudden flashes. Scared, you closed your eyes.")

    cls.print_description("When you open your eyes again, you seem to be in a land far away from reality.")

    you.speak("Where am I?")

    cls.print_description("You look around and notice an old man coming towards you.")

    old_man.speak("Welcome Player, to the world of Artifax!!!")

    #Handle accounts

    you.speak("Woah! You mean I am in the game itself?! This is so cool!")

    old_man.speak("Slow down, young man. This is unlike any game you might have played.")

    you.speak("So what? I mean I can infinitely respawn. Right?")

    old_man.speak("Nope. You have one life only. And if you die here, you'll die in real life too.")

    you.speak("That sounds scary. So, how do I escape this game?")

    old_man.speak("Obviously you need to beat the game.")

    you.speak("Ah right! That's a piece of cake. But how do I beat the game?")

    old_man.speak("It's simple. You need to save this world from the terror of Talgrog The Giant. However, if you try to defeat him in this world, you'll hardly make a scratch on him. Thus, you need to travel to the deadly plains of Grimsden and behead the beast before it leaves it's den.")

    you.speak("And how do I travel to Grimsden?")

    old_man.speak("Since Grimsden is located in the far corner of the universe, you can't travel there by foot. So, you first need to collect the 3 Artifacts of Power and make a portal to Grimsden. You can collect these artifacts by defeating the Artifact Keeper of every location you explore.")

    you.speak("Woah! That's alot of stuff to do.")

    old_man.speak("Don't worry. To help you track your progress, I am giving you an Artipedia. In case you ever need my help, type 'help' in the main menu. Start your journey by exploring the wilderness. ")

    old_man.speak("Now go out there and save the world!!!")
