import requests
import pandas as pd
import os

CURR_DIR = os.path.abspath(__file__).replace('__init__.py', '')

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
    url = 'https://oldschool.runescape.wiki/?title=Module:GEIDs/data.json&action=raw&ctype=application%2Fjson'
    out = requests.get(url, headers=HEADERS)
    
    newItemsTable = pd.DataFrame.from_dict(out.json(), orient='index') \
                                .reset_index() \
                                .rename(columns={'index':'item', 0:'api_id'}) \

    # Remove the LAST_UPDATE and LAST_UPDATE_F
    newItemsTable.drop(index=[0,1],inplace=True)

    ###############################################
    ### Code until SQL is implemented in Django ###
    ###############################################
    # Dump if file doesnt exist.

    # This part will be replaced by reading in SQL not CSV
    if (not os.path.exists(CURR_DIR + 'db/table.csv')):
        print('here')
        newItemsTable.to_csv(CURR_DIR + 'db/table.csv', index=False)
        itemsTable = newItemsTable.copy()
    else:
        print('found')
        itemsTable = pd.read_csv(CURR_DIR + 'db/table.csv')
    newItemsTable = newItemsTable.copy()

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
    pd.concat([itemsTable, insertQuery]).to_csv(CURR_DIR + 'db/table.csv', index=False)


def testLaunch():
    testUrl = f'prices.runescape.wiki/api/v1/osrs'

    out = requests.get(testUrl, headers=HEADERS)
    print(out.status_code)
    print(out.json())
