class Hero:
    def __init__(self, name, hp, AC):
        self.name = name
        self.hp = hp
        self.max = self.hp
        self.AC = AC
               
    def Damage(self,amount):
        self.hp = self.hp - amount
        print (self.name + ' has ' + str(self.hp) + ' hp remaining.')
        
    def SetInit(self,Initiative):
        self.initiative = Initiative