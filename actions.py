from diceroll import RollDice

class Action:
    def __init__(self,**actions):
        self.actionName = actions['name']
        self.attackBonus = actions['attackBonus']
        self.targetMax = actions['targetMax']
        self.damage = actions['damage']
        self.damageType = actions['damageType']