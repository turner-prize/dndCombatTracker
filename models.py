from sqlalchemy import create_engine
import os 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
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

    def __repr__(self):
        return "<Enemy(name='%s'>" % (self.name)


Base.metadata.create_all(engine)

gobby = Enemy(name='Goblin',size='Small',type='Humanoid(Goblinoid)',alignment='neutral evil',ac=15,hp='2d6',speed='30ft.',STR=8,DEX=14,CON=10,INT=10,WIS=8,CHA=8)
bandit=Enemy(name='Bandit',size='Medium',type='Humanoid(any race)',alignment='any non-lawful alignment',ac=12,hp='2d8+2',speed='30ft.',STR=11,DEX=12,CON=12,INT=10,WIS=10,CHA=10)

x = session.query(Enemy).filter_by(name='Goblin').first()

if not x:
    session.add(gobby)
session.commit()