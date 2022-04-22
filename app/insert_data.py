# insert_data.py
from app.create import *

officeColumns = ['id', 'area']
officeRows = [[101, 'San Marino'],
    [102, 'San Jose'],
    [103, 'San Francisco'],
    [104, 'San Diego'],
    [105, 'Santa Fe'],
    [106, 'Santa Cruz'],
    [107, 'San Mateo']]

agentColumns = ['id', 'name', 'contact']
agentRows = [[201, 'Mark Zucks', 'mark@fakebook1.com'],[202, 'Steve Robs', 'steve@pineapple1.com'],[203, 'Bill Waits', 'bill@macrohard1.com'],[204, 'Jeff Amazin', 'jeff@painforest.com'],[205, 'Jack Dowry', 'jack@teeter.com'],
[206, 'Banye East', 'clb@pottyfi.com'],[207, 'Joe Brandon', 'lgb@123fjb.com'],[208, 'Doland Troomp', 'troomp@8tower.com']]

sellerColumns = ['id','name','contact']
sellerRows = [[301,'Arnold','arnold@somemail.com'],
    [302,'Bruce','bruce@somemail.com'],
    [303, 'Ryan', 'ryan@somemail.com'],
    [304, 'Adam', 'adam@somemail.com'],
    [305, 'Richard', 'richard@somemail.com'],
    [306, 'Joe', 'joe@somemail.com'],
    [307, 'Ironman', 'ironman@somemail.com'],
    [308, 'Trump', 'trump@somemail.com'],
    [309, 'Bernie', 'bernie@somemail.com'],
    [310, 'Kamala', 'kamala@somemail.com'],
    [311, 'Sean', 'shawn@somemail.com'],
    [312, 'Olu', 'olu@somemail.com'],
    [313, 'Chamath', 'chamath@somemail.com']]

buyerColumns = ['id','name','contact']
buyerRows = [[401,'Ronald','ron@somemail.com'],
    [402, 'Nixon', 'nix@somemail.com'],
    [403, 'Harvey', 'harv@somemail.com'],
    [404, 'Smith', 'smit@somemail.com'],
    [405, 'Umm', 'umm@somemail.com'],
    [406, 'Talafi', 'Talafi@somemail.com'],
    [407, 'Bakchod', 'bakchod@somemail.com'],
    [408, 'Kofi', 'coffee@somemail.com'],
    [409, 'Eminem', 'marshall@somemail.com']]

houseColumns = ['id','name','officeID','listingAgentID','sellerID','beds','baths','listingPrice','zipcode', 'listingDate','sold']
houseRows = [
    [501,'High Rise Studio', 101,201,301,2,2,2900000,94103, datetime.date(2022, 4, 4), False],
    [505,'High-end Luxury Apt',102,203,305,1,1,430000,942069, datetime.date(2022, 5, 8), False],
    [511,'Furnished Studio',105,206,309,2,1,255000,911011, datetime.date(2022, 3, 19), False],
    [506,'Home with Garage',103,203,306,5,2,47500,999001, datetime.date(2022, 4, 12), False],
    [510,'Half building',104,202,303,7,4,9650000,999001, datetime.date(2022, 4, 17), False],
    [512,'Unfurnished Apt', 105,206,311,3,1,19900,999666, datetime.date(2022, 4, 8), False],
    [513,'Lease only Apt', 105,205,304,1,0,59900,123456, datetime.date(2022, 4, 2), False],
    [503,'Jumbo Penthouse',102,202,312,3,1,90000,90404, datetime.date(2022, 3, 4), False],
    [504,'Student House',102,202,310,4,5,600000,911420, datetime.date(2022, 5, 6), False],
    [502,'Corner House', 101,201,302,5,2,150000,91101, datetime.date(2022, 4, 3), False],
    [509,'Apartment',104,205,309,12,4,400000,911420, datetime.date(2022, 2, 21), False],
    [507,'Mansion XL',103,204,307,8,4,420000,989089, datetime.date(2022, 4, 20), False],
    [514,'Store', 106,207,312,6,3,355000, 56789, datetime.date(2022, 3, 14), False],
    [508,'Condo',104,207,308,4,2,690000,94103, datetime.date(2022, 3, 6), False],
    [515,'Room', 106,207,303,5,5,2555000, 101112, datetime.date(2022, 3, 17), False]]

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

#data to be stored
columns = [officeColumns, houseColumns, agentColumns, sellerColumns, buyerColumns]
rows = [officeRows, houseRows, agentRows, sellerRows, buyerRows]
tables = [Offices, Houses, Agents, Sellers, Buyers]

def createDB(tables, columns, rows):
    for value in rows:
        item_dict = dict(zip(columns, value))
        entry = tables(**item_dict)
        session.add(entry)

for i in range(len(tables)): createDB(tables[i], columns[i], rows[i])
session.commit()

def dotransaction(house_id,buyer_id,sale_price,sale_date):
    agent_id = session.query(Houses.listingAgentID).filter(Houses.id == house_id).first()[0]
    comps = [(sale_price < 100000, 0.01), (sale_price < 200000, 0.075),(sale_price < 500000, 0.06),(sale_price < 1000000, 0.05),(sale_price >= 1000000, 0.04)] #commision
    
    for comp in comps:
        if comp[0]: comm = comp[1]
    commission = sale_price*comm
    session.add(Sales(houseID=house_id,buyerID=buyer_id,salePrice=sale_price,saleDate=sale_date))
    sale = session.query(Sales.id).filter(Sales.houseID == house_id).first()[0]
    session.add(Commission(agentID=agent_id,saleID=sale,commission=commission))
    sold = session.query(Houses).filter(Houses.id == house_id)
    sold.update({Houses.sold: True}) #mark as sold
    session.commit()

transactions = [
    [501, 403, 2800000, datetime.date(2022, 4, 28)],
    [509, 407, 4800000, datetime.date(2022, 4, 23)],
    [505, 401, 300000, datetime.date(2022, 4, 25)],
    [511, 406, 100000, datetime.date(2022, 4, 30)],
    [514, 404, 360000, datetime.date(2022, 3, 28)],
    [515, 404, 760000, datetime.date(2022, 3, 28)],
    [508, 402, 700000, datetime.date(2022, 4, 28)],
    [502, 405, 130000, datetime.date(2022, 4, 29)],
    [506, 401, 45000, datetime.date(2022, 4, 28)],
    [507, 408, 29000, datetime.date(2022, 4, 30)],
    [503, 409, 88000, datetime.date(2022, 4, 27)],
    [504, 404, 550000, datetime.date(2022, 4, 22)]]

for transaction in transactions: dotransaction(*transaction)
session.close()
