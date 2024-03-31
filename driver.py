import osrsWikiAPI as osrs
'''
This file is just for testing purposes of testing the OSRS API;
It will be deleted once I launch the Django project.
'''

# Setup
osrs.itemTableSetup()
# osrs.itemDetailTableSetup()




# itemName = None
# itemId = -1
# # while (itemId == -1):
# #     itemName = input("Search for item: ")
# #     itemId = osrs.itemInDatabase(itemName)
# # itemName = input("Search for item: ")


itemId = str(osrs.itemApiId('Air Rune'))

itemData = osrs.get_currentItemCost(itemId)
osrs.currItemFormat(itemId, itemData)
print('\n\n\n')

osrs.get_itemLastYrInfo(itemId)