import requests
import pandas as pd
import os

CURR_DIR = os.path.abspath(__file__).replace('__init__.py', '')

ItemsTable = None
GLOBAL_DF = None # This will be used for now, will replace with SQL in Django


HEADERS = {
    'user-agent' : "Monster Drop Rates(Resume Project)", # OSRS Wiki requests you set this so they know why you're scrapping. 
}

def itemDatabase():
    '''
    Creates the table for the Items table.
    ['item', 'api_id']
    Where item is the name of the item, and api_id is the id that the rest of the api uses.

    ### Until Django is implemented this will feed into a csv. ###
      
    '''


    ''' Uncomment this when you want to work on the API call again. Stop pinging them lol
    
    url = 'https://oldschool.runescape.wiki/?title=Module:GEIDs/data.json&action=raw&ctype=application%2Fjson'
    out = requests.get(url, headers=HEADERS)
    
    newItemsTable = pd.DataFrame.from_dict(out.json(), orient='index') \
                                .reset_index() \
                                .rename(columns={'index':'item', 0:'api_id'}) \
    
    newItemsTable['check item'] = newItemsTable['item'].str.lower()
    # Remove the LAST_UPDATE and LAST_UPDATE_F
    newItemsTable.drop(index=[0,1],inplace=True)

    ###############################################
    ### Code until SQL is implemented in Django ###
    ###############################################
    # Dump if file doesnt exist.

    # This part will be replaced by reading in SQL not CSV
    if (not os.path.exists(CURR_DIR + 'db/table.csv')):
        newItemsTable.to_csv(CURR_DIR + 'db/table.csv', index=False)
        itemsTable = newItemsTable.copy()
    else:
        itemsTable = pd.read_csv(CURR_DIR + 'db/table.csv')
    newItemsTable = newItemsTable.copy()
    '''
    # Temp code, so I stop calling API on every run.. ###
    itemsTable = pd.read_csv(CURR_DIR + 'db/table.csv') #
    newItemsTable = itemsTable.copy()                   #
    #####################################################

    # Join to find what needs to be inserted.
    df = pd.merge(
        newItemsTable
        , itemsTable
        , on='api_id'
        , how='left'
        , suffixes=("", "_old")
    )
    # Get the data that needs to be added to the .csv
    insertQuery = df[df['item_old'].isna()][['item', 'api_id']]

    # Insert the new data into the Table. (Repalce with SQL)
    # for _, row in df.iterrows():
    #     val = row['item']
    #     api_id = row['api_id']
    #     ItemsTable(item=item, api_id=api_id).save()
    
    # Pandas Version...
    global GLOBAL_DF
    GLOBAL_DF = pd.concat([itemsTable, insertQuery])
    GLOBAL_DF.to_csv(CURR_DIR + 'db/table.csv', index=False)

def itemInDatabase(itemName:str):
    '''
    Function returns either True and the U-ID of the item or -1 if not found.
    '''
    #item = ItemsTable.objects.filter(item=itemName)
    # if (len(queryset)): ....
    global GLOBAL_DF
    val  = GLOBAL_DF[(GLOBAL_DF['check item'] == itemName.lower())]
    if (len(val)):
        return val.values[0][1]
    return -1
