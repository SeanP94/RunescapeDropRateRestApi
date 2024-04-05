import requests
import pandas as pd
import os
from datetime import datetime,date

'''
Functionality of this library:

[X] Get new items from APi
[X] Find Item in API  
[X] Get item data from API  
[X] Get last X days from API...         ##                     ### Here
[X] Store item data from API & possible ^^
[X] Get last X days from SQLTable and what I dont have ask API ^^^

'''

CURR_DIR = os.path.abspath(__file__).replace('grandExchange.py', '')
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
    
    # url = 'https://prices.runescape.wiki/api/v1/osrs/mapping'
    # out = requests.get(url, headers=HEADERS)
    # newItemsTable = pd.DataFrame.from_dict(out.json())
    # newItemsTable['name_check'] = newItemsTable['name'].str.lower()


    # ###############################################
    # ### Code until SQL is implemented in Django ###
    # ###############################################
    # # Dump if file doesnt exist.

    # # This part will be replaced by reading in SQL not CSV
    # if (not os.path.exists(CURR_DIR + 'db/items.csv')):
    #     newItemsTable.to_csv(CURR_DIR + 'db/items.csv', index=False)
    #     itemsTable = newItemsTable.copy()
    # else:
    #     itemsTable = pd.read_csv(CURR_DIR + 'db/items.csv')
    # newItemsTable = newItemsTable.copy()
    

    # Temp code, so I stop calling API on every run.. ###
    itemsTable = pd.read_csv(CURR_DIR + 'db/items.csv') #
    newItemsTable = itemsTable.copy()                   #
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
    TODO: Repalce with Django Model functionality.
    Returns the name if the U-ID passed in is valid. Else returns -1 
    '''
    global ITEMS
    val = ITEMS[ITEMS['id'] == int(itemKey)]
    if (len(val)):
        return val.values[0][-2]
    return -1

def itemApiId(itemName:str):
    '''
    Function returns either the U-ID of the item or -1 if not found.
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
    TODO: Just runs pass
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

def get_itemPastYrInfo(itemKey:str):
    '''
    Calls the API to get the last 365 days worth of data.

    To Note* You can pass 5m, 1h, 6h, or 24h on the timestep.
    Im opting to only collect 24h because that's all I really need for what I'm doing.
    '''
    url = f'https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=24h&id={itemKey}'
    out = requests.get(url, headers=HEADERS)

    queriedData = pd.DataFrame.from_dict(out.json()['data'])
    queriedData['item_id'] = int(itemKey)
    queriedData['date'] = queriedData['timestamp'].apply(lambda ts: date.fromtimestamp(ts))
    queriedData.drop(columns=['timestamp'], inplace=True)
    
    currQueriedData = pd.read_csv(CURR_DIR + 'db/price_history.csv')
    ds = set([(x[0], x[1]) for x in currQueriedData[['item_id','date']].values])
    
    mask = queriedData.apply(lambda row: False if (int(row['item_id']), str(row['date'])) in ds else True,axis=1)
    updateData = queriedData[mask].copy()
    # Temp Pandas save.....
    try:
        pd.concat([currQueriedData, updateData]).to_csv(CURR_DIR + 'db/price_history.csv', index=False)
        print('Data Successfully saved.')
    except Exception as e:
        print(f"Error: {e}")


# Misc tools
def currItemFormat(itemKey:str, itemData: dict):
    '''
    Used to just format a print statement of the current data of an item.
    '''
    highTime = datetime.fromtimestamp(itemData['highTime'])
    lowTime = datetime.fromtimestamp(itemData['lowTime'])
    
    print(f"Item: {itemName(itemKey)}".ljust(50))
    print(f"Daily High: {itemData['high']} gp at {highTime}".ljust(100))
    print(f"Daily Low: {itemData['low']} gp at {lowTime}".ljust(100))
