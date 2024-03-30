import osrsWikiAPI as osrs
'''
This file is just for testing purposes of testing the OSRS API;
It will be deleted once I launch the Django project.
'''

# Setup
osrs.itemDatabase()

itemName = None
itemId = -1
# while (itemId == -1):
#     itemName = input("Search for item: ")
#     itemId = osrs.itemInDatabase(itemName)
# itemName = input("Search for item: ")


itemId = str(osrs.itemInDatabase('Air Rune'))

itemData = osrs.getItemData(itemId)
osrs.currItemFormat(itemId, itemData)