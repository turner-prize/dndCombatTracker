from diceroll import RollDice

class Action:
    def __init__(self,**actions):
        self.actionName = actions['name']
        self.type = actions['type']
        self.attackBonus = actions['attackBonus']
        self.range = actions['range']
        self.targetMax = actions['targetMax']
        self.damage = actions['damage']
        self.damageType = actions['damageType']