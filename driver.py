import osrsWikiAPI.grandExchange as osrs
'''
This file is just for testing purposes of testing the OSRS API;
It will be deleted once I launch the Django project.
'''


itemId = str(osrs.itemApiId('Air Rune'))

itemData = osrs.get_currentItemCost(itemId)
osrs.currItemFormat(itemId, itemData)
print('')

osrs.get_itemPastYrInfo(itemId)