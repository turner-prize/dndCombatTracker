from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session
import os


Base = automap_base()
mydir=os.path.dirname(os.path.abspath(__file__))
# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine(f"sqlite:///{os.path.join(mydir,'combatTracker.db')}")#,echo=True)

# reflect the tables
Base.prepare(engine, reflect=True)
Enemy = Base.classes.enemies
SavingThrows = Base.classes.SavingThrows

session = Session(engine)

Badguy = session.query(Enemy,SavingThrows).filter_by(name="Adult Red Dragon").first()
st=[Badguy[1].Str,Badguy[1].Dex,Badguy[1].Con,Badguy[1].Int,Badguy[1].Wis,Badguy[1].Cha]

print(st)