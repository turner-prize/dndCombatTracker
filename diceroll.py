import re
import random
import operator

def RollDice(Dice):
    ops = { "+": operator.add, "-": operator.sub } 
    die = re.search(r'(\d{0,2})d(\d{1,3})(\+|\-)?(\d{1,3})?',Dice)
    x = sum([random.randint(1, int(die.group(2))) for i in range(int(die.group(1)))])
    if die.group(3):
        x = ops[die.group(3)](x,int(die.group(4)))
    return x