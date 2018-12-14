from diceroll import RollDice

class Enemy:
    _all = set()
    def __init__(self...):
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

        self.initiative = RollDice('1d20') + (dex-10) / 2
        self.max = self.hp
        
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