import pandas

def List2Dict(wn,am,dm, dt):
    x = {}
    x['wName'] = wn
    x['aMod'] = am
    x['dmg'] = dm
    x['dType'] = dt    
    return x    

class Weapon:
    def __init__(self, wName,attackbonus, damage,dType):
        self.wName = wName
        self.attackbonus = attackbonus
        self.damage = damage #RollDice(damage)
        self.dType = dType


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
    print EnemyList[EnemyName]
    
  
    
    
    
#OLD VERSION OF CREATEENEMYDICT
#def CreateEnemyDict(EnemyName):
#    df = pandas.read_excel("C:\Users\Turner_prize\Desktop\DnDEnemies2.xlsm")
#    dfx=df.set_index('EName')
#    dfx = dfx.transpose()
#    EnemyList = dfx.to_dict()    
#    return EnemyList[EnemyName]
    
#below print the attribules for each player. in this case it prints their ID code and their name
#for players in range(len(data)):
#    print str(data[players]['id']) +": " + data[players]["web_name"]
   
#below will just print the keys in the dictionary.
#for k in data[0]:
#    print k 
    
#below will just print the values in the dictionary.
#for k in data[0]:
#    print data[0].get(k)  

#below will print both keys and values in each dictionary
#for k,v in data[0].iteritems():
#    print str(k) + " : "  + str(v)
