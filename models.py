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
    damage_resistances=Column(String)
    damage_vulnerabilities=Column(String)
    damage_immunities=Column(String)
    condition_immunities=Column(String)

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


def CreateDbAndPopulate():
    session = CreateSession()
    session.add(Hero(name = 'Beardor',ac = 18,hp = 25))    
    session.add(Hero(name = 'James Brown',ac = 17,hp = 23))
    session.add(Hero(name = 'Bonk',ac = 12,hp = 16))
    session.commit()


def QueryDB(Badguy):
    Badguy ={k:v for k, v in Badguy.__dict__.items() if k!= '_sa_instance_state'and k!= 'enemyid' and v is not None}
    BadguysActions = session.query(Action).filter_by(enemyid=Badguy['id']).all()
    BadguysActions =[{k:v for k, v in i.__dict__.items() if k!= '_sa_instance_state'and k!= 'enemyid' and v is not None} for i in BadguysActions]
    Badguy['actions'] = BadguysActions

    st = session.query(SavingThrows).filter_by(enemyid=Badguy['id']).first()
    if st:
        saving_throws=[f"{k.title()} {v}" for k, v in st.__dict__.items() if k != 'id'and k!= '_sa_instance_state'and k!= 'enemyid' and v is not None]
        Badguy['savingThrows'] = saving_throws

    traits = session.query(SpecialTraits).filter_by(enemyid=Badguy['id']).all()
    if traits:
        Badguy['specialTraits'] = [{'title':i.title,'description':i.description} for i in traits]

    actionsText = session.query(ActionsText).filter_by(enemyid=Badguy['id']).all()
    if actionsText:
        Badguy['actionsText'] = [{'title':i.title,'actionType':i.actionType,'description':i.description} for i in actionsText]
    return Badguy

def createEnemyInstance(enemyName):
    session = CreateSession()
    Badguy = session.query(Enemy).filter_by(name=enemyName).first() #returns Enemy.Row instance
    Badguy=QueryDB(Badguy)
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
    Badguy = session.query(Enemy).filter_by(id=enemyInstance.enemyid).first() #returns Enemy.Row instance
    Badguy = QueryDB(Badguy)
    Badguy['initiative']=enemyInstance.initiativeScore
    Badguy['combatId']=enemyInstance.id
    Badguy['enemyId']=enemyInstance.enemyid
    Badguy['name']=enemyInstance.enemyName
    Badguy['hp']=enemyInstance.currentHp
    Badguy['maxhp']=enemyInstance.maxHp

    EnemyInstance =enemies.InitialisedEnemy(**Badguy)
    return EnemyInstance

def referenceEnemyInstanceByName(enemyCombatId): #this function just gets a string passed to it
    session = CreateSession()
    Badguy = session.query(Combat).filter_by(id=enemyCombatId).first()
    BadguyStats = session.query(Enemy).filter_by(id=Badguy.enemyid).first() #returns Enemy.Row instance
    BadguyStats = QueryDB(BadguyStats)

    BadguyStats['initiative']=Badguy.initiativeScore
    BadguyStats['combatId']=Badguy.id
    BadguyStats['enemyId']=Badguy.enemyid
    BadguyStats['name']=Badguy.enemyName
    BadguyStats['hp']=Badguy.currentHp
    BadguyStats['maxhp']=Badguy.maxHp

    EnemyInstance =enemies.InitialisedEnemy(**BadguyStats)
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