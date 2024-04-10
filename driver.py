import osrsWikiAPI.grandExchange as osrs
'''
This file is just for testing purposes of testing the OSRS API;
It will be deleted once I launch the Django project.
'''

# print(osrs.get_last24hrs())
print(osrs.get_daily24hrsOverNDays(2))
from datetime import datetime

rn = datetime.now()
# ts = int(datetime.timestamp())

# print(datetime.fromtimestamp(ts))
# for i in range(30):
#     ts -= 3600*24
#     print(datetime.fromtimestamp(ts))

# itemId = str(osrs.itemApiId('Air Rune'))

# itemData = osrs.get_currentItemCost(itemId)
# osrs.currItemFormat(itemId, itemData)
# print('')

# osrs.get_itemPastYrInfo(itemId)