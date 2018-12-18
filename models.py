from sqlalchemy import create_engine
import os 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
import enemies
import weapons



mydir=os.path.dirname(os.path.abspath(__file__))
engine = create_engine(f"sqlite:///{os.path.join(mydir,'combatTracker.db')}")#,echo=True)
Session = sessionmaker(bind=engine)
session = Session()
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
    hp = Column(String)
    speed = Column(String)
    STR = Column(Integer)
    DEX = Column(Integer)
    CON = Column(Integer)
    INT = Column(Integer)
    WIS = Column(Integer)
    CHA = Column(Integer)
    #challenge = Column(String)

    def __repr__(self):
        return "<Enemy(name='%s'>" % (self.name)

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
        return "<Enemy(name='%s'>" % (self.name)


def CreateDbAndPopulate():
    mydir=os.path.dirname(os.path.abspath(__file__))
    engine = create_engine(f"sqlite:///{os.path.join(mydir,'combatTracker.db')}")#,echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()
    Base.metadata.create_all(engine)
    goblin=Enemy(name='Goblin',size='Small',type='Humanoid(Goblinoid)',alignment='neutral evil',ac=15,hp='2d6',speed='30ft.',STR=8,DEX=14,CON=10,INT=10,WIS=8,CHA=8)
    bandit=Enemy(name='Bandit',size='Medium',type='Humanoid(any race)',alignment='any non-lawful alignment',ac=12,hp='2d8+2',speed='30ft.',STR=11,DEX=12,CON=12,INT=10,WIS=10,CHA=10)
    dragon=Enemy(name='Adult Red Dragon',size='Huge',type='Dragon',alignment='chaotic evil',ac=19,hp='19d12+133',speed='40ft., climb 40ft., fly 80ft.',STR=27,DEX=10,CON=25,INT=16,WIS=13,CHA=21)
    drow=Enemy(name='Drow',size='Medium',type='Humanoid(Elf)',alignment='neutral evil',ac=15,hp='3d8',speed='30ft.',STR=10,DEX=14,CON=10,INT=11,WIS=11,CHA=12)

    badguys=[goblin,bandit,dragon,drow]

    for i in badguys:
        x = session.query(Enemy).filter_by(name=i.name).first()
        if not x:
            session.add(i)

    session.add(Weapon(enemyid=1,
        name='Scimitar',
        type='Melee',
        attackBonus='+4',
        range='5ft.',
        targetMax=1,
        damage='1d6+2',
        damageType='Slashing'))

    session.add(Weapon(enemyid=1,
            name='Shortbow',
            type='Ranged',
            attackBonus='+4',
            range='80/320ft.',
            targetMax=1,
            damage='1d6+2',
            damageType='Piercing'))

    session.add(Weapon(enemyid=2,
            name='Scimitar',
            type='Melee',
            attackBonus='+3',
            range='5ft.',
            targetMax=1,
            damage='1d6+1',
            damageType='Slashing'))

    session.add(Weapon(enemyid=2,
            name='Light Crossbow',
            type='Ranged',
            attackBonus='+3',
            range='80/320ft.',
            targetMax=1,
            damage='1d8+1',
            damageType='Piercing'))

    session.add(Weapon(enemyid=3,
            name='Bite',
            type='Melee',
            attackBonus='+14',
            range='10ft.',
            targetMax=1,
            damage='2d10+8',
            damageType='Piercing')) #also has a secondary damage type, 2d6 fire. how best to show this?

    session.add(Weapon(enemyid=3,
            name='Claw',
            type='Melee',
            attackBonus='+14',
            range='5ft.',
            targetMax=1,
            damage='2d6+8',
            damageType='Slashing'))

    session.add(Weapon(enemyid=3,
            name='Tail',
            type='Melee',
            attackBonus='+14',
            range='15ft.',
            targetMax=1,
            damage='2d8+8',
            damageType='Bludgeoning'))

    session.add(Weapon(enemyid=4,
            name='Shortsword',
            type='Melee',
            attackBonus='+4',
            range='5ft.',
            targetMax=1,
            damage='1d6+2',
            damageType='Piercing'))

    session.add(Weapon(enemyid=4,
            name='Hand Crossbow',
            type='Ranged',
            attackBonus='+4',
            range='30/120ft.',
            targetMax=1,
            damage='1d6+2',
            damageType='Piercing')) #this one has more effects if it hits, need to think of how to show this.


    session.commit()


def createEnemyInstance(enemyName):
        Badguy = session.query(Enemy).filter_by(name=enemyName).first()
        #below is all well and good but can I just pass a dict to it?
        Gobster =enemies.Enemy('Goblin1',Badguy.size,Badguy.type,Badguy.alignment,Badguy.ac,Badguy.hp,Badguy.speed,Badguy.STR,Badguy.DEX,Badguy.CON,Badguy.INT,Badguy.WIS,Badguy.CON,weapons=weapons.Weapons2)
        print (Gobster.AC)
        print(Gobster.hp)
        print(Gobster.initiative)
        return Gobster

#createEnemyInstance('Adult Red Dragon')