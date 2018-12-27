from sqlalchemy import create_engine
import os 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session,relationship
import enemies
import heroes
import weapons

def CreateSession():
        mydir=os.path.dirname(os.path.abspath(__file__))
        engine = create_engine(f"sqlite:///{os.path.join(mydir,'combatTracker.db')}")#,echo=True)
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        return Session()

Base = declarative_base()


#may have to change the name of this class to avoid import errors against enemies.py
class Enemy(Base):
    __tablename__ = 'enemies'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    size = Column(String)
    type = Column(String)
    alignment = Column(String)
    ac = Column(Integer)
    armorType = Column(String)
    hp = Column(String)
    speed = Column(String)
    STR = Column(Integer)
    DEX = Column(Integer)
    CON = Column(Integer)
    INT = Column(Integer)
    WIS = Column(Integer)
    CHA = Column(Integer)
    weapons=relationship('Weapon')
    savingThrows=relationship('SavingThrows')
    challenge = Column(String)
    senses = Column(String) #list?
    languages = Column(String) #list?

    def __repr__(self):
        return self.name

class SavingThrows(Base):
    __tablename__ = 'savingThrows'
    __table_args__ = {'sqlite_autoincrement': True}
    savingThrowid = Column(Integer, primary_key=True)
    enemyid = Column(Integer, ForeignKey('enemies.id'))
    STR = Column(String)
    DEX = Column(String)
    CON = Column(String)
    INT = Column(String)
    WIS = Column(String)
    CHA = Column(String)
    #enemy=relationship("Enemy", back_populates="savingThrows")

class DamageTypes(Base):
    __tablename__ = 'damageTypes'
    __table_args__ = {'sqlite_autoincrement': True}
    damageTypeid = Column(Integer, primary_key=True)
    damageName=Column(String)

class DamageResistance(Base):
    __tablename__ = 'damageResistance'
    __table_args__ = {'sqlite_autoincrement': True}
    damageid = Column(Integer, primary_key=True)
    enemyid = Column(Integer, ForeignKey('enemies.id'))
    damageTypeid=Column(Integer)
    immune=Column(Integer)
    resistant=Column(Integer)
    vulnerable=Column(Integer)

class ConditionTypes(Base):
    __tablename__ = 'conditionTypes'
    __table_args__ = {'sqlite_autoincrement': True}
    conditionTypeid = Column(Integer, primary_key=True)
    conditionName=Column(String)

class ConditionImmunities(Base):
    __tablename__ = 'conditionImmunities'
    __table_args__ = {'sqlite_autoincrement': True}
    conditionid = Column(Integer, primary_key=True)
    enemyid = Column(Integer, ForeignKey('enemies.id'))
    conditionTypeid=Column(Integer)
    immune=Column(Integer)

class Hero(Base):
    __tablename__ = 'heros'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ac = Column(Integer)
    hp = Column(Integer)

    def __repr__(self):
        return self.name

class Weapon(Base):
    __tablename__ = 'weapons'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    enemyid=Column(Integer, ForeignKey('enemies.id'))
    name = Column(String)
    type = Column(String)
    attackBonus = Column(String)
    range = Column(String)
    targetMax = Column(Integer)
    damage = Column(String)
    damageType = Column(String)

    def __repr__(self):
        return self.name

class Combat(Base):
    __tablename__ = 'combat'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    enemyid=Column(Integer, ForeignKey('enemies.id'))
    enemyName = Column(String)
    initiativeScore = Column(Integer)
    currentHp = Column(Integer)
    maxHp = Column(Integer)
    AC = Column(Integer)
    hadTurn= Column(Integer)

    def __repr__(self):
        return self.enemyName


