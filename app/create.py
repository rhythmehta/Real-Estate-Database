#create.py
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

#DB setup
engine = create_engine('sqlite:///data.db')
engine.connect()
Base = declarative_base()

class Agents(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String)

class Offices(Base):
    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)
    area = Column(String)

class Sellers(Base):
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String)

class Buyers(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String)

class Houses(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sellerID = Column(Integer, ForeignKey('sellers.id'))
    beds = Column(Integer)
    baths = Column(Integer)
    listingPrice = Column(Integer)
    zipcode = Column(Integer)
    listingDate = Column(Date)
    listingAgentID = Column(Integer, ForeignKey('agents.id'))
    officeID = Column(Integer, ForeignKey('offices.id'))
    sold = Column(Boolean)

class Sales(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    houseID = Column(Integer, ForeignKey('houses.id'))
    buyerID = Column(Integer, ForeignKey('buyers.id'))
    salePrice = Column(Integer)
    saleDate = Column(Date)

class Commission(Base):
    __tablename__ = 'commission'
    id = Column(Integer, primary_key=True)
    agentID = Column(Integer, ForeignKey('agents.id'))
    saleID = Column(Integer, ForeignKey('sales.id'))
    commission = Column(Integer)
