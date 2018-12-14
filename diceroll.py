import re
import random
import operator

def Roll(x,y):
    Roll = 0
    for i in range(int(x)):
        Roll = Roll + random.randint(1, int(y))
    return Roll

def RollDice(Dice):
    ops = { "+": operator.add, "-": operator.sub } 
    die = re.search(r'(\d{1,2})d(\d{1,3})(\+|\-)?(\d{1,3})?',Dice)
    x = Roll(die.group(1),die.group(2))
    if die.group(3):
        opr= die.group(3)
        Mod = die.group(4)
        x = ops[opr](x,int(Mod))
    return x