def CreateDbAndPopulate():
    session = CreateSession()
    goblin=Enemy(name='Goblin',size='Small',type='Humanoid(Goblinoid)',alignment='neutral evil',ac=15,hp='2d6',speed='30ft.',STR=8,DEX=14,CON=10,INT=10,WIS=8,CHA=8)
    bandit=Enemy(name='Bandit',size='Medium',type='Humanoid(any race)',alignment='any non-lawful alignment',ac=12,hp='2d8+2',speed='30ft.',STR=11,DEX=12,CON=12,INT=10,WIS=10,CHA=10)
    dragon=Enemy(name='Adult Red Dragon',size='Huge',type='Dragon',alignment='chaotic evil',ac=19,hp='19d12+133',speed='40ft., climb 40ft., fly 80ft.',STR=27,DEX=10,CON=25,INT=16,WIS=13,CHA=21)
    drow=Enemy(name='Drow',size='Medium',type='Humanoid(Elf)',alignment='neutral evil',ac=15,hp='3d8',speed='30ft.',STR=10,DEX=14,CON=10,INT=11,WIS=11,CHA=12)

    badguys=[goblin,bandit,dragon,drow]

    for i in badguys:
        x = session.query(Enemy).filter_by(name=i.name).first()
        if not x:
                session.add(i)

    session.add(Weapon(enemyid=1,name='Scimitar',type='Melee',attackBonus='+4',range='5ft.',targetMax=1,damage='1d6+2',damageType='Slashing'))
    session.add(Weapon(enemyid=1,name='Shortbow',type='Ranged',attackBonus='+4',range='80/320ft.',targetMax=1,damage='1d6+2',damageType='Piercing'))
    session.add(Weapon(enemyid=2,name='Scimitar',type='Melee',attackBonus='+3',range='5ft.',targetMax=1,damage='1d6+1',damageType='Slashing'))
    session.add(Weapon(enemyid=2,name='Light Crossbow',type='Ranged',attackBonus='+3',range='80/320ft.',targetMax=1,damage='1d8+1',damageType='Piercing'))
    session.add(Weapon(enemyid=3,name='Bite',type='Melee',attackBonus='+14',range='10ft.',targetMax=1,damage='2d10+8',damageType='Piercing')) #also has a secondary damage type, 2d6 fire. how best to show this?
    session.add(Weapon(enemyid=3,name='Claw',type='Melee',attackBonus='+14',range='5ft.',targetMax=1,damage='2d6+8',damageType='Slashing'))
    session.add(Weapon(enemyid=3,name='Tail',type='Melee',attackBonus='+14',range='15ft.',targetMax=1,damage='2d8+8',damageType='Bludgeoning'))
    session.add(Weapon(enemyid=4,name='Shortsword',type='Melee',attackBonus='+4',range='5ft.',targetMax=1,damage='1d6+2',damageType='Piercing'))
    session.add(Weapon(enemyid=4,name='Hand Crossbow',type='Ranged',attackBonus='+4',range='30/120ft.',targetMax=1,damage='1d6+2',damageType='Piercing')) #this one has more effects if it hits, need to think of how to show this.
    session.add(Hero(name = 'Beardor',ac = 18,hp = 25))    
    session.add(Hero(name = 'James Brown',ac = 17,hp = 23))
    session.add(Hero(name = 'Bonk',ac = 12,hp = 16))
    session.add(SavingThrows(enemyid=3,DEX='+6',CON='+13',WIS='+7',CHA='+5'))
    session.commit()
    session.close()

        #below is all well and good but can I just pass a dict to it? probably better to be verbose for the time being.
def createEnemyInstance(enemyName):
    session = CreateSession()
    Badguy = session.query(Enemy).filter_by(name=enemyName).first()
    BadguysWeapons = session.query(Weapon).filter_by(enemyid=Badguy.id).all()
    BadguysWeapons = [{'name':i.name,'type':i.type,'attackBonus':i.attackBonus,'range':i.range,'targetMax':i.targetMax,'damage':i.damage,'damageType':i.damageType} for i in BadguysWeapons]
    EnemyInstance =enemies.Enemy(Badguy.name,Badguy.size,Badguy.type,Badguy.alignment,Badguy.ac,Badguy.hp,Badguy.speed,Badguy.STR,Badguy.DEX,Badguy.CON,Badguy.INT,Badguy.WIS,Badguy.CON,weapons=BadguysWeapons,enemyId=Badguy.id)
    return EnemyInstance

def createHeroInstance(heroName):
    session = CreateSession()
    Goodguy = session.query(Hero).filter_by(name=heroName).first()
    HeroInstance =heroes.Hero(Goodguy.name,Goodguy.hp,Goodguy.ac)
    return HeroInstance

