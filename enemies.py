from diceroll import RollDice
from weapons import Weapon,Weapons,Weapons2

class Enemy:
    def __init__(self,name,size,type,alignment,AC,hp,speed,STR,DEX,CON,INT,WIS,CHA,weapons):
        self.name = name
        self.size = size
        self.type = type
        self.alignment = alignment
        self.AC = AC
        self.hp = RollDice(hp)
        self.speed = speed
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.initiative = int(RollDice('1d20') + (self.DEX-10) / 2)
        self.max = self.hp
        self.alive = True
        self.currentstatus = 'Healthy'
        self.weapons = [Weapon(**i) for i in weapons]
        
    def Attack(self, weapon, target):
        if self.alive:
            aRoll = RollDice('1d20'+ weapon.attackBonus)
            print ('Attack Roll: ' + str(aRoll) )
            if aRoll > target.AC:
                damageDone = RollDice(weapon.damage)
                print ('The ' + self.name + ' attacks with it''s ' + weapon.name + ' and does ' + str(damageDone) + ' ' + weapon.damageType + ' damage.')
                target.Damage(damageDone)
                if type(target) is Enemy:
                    target.Status()
            else:
                print ('The ' + self.name +  "'s attack misses!")

    def Damage(self,amount):
        self.hp = self.hp - amount
        print (self.name + ' has ' + str(self.hp) + ' hp remaining.')   
 
    def Status (self):
        currenthp = self.hp
        if currenthp <= 0:
            print (self.name + ' is dead.')
            self.IsDead = True
            self.currentstatus = 'Dead'
        elif currenthp <= (self.max / 2):
            print (self.name + ' is bloodied.')
            self.currentstatus = 'Bloodied'
        elif currenthp > (self.max / 2):
            print (self.name + ' is ok.')
            
    def CurrentWeapon(self, weaponDict):
        self.cWeapon = weaponDict

    def UpdateHP(self, newHP):
        self.hp = newHP


Goblin1=Enemy('goblin1','small','humanoid(goblinoid)','neutral evil',15,'2d6','30ft.',8,14,10,10,8,8,weapons=Weapons)
Goblin2=Enemy('goblin2','small','humanoid(goblinoid)','neutral evil',15,'2d6','30ft.',8,14,10,10,8,8,weapons=Weapons)
Goblin3=Enemy('goblin3','small','humanoid(goblinoid)','neutral evil',15,'2d6','30ft.',8,14,10,10,8,8,weapons=Weapons2)