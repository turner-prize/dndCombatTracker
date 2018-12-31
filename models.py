import os 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, ForeignKey,create_engine
from sqlalchemy.orm import sessionmaker, Session,relationship
import enemies
import heroes
import actions

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
    savingThrows=relationship('SavingThrows')
    challenge = Column(String)
    senses = Column(String) #list?
    languages = Column(String) #list?
    legendaryActionsOverview = Column(String)
    actions=relationship('Action')
    specialTraits=relationship('SpecialTraits')
    
    def __repr__(self):
        return self.name

class SpecialTraits(Base):
    __tablename__ = 'specialTraits'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    enemyid = Column(Integer, ForeignKey('enemies.id'))
    title = Column(String)
    description = Column(String)

class ActionsText(Base):
    __tablename__ = 'actionsText'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    enemyid = Column(Integer, ForeignKey('enemies.id'))
    title = Column(String)
    actionType=Column(String)
    description = Column(String)

class SavingThrows(Base):
    __tablename__ = 'savingThrows'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    enemyid = Column(Integer, ForeignKey('enemies.id'))
    STR = Column(String)
    DEX = Column(String)
    CON = Column(String)
    INT = Column(String)
    WIS = Column(String)
    CHA = Column(String)
    #enemy=relationship("Enemy", back_populates="savingThrows")

class DamageResistance(Base):
    __tablename__ = 'damageResistance'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    enemyid = Column(Integer, ForeignKey('enemies.id'))
    damageName=Column(String)
    immune=Column(Integer)
    resistant=Column(Integer)
    vulnerable=Column(Integer)

class ConditionImmunities(Base):
    __tablename__ = 'conditionImmunities'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    enemyid = Column(Integer, ForeignKey('enemies.id'))
    conditionName=Column(String)
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

class Action(Base):
    __tablename__ = 'actions'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    enemyid=Column(Integer, ForeignKey('enemies.id'))
    name = Column(String)
    attackBonus = Column(String)
    targetMax = Column(Integer)
    damage = Column(String)
    damageType = Column(String)

    def __repr__(self):
        return self.name

class LedgendaryAction(Base):
    __tablename__ = 'ledgendaryActions'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    enemyid=Column(Integer, ForeignKey('enemies.id'))
    title = Column(String)
    description = Column(String)

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


# def CreateDbAndPopulate():
#     session = CreateSession()
#     goblin=Enemy(name='Goblin',size='Small',type='Humanoid(Goblinoid)',alignment='neutral evil',ac=15,hp='2d6',speed='30ft.',STR=8,DEX=14,CON=10,INT=10,WIS=8,CHA=8)
#     bandit=Enemy(name='Bandit',size='Medium',type='Humanoid(any race)',alignment='any non-lawful alignment',ac=12,hp='2d8+2',speed='30ft.',STR=11,DEX=12,CON=12,INT=10,WIS=10,CHA=10)
#     dragon=Enemy(name='Adult Red Dragon',size='Huge',type='Dragon',alignment='chaotic evil',ac=19,hp='19d12+133',speed='40ft., climb 40ft., fly 80ft.',STR=27,DEX=10,CON=25,INT=16,WIS=13,CHA=21,languages="Common,Draconic",senses="blindsight 60ft., darkvision 120ft., passive Perception 23",challenge="17 (18,000xp)",legendaryActionsOverview="""The dragon can take 3 legendary actions, choosing from the
#                                                                                                                                                                                                                             options below. Only one legendary action option can be used
#                                                                                                                                                                                                                             at a time and only at the end of another creature's turn. The
#                                                                                                                                                                                                                             dragon regains spent legendary actions at the start of its turn.""")
#     drow=Enemy(name='Drow',size='Medium',type='Humanoid(Elf)',alignment='neutral evil',ac=15,hp='3d8',speed='30ft.',STR=10,DEX=14,CON=10,INT=11,WIS=11,CHA=12)

#     badguys=[goblin,bandit,dragon,drow]

#     for i in badguys:
#         x = session.query(Enemy).filter_by(name=i.name).first()
#         if not x:
#                 session.add(i)

