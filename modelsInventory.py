import os 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,create_engine
from sqlalchemy.orm import sessionmaker, Session


def CreateSession():
        mydir=os.path.dirname(os.path.abspath(__file__))
        engine = create_engine(f"sqlite:///{os.path.join(mydir,'inventoryTracker.db')}")#,echo=True)
        Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        return Session()

Base = declarative_base()

class Inventory(Base):
    __tablename__ = 'enemies'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    itemName = Column(String)
    quantity = Column(Integer)

    

def updateInventory(itemName,quantity):
    session = CreateSession()
    session.add(Inventory(itemName=itemName,quantity=quantity))
    session.commit()
    
    
def getInventory():
    session = CreateSession()
    items = session.query(Inventory).all()
    return [(i.itemName,i.quantity) for i in items]
    
def removeInventoryItem(itemName,quantity):
    session = CreateSession()
    session.query(Inventory).filter_by(itemName=itemName).delete()
    session.commit()