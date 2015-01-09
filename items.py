# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TeamStats(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    team = Field()
    division = Field()
    rosterurl = Field()
    player_desc = Field()
    playerurl = Field()
    pass
    
class Player(Item):
    name = Field()
    position = Field()
    age = Field()
    height = Field()
    weight = Field()
    college = Field()
    salary = Field()
    exp = Field()
    pass

##class PlayerStats(Item):
##    Year = 
##    GP = 
##    GS = 
##    Min = 
##    FGM-A =
##    3PM-A =
##    FTM - A =
##    OR
##    DR
##    AST
##    BLK
##    STL
##    PF
##    TO
##    PTS
##    
##    pass
