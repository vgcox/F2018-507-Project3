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
        print("Database initiated")
    except:
        print("Error, database not created correctly")
create_choc_db()

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
