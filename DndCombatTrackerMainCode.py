from diceroll import RollDice
import operator
import pandas

class Enemy:
    _all = set()
    def __init__(self, name, hp, dex, AC, type, Weapons):
        self.name = name
        self.type = type
        self.hp = RollDice(hp)
        self.dex = dex
        self.initiative = RollDice('1d20') + (dex-10) / 2
        self.max = self.hp
        self.AC = AC
        self.IsDead = False
        self.currentstatus = 'Ok'
        self.weapons = Weapons
        self.__class__._all.add(self)        
    
    def DisplayStats(self):
        if not self.IsDead:
            print "Name : ", self.name
            print "max hp: ", self.max 
            print "current hp: ", self.hp
            print "Initiative: ", self.initiative
            print "Armor Class :" + str(self.AC)
        else:
            print self.name + ' is dead'
            #print "Weapon: ", self.weapon.wName.title()
        
    def Damage(self,amount):
        self.hp = self.hp - amount
        print 'The ' + self.name + ' has ' + str(self.hp) + ' hp remaining.'
        
    def Attack(self, weapon, target):
        if not self.IsDead:
            aRoll = RollDice('1d20')
            print 'Attack Roll: ' + str(aRoll)
            if aRoll > target.AC:
                print 'The ' + self.name + ' attacks with it''s ' + weapon.wName + ' and does ' + str(weapon.dmg) + ' ' + weapon.dType + ' damage.'
                target.Damage(weapon.dmg)
                if type(target) is Enemy:
                    target.Status()
            else:
                print 'The ' + self.name +  "'s attack misses!"
         
    def Status (self):
        currenthp = self.hp
        if currenthp <= 0:
            print self.name + ' is dead.'
            self.IsDead = True
            self.currentstatus = 'Dead'
        elif currenthp <= (self.max / 2):
            print self.name + ' is bloodied.'
            self.currentstatus = 'Bloodied'
        elif currenthp > (self.max / 2):
            print self.name + ' is ok.'
            
    def CurrentWeapon(self, weaponDict):
        self.cWeapon = weaponDict
            
class Hero:
    _all = set()
    def __init__(self, name, hp, dex, AC):
        self.name = name
        self.hp = hp
        self.max = self.hp
        self.AC = AC
        self.dex = dex
        self.__class__._all.add(self) 
    
    def DisplayStats(self):
            print "Name : ", self.name
            print "max hp: ", self.max 
            print "current hp: ", self.hp
            
    def Damage(self,amount):
        self.hp = self.hp - amount
        print self.name + ' has ' + str(self.hp) + ' hp remaining.'
        
    def SetInit(self,Initiative):
        self.initiative = Initiative + self.dex


class Weapon:
    def __init__(self, wName, aMod, dmg, dType):
        self.wName = wName
        self.aMod = aMod
        self.dmg = 10 #RollDice(str(dmg))
        self.dType = dType

Weapons =   {1:{'wName':'sword','damage':'1d6','dType':'slashing'},
             2:{'wName':'shortbow','damage':'1d6','dType':'piercing'},
            3:{'wName':'greatsword','damage':'2d8','dType':'slashing'}}

#CurrentWeapon = Weapon(**Weapons[1])

def CreateEnemyList(EnemyName, amount=1):
    for x in range(amount):
        e = CreateEnemyDict(EnemyName)
        e['type'] = e['name']
        e['name'] = e['name'] + ' ' + str(x + 1)
        Enemy(**e)

def CreateEnemyDict(EnemyName):
    df = pandas.read_excel("C:\Users\Turner_prize\Desktop\DnDEnemies2.xlsm")
    dfx=df.set_index('EName')
    dfx = dfx.transpose()
    EnemyList = dfx.to_dict()    
    wList = EnemyList[EnemyName]['Weapon'].split(';')
    Weapons = {}
    for i, w in enumerate(wList, start=1):
        W = w.split(',')  
        MyWeapon = List2Dict(*W)
        Weapons['Weapon' + str(i)] = MyWeapon
    del EnemyList[EnemyName]['Weapon']
    EnemyList[EnemyName]['Weapons'] = Weapons
    return EnemyList[EnemyName]

#Creates a list object of all Hero and Enemy class instances and places them into a list, sorted by Initiative (and then dex) for use in combat.
def SortInitiative():
    CombatList = []

    for x in Enemy._all:
        CombatList.append(x)
        
    for x in Hero._all:
        CombatList.append(x)
    
    CombatList.sort(key=operator.attrgetter('initiative','dex'),reverse=True)
    for c in CombatList:
        print c.name + ' ' +str(c.initiative)
    return CombatList
    
def List2Dict(wn,am,dm, dt):
    x = {}
    x['wName'] = wn
    x['aMod'] = am
    x['dmg'] = dm
    x['dType'] = dt    
    return x    

#--------------------------Functions above, code below

Beardor = {'name':'Beardor','hp':50,'dex':2,'AC':10}
  
Hero1 = Hero(**Beardor)

CreateEnemyList('Goblin',6)
CreateEnemyList('Ogre')
Hero1.SetInit(10)
x = iter(SortInitiative())


#Can return name of weapon below. I can use this to backtrack to the relevent dictionary name, and use that to activate the weapon class / attack functions
#for x in Enemy._all:
#        for i in x.weapons:
            #print x.name
            #print x.weapons[i].get('wName')


print " " 

for i in range(3):
    MyTestName = next(iter(x))
    print MyTestName.name
    CurrentWeapon = Weapon(**MyTestName.weapons['Weapon1'])
    MyTestName.Attack(CurrentWeapon,Hero1)
    print " " 
    print MyTestName.Status()
#next(iter(G)).Attack(Weapon(**weapons['Weapon2']),Hero1)