def referenceEnemyInstance(enemyInstance): #this function gets passed a models.Combat row object
    session = CreateSession()
    Badguy = session.query(Enemy).filter_by(id=enemyInstance.enemyid).first()
    BadguysWeapons = session.query(Weapon).filter_by(enemyid=Badguy.id).all()
    BadguysWeapons = [{'name':i.name,'type':i.type,'attackBonus':i.attackBonus,'range':i.range,'targetMax':i.targetMax,'damage':i.damage,'damageType':i.damageType} for i in BadguysWeapons]
    EnemyInstance =enemies.InitialisedEnemy(enemyInstance.enemyName,Badguy.size,Badguy.type,Badguy.alignment,enemyInstance.AC,enemyInstance.currentHp,Badguy.speed,Badguy.STR,Badguy.DEX,Badguy.CON,Badguy.INT,Badguy.WIS,Badguy.CON,weapons=BadguysWeapons,initiative=enemyInstance.initiativeScore,enemyId=Badguy.id,combatId=enemyInstance.id)
    return EnemyInstance

def referenceEnemyInstanceByName(enemyCombatId): #this function just gets a string passed to it
    session = CreateSession()
    Badguy = session.query(Combat).filter_by(id=enemyCombatId).first()
    BadguysStats = session.query(Enemy).filter_by(id=Badguy.enemyid).first()
    BadguysWeapons = session.query(Weapon).filter_by(enemyid=Badguy.enemyid).all()
    BadguysWeapons = [{'name':i.name,'type':i.type,'attackBonus':i.attackBonus,'range':i.range,'targetMax':i.targetMax,'damage':i.damage,'damageType':i.damageType} for i in BadguysWeapons]
    EnemyInstance =enemies.InitialisedEnemy(Badguy.enemyName,BadguysStats.size,BadguysStats.type,BadguysStats.alignment,Badguy.AC,Badguy.currentHp,BadguysStats.speed,BadguysStats.STR,BadguysStats.DEX,BadguysStats.CON,BadguysStats.INT,BadguysStats.WIS,BadguysStats.CON,weapons=BadguysWeapons,initiative=Badguy.initiativeScore,enemyId=Badguy.id,combatId=enemyCombatId)
    return EnemyInstance

def markTurn(enemy): #need to sort out names of 
    session = CreateSession()
    x=session.query(Combat).filter_by(enemyName=enemy.enemyName).first()
    x.hadTurn =1
    session.commit()

def removeEnemy(enemy):
    session = CreateSession()
    session.query(Combat).filter_by(enemyName=enemy).delete() #possibly better to use id? not sure atm
    session.commit()

def getCombatOrder():
    session = CreateSession()
    results = session.query(Combat).order_by(Combat.initiativeScore.desc()).all()
    return results

def getNextTurn():
    session = CreateSession()
    results = session.query(Combat).filter(Combat.hadTurn == None).order_by(Combat.initiativeScore.desc()).first()
    if not results:
        for row in session.query(Combat).all():  # all() is extra
            row.hadTurn = None
        session.commit()
        results = session.query(Combat).filter(Combat.hadTurn == None).order_by(Combat.initiativeScore.desc()).first()
    return results #Combat.Row entry

def updateHP(enemy,hp):
    session = CreateSession()
    results = session.query(Combat).filter(Combat.enemyName == enemy).first()
    results.currentHp = hp
    session.commit()

def generateEnemiesList():
    session = CreateSession()
    results = session.query(Enemy).all()
    results.sort(key=lambda x: x.name)
    return results

def generateHeroesList():
    session = CreateSession()
    results = session.query(Hero).all()
    results.sort(key=lambda x: x.name)
    return results

def truncateCombatList():
    session = CreateSession()
    session.execute('''delete from combat''')
    session.commit()
    session.close()

def addToCombatTable(enemy): #need to sort out names of 
    session = CreateSession()
    try:
        x=session.query(Enemy).filter_by(id=enemy.enemyId).first()
        dupeCheck=session.query(Combat).filter_by(enemyid=enemy.enemyId).count()
        session.add(Combat(enemyid=x.id,enemyName=f"{enemy.name} {str(dupeCheck +1)}",initiativeScore=enemy.initiative,currentHp=enemy.hp,AC=enemy.AC,maxHp=enemy.hp))
        session.commit()
    except AttributeError:
        session.add(Combat(enemyName=f"{enemy.name}",initiativeScore=enemy.initiative,currentHp=enemy.hp,AC=enemy.AC,maxHp=enemy.hp))
        session.commit()


#join examples
# session = CreateSession()
# x = session.query(Enemy,SavingThrows).filter(Enemy.id==SavingThrows.enemyid).filter(Enemy.name=='Adult Red Dragon').all()
# x = session.query(Enemy).join(SavingThrows).filter(Enemy.name=='Adult Red Dragon').first()
# print(x.savingThrows[0].__dict__)