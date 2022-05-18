import yfinance as yf
import os
from notion_client import Client
import csv

try:

    f = open("config.csv","r")
    reader = csv.reader(f)

    try:

        header = next(reader)
        print(header)
        database_id = header[0]
        NOTION_TOKEN = header[1]

    except:

        os.remove("config.csv")

        print("***********************************************************************")
        print("***********************************************************************")
        print('Hello there!\n')
        print('This is either your first time setting up the script, or you have deleted/modified your config file.')
        print("Let's create a new one for you.\n")

        f = open("config.csv","w")
        writer = csv.writer(f)

        DB_URL = input("Insert Database URL:\n")
        database_id = DB_URL.split('?')[0].split('/')[-1]
        NOTION_TOKEN = input("Insert secret token for your integration:\n")

        header =[database_id,NOTION_TOKEN]
        writer.writerow(header)
        f.close()

        print("You're all set-up now! Enjoy using you Investment Tracker script.\n")
        print("************************************************************************")
        print("************************************************************************\n")

        input("Press ANY key to close the script now and run it whenever you want to sync your investment data.")

        quit()

except IOError:

    print("***********************************************************************")
    print("***********************************************************************")
    print('Hello there!\n')
    print('This is either your first time setting up the script, or you have deleted/modified your config file.')
    print("Let's create a new one for you.\n")

    f = open("config.csv","w")
    writer = csv.writer(f)

    DB_URL = input("Insert Database URL:\n")
    database_id = DB_URL.split('?')[0].split('/')[-1]
    NOTION_TOKEN = input("Insert secret token for your integration:\n")

    header =[database_id,NOTION_TOKEN]
    writer.writerow(header)
    f.close()

    print("You're all set-up now! Enjoy using you Investment Tracker script.\n")
    print("************************************************************************")
    print("************************************************************************")

    input("Press ANY key to close the script now and run it whenever you want to sync your investment data.")

    quit()

os.environ['NOTION_TOKEN'] = NOTION_TOKEN
notion = Client(auth=os.environ["NOTION_TOKEN"])

database = notion.databases.query(
           **{
            "database_id": database_id
            }
       )

results = database['results']
for result in results:
        
    ticker = result['properties']['Stock Ticker']['select']['name']

    ticker_yahoo = yf.Ticker(ticker)
    data = ticker_yahoo.history()
    last_quote = (data.tail(1)['Close'].iloc[0])

    updated_page = notion.pages.update(
            **{
                    "page_id": result['id'], 
                    "properties": {
                            'Current price': { 'number' : last_quote }
                            } 
                    }
                
                )