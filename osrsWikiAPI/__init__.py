# import monsterDrops as monsterDrops
import requests
import pandas as pd

HEADERS = {
    'user-agent' : "Monster Drop Rates(Resume Project)", # OSRS Wiki requests you set this so they know why you're scrapping. 
}

def itemDatabase():
    ''' Creates the table '''
    url = 'https://oldschool.runescape.wiki/?title=Module:GEIDs/data.json&action=raw&ctype=application%2Fjson'
    out = requests.get(url, headers=HEADERS)
    
    data = pd.DataFrame.from_dict(out.json(), orient='index').reset_index().rename(columns={'index':'item', 0:'api_id'})
    
    # Todo: Use Pandas to join with database query and add what isn't currently on there.
    # Cols 

def testLaunch():
    testUrl = f'prices.runescape.wiki/api/v1/osrs'

    out = requests.get(testUrl, headers=HEADERS)
    print(out.status_code)
    print(out.json())