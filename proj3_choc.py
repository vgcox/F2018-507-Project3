import sqlite3
import csv
import json

# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 1: Read data from CSV and JSON into a new database called choc.db
DBNAME = 'choc.db'
BARSCSV = 'flavors_of_cacao_cleaned.csv'
COUNTRIESJSON = 'countries.json'
def create_choc_db():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        conn.commit()
        print("Database initiated")
    except:
        print("Error, database not created correctly")
    statement = '''
        DROP TABLE IF EXISTS 'Bars';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Countries';
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()
def populate_choc_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = '''PRAGMA foregin_keys'''
    cur.execute(statement)
    conn.commit()
    statement = '''
    CREATE TABLE Countries (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Alpha2 TEXT,
        Alpha3 TEXT,
        EnglishName TEXT,
        Region TEXT,
        Subregion TEXT,
        Population INTEGER,
        Area REAL)'''
    cur.execute(statement)
    conn.commit()
    statement = '''
    CREATE TABLE Bars (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Company TEXT,
        SpecificBeanBarName TEXT,
        REF TEXT,
        ReviewDate TEXT,
        CocoaPercent REAL,
        CompanyLocationId INTEGER,
        Rating REAL,
        BeanType TEXT,
        BroadBeanOriginId INTEGER,
        FOREIGN KEY (BroadBeanOriginId) REFERENCES Countries (Id),
        FOREIGN KEY(CompanyLocationId) REFERENCES Countries(Id));'''
    cur.execute(statement)
    conn.commit()
    with open('countries.json') as f:
        data =json.loads(f.read())
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        for item in data:
            statement = '''INSERT INTO Countries (Alpha2, Alpha3, EnglishName, Region, Subregion, Population, Area)
            VALUES(?,?,?,?,?,?,?)'''
            cur.execute(statement, (item['alpha2Code'], item['alpha3Code'], item['name'], item['region'], item['subregion'], item['population'], item['area']))
            conn.commit()
    with open("flavors_of_cacao_cleaned.csv") as f:
        conn = sqlite3.connect(DBNAME)
        conn.text_factory = str
        cur = conn.cursor()
        csvReader = csv.reader(f)
        next(csvReader)
        for row in csvReader:
            companyId = row[5]
            companyStatment = '''SELECT Id FROM Countries WHERE EnglishName="'''+companyId+'''"'''
            cur.execute(companyStatment)
            companyResults = cur.fetchall()
            companyValue = companyResults[0][0]
            beanId = row[8]
            beanStatment = '''SELECT Id FROM Countries WHERE EnglishName="'''+beanId+'''"'''
            cur.execute(beanStatment)
            beanResults = cur.fetchall()
            if len(beanResults) > 0:
                beanValue = beanResults[0][0]
            else:
                beanValue = 'NULL'
            statement = '''INSERT INTO Bars(Company,SpecificBeanBarName,REF,ReviewDate,CocoaPercent, CompanyLocationId, Rating,BeanType, BroadBeanOriginId)
            VALUES (?,?,?,?,?,?,?,?,?) '''
            cur.execute(statement, (row[0], row[1], row[2], row[3], row[4], companyValue, row[6], row[7], beanValue))
            conn.commit()
    conn.commit()
    conn.close()
create_choc_db()
populate_choc_db()
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()
convert = '''SELECT CAST(CocoaPercent AS decimal(0,2)) FROM Bars'''
cur.execute(convert)
results = cur.fetchall()
id = 0
for result in results:
    id+=1
    sql = '''UPDATE Bars SET CocoaPercent="'''+str(result[0]/100)+'''" WHERE Id="'''+str(id)+'''"'''
    cur.execute(sql)
    conn.commit()
# Part 2: Implement logic to process user commands
def process_command(command):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    comm_list = command.split()[1:]
    num = ''' 10'''
    for item in comm_list:
        if 'top' in item or 'bottom' in item:
            num = item.split('=')[1]
    limit = ''' LIMIT '''+num
    if 'bottom' in command:
        dir = ''' ASC'''
    else:
        dir = ''' DESC'''
    if command.split()[0] == 'bars':
        base = '''SELECT Bars.SpecificBeanBarName, Bars.Company, C1.EnglishName, Bars.Rating,
        Bars.CocoaPercent, C2.EnglishName FROM Bars JOIN Countries AS C1 ON Bars.CompanyLocationId=C1.Id
        JOIN Countries AS C2 ON Bars.BroadBeanOriginId=C2.Id'''
        params = [i.split('=')[0] for i in comm_list]
        chosen = lambda params, options: any(i in options for i in params)
        search_by = []
        if 'sellcountry' in params:
            search_by.append('C1.Alpha2')
        if 'sellregion' in params:
            search_by.append('C1.Region')
        if 'sourcecountry' in params:
            search_by.append('C2.Alpha2')
        if 'sourceregion' in params:
            search_by.append('C2.Region')
        if len(search_by) > 0:
            for item in comm_list:
                if 'country' in item or 'region' in item:
                    place = item.split('=')[1]
            where = ''' WHERE '''+search_by[0]+'''='''+'''"'''+place+'''"'''
            base = base+where
        if 'cocoa' in params:
            order = ''' ORDER BY Bars.CocoaPercent'''
            base = base+order
        else:
            order = ''' ORDER BY Bars.Rating'''
            base = base+order
        base = base+dir+limit
        cur.execute(base)
        results = cur.fetchall()
        return results
    if command.split()[0] == 'companies':
        comm_list = command.split()[1:]
        select = '''SELECT Bars.Company, Countries.EnglishName, Bars.Rating AS "AGG" FROM Bars JOIN Countries ON Bars.CompanyLocationId=Countries.Id'''
        rest = ''' GROUP BY Bars.Company HAVING Count(SpecificBeanBarName) > 4 ORDER BY Bars.Rating'''
        if 'cocoa' in command:
            select = '''SELECT Bars.Company, Countries.EnglishName, Bars.CocoaPercent AS "AGG" FROM Bars JOIN Countries ON Bars.CompanyLocationId=Countries.Id'''
            rest =''' GROUP BY Bars.Company HAVING Count(SpecificBeanBarName) > 4 ORDER BY Bars.CocoaPercent'''
        elif 'bars_sold' in command:
            select = '''SELECT Bars.Company, Countries.EnglishName, Count(Company) AS "AGG" FROM Bars JOIN Countries ON Bars.CompanyLocationId=Countries.Id'''
            rest = ''' GROUP BY Bars.Company HAVING Count(SpecificBeanBarName) > 4 ORDER BY Count(Company)'''
        search_by = []
        if 'country' in command:
            search_by.append('Countries.Alpha2')
        if 'region' in command:
            search_by.append('Countries.Region')
        if len(search_by) > 0:
            for item in comm_list:
                if 'country' in item or 'region' in item:
                    place = item.split('=')[1]
            where = ''' WHERE '''+search_by[0]+'''='''+'''"'''+place+'''"'''
            select = select + where
        if 'bottom' in command:
            dir = ''' ASC'''
            rest = rest+dir+''', Bars.Company DESC'''
        else:
            dir = ''' DESC'''
            rest = rest+dir+''', Bars.Company DESC'''
        sql = select+rest+limit
        cur.execute(sql)
        results = cur.fetchall()
        return results
    if command.split()[0] == 'countries':
        select = '''SELECT Countries.EnglishName, Countries.Region, Bars.Rating AS 'Rating' FROM Bars JOIN Countries'''
        if 'sources' in command:
            country = ''' ON Bars.BroadBeanOriginId=Countries.Id GROUP BY Bars.BroadBeanOriginId HAVING Count(Bars.SpecificBeanBarName) > 4'''
        else:
            country = ''' ON Bars.CompanyLocationId=Countries.Id GROUP BY Bars.CompanyLocationId HAVING Count(Bars.SpecificBeanBarName) > 4'''
        if 'cocoa' in command:
            select = '''SELECT Countries.EnglishName, Countries.Region, Bars.CocoaPercent AS ' Cocoa Percentage' FROM Bars JOIN Countries'''
            order = ''' ORDER BY Bars.CocoaPercent'''
        elif 'bars_sold' in command:
            select ='''SELECT Countries.EnglishName, Countries.Region, Count(Bars.Company) AS "Bars Sold" FROM Bars JOIN Countries'''
            order = ''' ORDER BY Count(Company)'''
        else:
            order = ''' ORDER BY Bars.Rating'''
        sql = select+country+order+dir+limit
        cur.execute(sql)
        results = cur.fetchall()
        return results
    if command.split()[0] == 'regions':
        comm_list = command.split()[1:]
        select = '''SELECT Countries.Region, Bars.Rating AS 'Rating' FROM Countries JOIN Bars'''
        if 'sources' in command:
            country = ''' ON Countries.Id=Bars.BroadBeanOriginId GROUP BY Bars.BroadBeanOriginId HAVING Count(Bars.SpecificBeanBarName) > 4'''
        else:
            country = ''' ON Bars.CompanyLocationId=Countries.Id GROUP BY Bars.CompanyLocationId HAVING Count(Bars.SpecificBeanBarName) > 4'''
        if 'cocoa' in command:
            select = '''SELECT Countries.Region, Bars.CocoaPercent AS 'Cocoa Percentage FROM Bars JOIN Countries'''
            order = ''' ORDER BY Bars.CocoaPercent'''
        elif 'bars_sold' in command:
            select ='''SELECT Countries.Region, Count(Bars.Company) AS "Bars Sold" FROM Bars JOIN Countries'''
            order = ''' ORDER BY Count(Company)'''
        else:
            order = '''ORDER BY Bars.Rating'''
        sql = select+country+order+dir+limit
        cur.execute(sql)
        results = cur.fetchall()
        return results
# command = input('Enter a command: ')
# process_command(command))
def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    flag = True
    while flag == True:
        response = input('Enter a command: ')
        if response == 'help':
            print(help_text)
            continue
        try:
            results_list = process_command(response)
            out = ''
            for sets in results_list:
                for item in sets:
                    if str(item)[0] == '0':
                        item = str(int(float(item)*100))+"%"
                    out+='{}    '.format(item)
                out+="\n"
            print(out)
        except:
            if response == 'exit':
                flag = False
            else:
                print("Sorry, the command you entered was not valid.\nPlease try again or type 'help' to see instructions for valid commands")

# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    interactive_prompt()
