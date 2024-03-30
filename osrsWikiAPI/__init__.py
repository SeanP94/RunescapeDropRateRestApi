import requests

def testLaunch():
    testUrl = 'http://services.runescape.com/m=itemdb_rs/bestiary/beastData.json?beastid=89'

    headers = {
        'user-agent' : "Monster Drop Rates(Resume Project)", # OSRS Wiki requests you set this so they know why you're scrapping. 
    }

    out = requests.get(testUrl, headers=headers)

    print(out.status_code)
    print(out.json())