#     session.add(Action(enemyid=1,name='Scimitar',type='Melee',attackBonus='+4',range='5ft.',targetMax=1,damage='1d6+2',damageType='Slashing'))
#     session.add(Action(enemyid=1,name='Shortbow',type='Ranged',attackBonus='+4',range='80/320ft.',targetMax=1,damage='1d6+2',damageType='Piercing'))
#     session.add(Action(enemyid=2,name='Scimitar',type='Melee',attackBonus='+3',range='5ft.',targetMax=1,damage='1d6+1',damageType='Slashing'))
#     session.add(Action(enemyid=2,name='Light Crossbow',type='Ranged',attackBonus='+3',range='80/320ft.',targetMax=1,damage='1d8+1',damageType='Piercing'))
#     session.add(Action(enemyid=3,name='Bite',type='Melee',attackBonus='+14',range='10ft.',targetMax=1,damage='2d10+8',damageType='Piercing')) #also has a secondary damage type, 2d6 fire. how best to show this?
#     session.add(Action(enemyid=3,name='Claw',type='Melee',attackBonus='+14',range='5ft.',targetMax=1,damage='2d6+8',damageType='Slashing'))
#     session.add(Action(enemyid=3,name='Tail',type='Melee',attackBonus='+14',range='15ft.',targetMax=1,damage='2d8+8',damageType='Bludgeoning'))
#     session.add(Action(enemyid=4,name='Shortsword',type='Melee',attackBonus='+4',range='5ft.',targetMax=1,damage='1d6+2',damageType='Piercing'))
#     session.add(Action(enemyid=4,name='Hand Crossbow',type='Ranged',attackBonus='+4',range='30/120ft.',targetMax=1,damage='1d6+2',damageType='Piercing')) #this one has more effects if it hits, need to think of how to show this.
#     session.add(Hero(name = 'Beardor',ac = 18,hp = 25))    
#     session.add(Hero(name = 'James Brown',ac = 17,hp = 23))
#     session.add(Hero(name = 'Bonk',ac = 12,hp = 16))
#     session.add(SavingThrows(enemyid=3,DEX='+6',CON='+13',WIS='+7',CHA='+5'))
#     session.add(SpecialTraits(enemyid=3,title='Legendary Resistance (3/Day).',description="If the dragon fails a saving throw, it can choose to succeed instead."))
#     session.commit()

def createEnemyInstance(enemyName):
    session = CreateSession()
    Badguy = session.query(Enemy).filter_by(name=enemyName).first()
    Badguy ={k:v for k, v in Badguy.__dict__.items() if k!= '_sa_instance_state'and k!= 'enemyid' and v is not None}
    BadguysActions = session.query(Action).filter_by(enemyid=Badguy['id']).all()
    BadguysActions =[{k:v for k, v in i.__dict__.items() if k!= '_sa_instance_state'and k!= 'enemyid' and v is not None} for i in BadguysActions]
    Badguy['actions'] = BadguysActions

    st = session.query(SavingThrows).filter_by(enemyid=Badguy['id']).first()
    if st:
        saving_throws=[f"{k.title()} {v}" for k, v in st.__dict__.items() if k != 'id'and k!= '_sa_instance_state'and k!= 'enemyid' and v is not None]
        Badguy['savingThrows'] = saving_throws

    traits = session.query(SpecialTraits).filter_by(enemyid=Badguy['id']).first()
    if traits:
        Badguy['specialTraits'] = [{'title':traits.title,'description':traits.description}]

    actionsText = session.query(ActionsText).filter_by(enemyid=Badguy['id']).all()
    if actionsText:
        Badguy['actionsText'] = [{'title':i.title,'actionType':i.actionType,'description':i.description} for i in actionsText]

    EnemyInstance =enemies.Enemy(**Badguy)
    session.close()
    return EnemyInstance

def createHeroInstance(heroName):
    session = CreateSession()
    Goodguy = session.query(Hero).filter_by(name=heroName).first()
    HeroInstance =heroes.Hero(Goodguy.name,Goodguy.hp,Goodguy.ac)
    return HeroInstance

def referenceEnemyInstance(enemyInstance): #this function gets passed a models.Combat row object
    session = CreateSession()
    Badguy = session.query(Enemy).filter_by(id=enemyInstance.enemyid).first()
    BadguysActions = session.query(Action).filter_by(enemyid=Badguy.id).all()
    BadguysActions = [{'name':i.name,'attackBonus':i.attackBonus,'targetMax':i.targetMax,'damage':i.damage,'damageType':i.damageType} for i in BadguysActions]
    EnemyInstance =enemies.InitialisedEnemy(enemyInstance.enemyName,Badguy.size,Badguy.type,Badguy.alignment,enemyInstance.AC,enemyInstance.currentHp,Badguy.speed,Badguy.STR,Badguy.DEX,Badguy.CON,Badguy.INT,Badguy.WIS,Badguy.CON,actions=BadguysActions,initiative=enemyInstance.initiativeScore,enemyId=Badguy.id,combatId=enemyInstance.id)
    return EnemyInstance

def referenceEnemyInstanceByName(enemyCombatId): #this function just gets a string passed to it
    session = CreateSession()
    Badguy = session.query(Combat).filter_by(id=enemyCombatId).first()
    BadguysStats = session.query(Enemy).filter_by(id=Badguy.enemyid).first()
    BadguysActions = session.query(Action).filter_by(enemyid=Badguy.enemyid).all()
    BadguysActions = [{'name':i.name,'attackBonus':i.attackBonus,'targetMax':i.targetMax,'damage':i.damage,'damageType':i.damageType} for i in BadguysActions]
    EnemyInstance =enemies.InitialisedEnemy(Badguy.enemyName,BadguysStats.size,BadguysStats.type,BadguysStats.alignment,Badguy.AC,Badguy.currentHp,BadguysStats.speed,BadguysStats.STR,BadguysStats.DEX,BadguysStats.CON,BadguysStats.INT,BadguysStats.WIS,BadguysStats.CON,actions=BadguysActions,initiative=Badguy.initiativeScore,enemyId=Badguy.id,combatId=enemyCombatId)
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
        session.close()
    except AttributeError:
        session.add(Combat(enemyName=f"{enemy.name}",initiativeScore=enemy.initiative,currentHp=enemy.hp,AC=enemy.AC,maxHp=enemy.hp))
        session.commit()
        session.close()


CreateSession()