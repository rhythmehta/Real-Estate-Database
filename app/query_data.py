# query_data.py
from .models import *
import numpy as np
import pandas as pd
from sqlalchemy import func

#session init
Session = sessionmaker(bind=engine)
session = Session()

print("Enter the desired month and year to retreive reports. \n You can enter 2022 as year then 4 as month to get a good example of results because of the sample data.")
year = int(input("Enter year: "))
month = int(input("Enter month: "))
monthName = datetime.datetime.strptime(str(month), "%m").strftime("%B")

print("\n ---- QUERYING REPORT FOR ", monthName, year, " ---- \n")

print("1. Top 5 offices with the most sales")
query = session.query(Offices.area,func.count(Houses.officeID)).join(Sales, Offices).filter(Houses.sold==True,func.extract('month', Sales.saleDate)==month,func.extract('year',Sales.saleDate)==year).group_by(Houses.officeID).order_by(func.count(Houses.officeID).desc()).limit(5).statement
print(pd.read_sql(query, session.bind), "\n")

print("2. Top 5 estate agents who have sold the most")
query = session.query(Agents.name,Agents.contact,func.count(Houses.listingAgentID)).join(Sales, Agents).filter(Houses.sold == True,func.extract('month', Sales.saleDate)==month,func.extract('year', Sales.saleDate) == year).group_by(Houses.listingAgentID).order_by(func.count(Houses.listingAgentID).desc()).limit(5).statement
print(pd.read_sql(query, session.bind), "\n")

print("\n 3.a. Commission that each estate agent must receive \n")
query = session.query(Commission.agentID,Agents.name,Agents.contact,func.sum(Commission.commission)).join(Agents, Sales).filter(func.extract('month', Sales.saleDate) == month,func.extract('year', Sales.saleDate) == year).group_by(Commission.agentID).order_by(func.sum(Commission.commission).desc()).statement
print(pd.read_sql(query, session.bind), "\n")

print("3.b. Average number of days that the house was on the market")
query = session.query(Houses.name,Houses.listingDate,Sales.saleDate).join(Sales).filter(Houses.sold == True,func.extract('month', Sales.saleDate) == month,func.extract('year', Sales.saleDate) == year).statement
print(pd.read_sql(query, session.bind))
_pd = pd.read_sql(query, session.bind)
diff = []
for idx, _ in enumerate(_pd.iterrows()): diff.append((_pd['saleDate'][idx]-_pd['listingDate'][idx]).days)
print("\n Houses were on the market for about", np.mean(diff), "days \n")

print("\n 4. Average selling price")
query = session.query(Houses.name,Sales.salePrice
).join(Sales).filter(Houses.sold == True,func.extract('month',Sales.saleDate)==month,func.extract('year',Sales.saleDate)==year).statement
avg = session.query(func.avg(Sales.salePrice)).filter(func.extract('month', Sales.saleDate) == month,func.extract('year', Sales.saleDate) == year).one()
print(pd.read_sql(query, session.bind))
print("\n Avg selling price: ", (avg[0]))

print("---- END OF REPORT, ", monthName, year, " ----")
