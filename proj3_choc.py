import sqlite3 as sqlite
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
        conn = sqlite.connect(DBNAME)
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
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
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
        BroadBeanOriginId INTEGER);'''
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
    with open("flavors_of_cacao_cleaned.csv") as f:
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()
        csvReader = csv.reader(f)
        next(csvReader)
        for row in csvReader:
            statement = '''INSERT INTO Bars(Company,SpecificBeanBarName,REF,ReviewDate,CocoaPercent,CompanyLocationId,Rating,BeanType,BroadBeanOriginId)
            VALUES (?,?,?,?,?,?,?,?,?) '''
            cur.execute(statement, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
            conn.commit()
    # with open("games.csv") as g:
    #     csvReader = csv.reader(g)
    #     conn = sqlite.connect('coxtori_big10.sqlite')
    #     cur = conn.cursor()
    #     for row in csvReader:
    #         statement = '''INSERT INTO Games(Winner, Loser, WinnerScore, LoserScore, Round,Time) VALUES(?,?,?,?,?,?)'''
    #         cur.execute(statement, (row[0], row[1], row[2], row[3], row[4], row[5]))
    #         conn.commit()
    conn.commit()
    conn.close()
create_choc_db()
populate_choc_db()
# Part 2: Implement logic to process user commands
def process_command(command):
    return []


def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue

# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    interactive_prompt()
