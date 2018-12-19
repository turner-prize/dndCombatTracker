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



Weapons =   [{'name':'Scimitar','type':'Melee','attackBonus':'+4','range':'5 ft.','targetMax':1,'damage':'1d6+2','damageType':'slashing'}]

Weapons2 =   [{'name':'Bigger Scimitar','type':'Melee','attackBonus':'+4','range':'5 ft.','targetMax':1,'damage':'1d6+2','damageType':'slashing'},
             {'name':'Bigger Shortbow','type':'Ranged','attackBonus':'+4','range':'80/320 ft.','targetMax':1,'damage':'1d6+2','damageType':'peircing'}]