from diceroll import RollDice
from actions import Action
import models

class Enemy(object):
    def __init__(self,**enemy):
        self.name = enemy['name']
        self.size = enemy['size']
        self.type = enemy['type']
        self.alignment = enemy['alignment']
        self.AC = enemy['ac']
        self.armorType = enemy['armorType']
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
        self.savingThrows = enemy.get('savingThrows',None)
        self.challenge = enemy['challenge']
        self.languages= enemy['languages']
        self.senses= enemy['senses']
        self.damage_vulnerabilities= enemy['damage_vulnerabilities']
        self.damage_resistances= enemy['damage_resistances']
        self.damage_immunities= enemy['damage_immunities']
        self.condition_immunities= enemy['condition_immunities']
        if enemy.get('specialTraits',None):
            self.specialTraits = [SpecialTraits(**i) for i in enemy['specialTraits']]
        self.actionsText = [ActionsText(**i) for i in enemy['actionsText']]
        
        
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

    def Damage(self,amount): #need to write damage to db here?
        self.hp = self.hp - amount
        models.updateHP(self.name,self.hp)
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
    def __init__(self,**enemy):
        self.name = enemy['name']
        self.size = enemy['size']
        self.type = enemy['type']
        self.alignment = enemy['alignment']
        self.AC = enemy['ac']
        self.armorType = enemy['armorType']
        self.hp = enemy['hp']
        self.STR = enemy['STR']
        self.DEX = enemy['DEX']
        self.CON = enemy['CON']
        self.INT = enemy['INT']
        self.WIS = enemy['WIS']
        self.CHA = enemy['CHA']
        self.initiative = enemy['initiative']
        self.alive = True
        self.currentstatus = 'Healthy'
        self.actions = [Action(**i) for i in enemy['actions']]
        self.max = enemy['maxhp']
        self.enemyId = enemy['enemyId']
        self.combatId = enemy['combatId']
        self.savingThrows = enemy.get('savingThrows',None)
        self.challenge = enemy['challenge']
        self.languages= enemy['languages']
        self.senses= enemy['senses']
        self.bloodied= enemy['bloodied']
        self.damage_vulnerabilities= enemy['damage_vulnerabilities']
        self.damage_resistances= enemy['damage_resistances']
        self.damage_immunities= enemy['damage_immunities']
        self.condition_immunities= enemy['condition_immunities']
        if enemy.get('specialTraits',None):
            self.specialTraits = [SpecialTraits(**i) for i in enemy['specialTraits']]
        self.actionsText = [ActionsText(**i) for i in enemy['actionsText']]

class SpecialTraits(object):
    def __init__(self,**st):
        self.title = st['title']
        self.description = st['description']

class ActionsText(object):
    def __init__(self,**st):
        self.title = st['title']
        self.actionType = st.get('actionType',None)
        self.description = st['description']