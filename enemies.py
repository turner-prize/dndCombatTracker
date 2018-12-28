from diceroll import RollDice
from actions import Action
#import models

class Enemy(object):
    def __init__(self,**enemy):
        self.name = enemy['name']
        self.size = enemy['size']
        self.type = enemy['type']
        self.alignment = enemy['alignment']
        self.AC = enemy['ac']
        self.hp = RollDice(enemy['hp'])
        self.speed = enemy['speed']
        self.STR = enemy['STR']
        self.DEX = enemy['DEX']
        self.CON = enemy['CON']
        self.INT = enemy['INT']
        self.WIS = enemy['WIS']
        self.CHA = enemy['CHA']
        self.initiative = int(RollDice('1d20') + (self.DEX-10) / 2)
        self.max = self.hp
        self.alive = True
        self.currentstatus = 'Healthy'
        self.actions = [Action(**i) for i in enemy['actions']]
        self.enemyId = enemy['id'] 
        
        
    def Attack(self, action, target):
        if self.alive:
            aRoll = RollDice('1d20'+ action.attackBonus)
            print ('Attack Roll: ' + str(aRoll) )
            if aRoll > target.AC:
                damageDone = RollDice(action.damage)
                print ('The ' + self.name + ' attacks with it''s ' + action.actionName + ' and does ' + str(damageDone) + ' ' + action.damageType + ' damage.')
                target.Damage(damageDone)
                if type(target) is Enemy or type(target) is InitialisedEnemy:
                    target.Status()
                return 'The ' + self.name + ' attacks with it''s ' + action.actionName + ' and does ' + str(damageDone) + ' ' + action.damageType + ' damage.'
            else:
                print ('The ' + self.name +  "'s attack misses!")
                return ('The ' + self.name +  "'s attack misses!")

    def Damage(self,amount):
        self.hp = self.hp - amount
        print (self.name + ' has ' + str(self.hp) + ' hp remaining.')   
 
    def Status (self):
        currenthp = self.hp
        models.updateHP(self.name,currenthp)
        if currenthp <= 0:
            print (self.name + ' is dead.')
            self.IsDead = True
            self.currentstatus = 'Dead'
            models.removeEnemy(self.name)
        elif currenthp <= (self.max / 2):
            print (self.name + ' is bloodied.')
            self.currentstatus = 'Bloodied'
        elif currenthp > (self.max / 2):
            print (self.name + ' is ok.')
            
    def CurrentAction(self, actionDict):
        self.cAction = actionDict

    def UpdateHP(self, newHP):
        self.hp = newHP


class InitialisedEnemy(Enemy):
    def __init__(self,name,size,type,alignment,AC,hp,speed,STR,DEX,CON,INT,WIS,CHA,actions,initiative,enemyId, combatId):
        self.name = name
        self.size = size
        self.type = type
        self.alignment = alignment
        self.AC = AC
        self.hp = hp
        self.speed = speed
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.initiative = initiative
        self.alive = True
        self.currentstatus = 'Healthy'
        self.actions = [Action(**i) for i in actions]
        self.max = self.hp
        self.enemyId = enemyId
        self.combatId = combatId