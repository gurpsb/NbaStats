# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy                                                                                                           
from scrapy.selector import HtmlXPathSelector                                                                       ##needed to import xpath command
from scrapy.shell import inspect_response                                                                           ##needed for Response object
from nbastats.items import TeamStats, PlayerStats                                                                   ##needed to import player stats




class NbastatsSpider(scrapy.Spider):
    name = "nbaStats"

    start_urls = [
        "http://espn.go.com/nba/teams"                                                                              ##only start not allowed because had some issues when navigated to team roster pages
        ]
    def parse(self,response):
        items = []                                                                                                  ##array or list that stores TeamStats item
        i=0                                                                                                         ##counter needed for older code
##        for sel in response.xpath(mex):
##            item = TeamStats()
##            item['team'] = sel.xpath(mex + "/div/h5/a/text()")[i]
##            item['division'] = sel.xpath("//div[@class='span-6']/div[@class='span-4']/div/div/div/div[1]/h4")
##
##            items.append(item)
##            i=i+1
##        return items
        for division in response.xpath('//div[@id="content"]//div[contains(@class, "mod-teams-list-medium")]'):     
            for team in division.xpath('.//div[contains(@class, "mod-content")]//li'):
                item = TeamStats()
        
                play = PlayerStats()
                item['division'] = division.xpath('.//div[contains(@class, "mod-header")]/h4/text()').extract()[0]            
                item['team'] = team.xpath('.//h5/a/text()').extract()[0]
                item['rosterurl'] = "http://espn.go.com" + team.xpath('.//div/span[2]/a[3]/@href').extract()[0]

                request = scrapy.Request(item['rosterurl'], callback = self.parseRoster)
                request.meta['play']=play

                yield request
                
                items.append(item)
##        return item                                                                                               ##use this to extract team stats when i don't yield request                                              

##    def parseRoster(self, response):
##        play = response.meta['play']
##        players1 = []
##        int = 0
##        for players in response.xpath("//td[@class='sortcell']"):
##
##            play['name'] = players.xpath("a/text()").extract()[0]
##            play['position'] = players.xpath("following-sibling::td[1]").extract()[0]
##            play['age'] = players.xpath("following-sibling::td[2]").extract()[0]
##            play['height'] = players.xpath("following-sibling::td[3]").extract()[0]
##            play['weight'] = players.xpath("following-sibling::td[4]").extract()[0]
##            play['college'] = players.xpath("following-sibling::td[5]").extract()[0]
##            play['salary'] = players.xpath("following-sibling::td[6]").extract()[0]
##            print(play)
##            players1.append(play)
##            print(players1)
##        
##        return players1
    def parseRoster(self, response):
        play_original = response.meta['play']
        players1 = []
        int = 0
        for players in response.xpath("//td[@class='sortcell']"):

            play = play_original.copy()

            play['name'] = players.xpath("a/text()").extract()[0]
            play['position'] = players.xpath("following-sibling::td[1]").extract()[0]
            play['age'] = players.xpath("following-sibling::td[2]").extract()[0]
            play['height'] = players.xpath("following-sibling::td[3]").extract()[0]
            play['weight'] = players.xpath("following-sibling::td[4]").extract()[0]
            play['college'] = players.xpath("following-sibling::td[5]").extract()[0]
            play['salary'] = players.xpath("following-sibling::td[6]").extract()[0]
            players1.append(play)

        return players1
            
