# RunescapeDropRateRestApi

An API project for interacting with the OSRS Wiki for Grand Exchange informations.

This project is meant to read their external API and store data. 
The project will be a REST Api that I can interact with, that also has a PostGRES SQL database.

Postgres is going to be optimal, so that I can implement full Text search (Since some things like Home Teleports are called House Teleport Tablets or item states like Willow Shortbow (u) are terrible...)


This tool will allow for me to quickly pull together Item cost data 


# Project Setup 
---
Current State:

Clone Repository from github.

Make sure you have Python downloaded, and virtual environtments (pip install virtualenv)
From the command line type

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

and from there the project is setup 
(This will get a bit more complicated once PostGres and Django are setup, but I'm going to make a docker-compose file, so it shouldn't be too rough)



 Below are just notes for myself.
---
# Get Main Project
https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices



# Figure out the Ask APi for boss drop stuff later?
https://oldschool.runescape.wiki/w/Special:ApiSandbox#action=ask&format=json&query=%5B%5BCategory%3AItems%5D%5D%5B%5BAll%20Item%20ID%3A%3A%2B%5D%5D%7C%3FAll%20Item%20ID%7C%3FCategory%7Climit%3D10&formatversion=2


# Notes:
---
this might be part of how you get the Ask API to work..
'https://oldschool.runescape.wiki/?title=Module:GEIDs/data.json&action=raw&ctype=application%2Fjson'