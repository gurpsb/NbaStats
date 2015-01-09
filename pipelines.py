# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3 as lite
from nbastats.items import TeamStats, Player                                                                  ##needed to import player stats
import re

con = None #this is the db connection object
##it gets created on init and deleted on __del__ just be careful of dependancies
##because del might not be called in that case

class NbastatsPipeline(object):

    def __init__(self):
        self.setupDBCon()
        self.createTables()
        
    def setupDBCon(self):
        self.con = lite.connect('test.db')
        self.cur = self.con.cursor()

    def createTables(self):
        self.dropTeamsTable()
        self.dropPlayersTable()

        self.createTeamsTable()
        self.createPlayersTable()


    def createTeamsTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Teams(P_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, \
            team TEXT, \
            division TEXT \
            )")
        
    def createPlayersTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Players(player_name TEXT, \
            salary TEXT, \
            weight INTEGER, \
            age INTEGER, \
            height TEXT, \
            position TEXT, \
            college TEXT )")
        

    def dropTeamsTable(self):
        self.cur.execute("DROP TABLE IF EXISTS Teams")
    def dropPlayersTable(self):
        self.cur.execute("DROP TABLE IF EXISTS Players")


    def closeDB(self):
        self.con.close()

    def __del__(self):
        self.closeDB()


        
    def storePlayerInfoInDb(self, item):
        self.cur.execute("INSERT INTO Teams(\
            player_name, \
            salary, \
            weight, \
            age, \
            height, \
            position, \
            college \
            ) \
            VALUES( ?, ?, ?, ?, ?, ?, ?)", \
            ( \
            item.get('name', ''),
            item.get('salary', 0),
            item.get('weight', 0),
            item.get('age', 0),
            item.get('height', ''),
            item.get('position', ''),
            item.get('college', '')
            ))
        self.con.commit() 
    
    def process_item(self, item, spider):
        if isinstance(item, TeamStats):
            self.cur.execute("INSERT INTO Teams(\
                team, \
                division \
                ) \
                VALUES( ?, ?)", \
                ( \
                item.get('team', ''),
                item.get('division', 0)
                ))
            self.con.commit()
        if isinstance(item, Player):
            self.cur.execute("INSERT INTO Players(\
                player_name, \
                salary, \
                weight, \
                age, \
                height, \
                position, \
                college \
                ) \
                VALUES( ?, ?, ?, ?, ?, ?, ?)", \
                ( \
                item.get('name', ''),
                re.sub(r'[,$]', "", item.get('salary', 0)),
                item.get('weight', 0),
                item.get('age', 0),
                item.get('height', ''),
                item.get('position', ''),
                item.get('college', '')
                ))
            
            self.con.commit() 
        return item

    #def storeInDb(self, item):
