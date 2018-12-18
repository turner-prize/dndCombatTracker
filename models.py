from sqlalchemy import create_engine
import os 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker

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
session.commit()