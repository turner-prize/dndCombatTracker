from diceroll import RollDice

class Weapon:
    def __init__(self,name,type,attackBonus,range,targetMax,damage,damageType):
        self.name = name
        self.type = type
        self.attackBonus = attackBonus
        self.range = range
        self.targetMax = targetMax
        self.damage = damage
        self.damageType = damageType
