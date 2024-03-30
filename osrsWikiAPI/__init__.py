import requests
import pandas as pd
import os
from datetime import datetime

'''
Functionality of this library:

[X] Get new items from APi
[X] Find Item in API  
[ ] Get item data from API  
[ ] Get last X days from API...         ##                     ### Here
[ ] Store item data from API & possible ^^
[ ] Get last X days from SQLTable and what I dont have ask API ^^^

'''

CURR_DIR = os.path.abspath(__file__).replace('__init__.py', '')
ITEMS = None # This will be used for now, will replace with SQL in Django

HEADERS = {
    'user-agent' : "Monster Drop Rates(Resume Project)", # OSRS Wiki requests you set this so they know why you're scrapping. 
}

# Setups
def itemTableSetup():
    '''
    Creates the table for the Items table.
    ['item', 'id']
    Where item is the name of the item, and id is the id that the rest of the api uses.

    ### Until Django is implemented this will feed into a csv. ###
      
    '''

    #Uncomment this when you want to work on the API call again. Stop pinging them lol
    
    # url = 'https://oldschool.runescape.wiki/?title=Module:GEIDs/data.json&action=raw&ctype=application%2Fjson'
    url = 'https://prices.runescape.wiki/api/v1/osrs/mapping'
    out = requests.get(url, headers=HEADERS)
    
    # newItemsTable = pd.DataFrame.from_dict(out.json(), orient='index') \
    #                             .reset_index() \
    #                             .rename(columns={'index':'item', 0:'id'}) \
    
    newItemsTable = pd.DataFrame.from_dict(out.json())
    newItemsTable['name_check'] = newItemsTable['name'].str.lower()
    # Remove the LAST_UPDATE and LAST_UPDATE_F
    # newItemsTable.drop(index=[0,1],inplace=True)

    ###############################################
    ### Code until SQL is implemented in Django ###
    ###############################################
    # Dump if file doesnt exist.

    # This part will be replaced by reading in SQL not CSV
    if (not os.path.exists(CURR_DIR + 'db/items.csv')):
        newItemsTable.to_csv(CURR_DIR + 'db/items.csv', index=False)
        itemsTable = newItemsTable.copy()
    else:
        itemsTable = pd.read_csv(CURR_DIR + 'db/items.csv')
    newItemsTable = newItemsTable.copy()
    

    # Temp code, so I stop calling API on every run.. ###
    # itemsTable = pd.read_csv(CURR_DIR + 'db/items.csv') #
    # newItemsTable = itemsTable.copy()                   #
    #####################################################

    # Join to find what needs to be inserted.
    df = pd.merge(
        newItemsTable
        , itemsTable
        , on='id'
        , how='left'
        , suffixes=("", "_old")
    )
    # Get the data that needs to be added to the .csv
    insertQuery = df[df['name_old'].isna()][['name', 'id']]

    # Insert the new data into the Table. (Repalce with SQL)
    # for _, row in df.iterrows():
    #     val = row['item']
    #     id = row['id']
    #     ItemsTable(item=item, id=id).save()
    
    # Pandas Version...
    global ITEMS
    ITEMS = pd.concat([itemsTable, insertQuery])
    ITEMS.to_csv(CURR_DIR + 'db/items.csv', index=False)


# Get Info from Item DB
def itemName(itemKey:str):
    '''
    Might not need this if I work with objects but just in case I need it lol.
    '''
    global ITEMS
    val = ITEMS[ITEMS['id'] == int(itemKey)]
    if (len(val)):
        return val.values[0][0]
    return -1

def itemApiId(itemName:str):
    '''
    Function returns either True and the U-ID of the item or -1 if not found.
    '''
    #item = ItemsTable.objects.filter(item=itemName)
    # if (len(queryset)): ....
    global ITEMS
    val  = ITEMS[(ITEMS['name_check'] == itemName.lower())]
    if (len(val)):
        return val.values[0][1]
    return -1

def postgresSearchItem(itemName:str):
    '''
    This function will be built when Postgres is implemented.
    It will use full text search, a feature of Postgres to search for 
    the item and return back possible solutions.
    '''
    pass



# Api Tools
def get_currentItemCost(itemKey:str) :
    url = f'https://prices.runescape.wiki/api/v1/osrs/latest/?id={itemKey}'
    response = requests.get(url, headers=HEADERS)

    print(response.status_code)
    print(response.json()['data'][itemKey])
    return response.json()['data'][itemKey]

def get_itemInformation(itemKey:str):
    pass

# Misc, might delete later
def currItemFormat(itemKey:str, itemData: dict):
    '''
    Used to just format what I anticipate. the output should be.
    '''
    highTime = datetime.fromtimestamp(itemData['highTime'])
    lowTime = datetime.fromtimestamp(itemData['lowTime'])
    
    print(f"Item: {itemName(itemKey)}".ljust(50))
    print(f"Item: {itemData['high']} gp High at {highTime}".ljust(100))
    print(f"Item: {itemData['low']} gp Low at {lowTime}".ljust(100))