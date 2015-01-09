# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import string
import re
from scrapy.selector import HtmlXPathSelector                                                                       ##needed to import xpath command
from scrapy.shell import inspect_response                                                                           ##needed for Response object
from nbastats.items import TeamStats, Player                                                                  ##needed to import player stats




class NbastatsSpider(scrapy.Spider):
    name = "nbaStats"

    start_urls = [
        "http://espn.go.com/nba/teams"                                                                              ##only start not allowed because had some issues when navigated to team roster pages
        ]
    def parse(self,response):
        items = []                                                                                                  ##array or list that stores TeamStats item
        i=0                                                                                                         ##counter needed for older code

        for division in response.xpath('//div[@id="content"]//div[contains(@class, "mod-teams-list-medium")]'):     
            for team in division.xpath('.//div[contains(@class, "mod-content")]//li'):
                item = TeamStats()
        

                item['division'] = division.xpath('.//div[contains(@class, "mod-header")]/h4/text()').extract()[0]            
                item['team'] = team.xpath('.//h5/a/text()').extract()[0]
                item['rosterurl'] = "http://espn.go.com" + team.xpath('.//div/span[2]/a[3]/@href').extract()[0]
                items.append(item)
                request = scrapy.Request(item['rosterurl'], callback = self.parseWPNow)
                request.meta['play'] = item

                yield request
                
        print(item)      

    def parseWPNow(self, response):
        item = response.meta['play']
        item = self.parseRoster(item, response)
#        item = self.parsePlayer(item, response)
        return item

    def parseRoster(self, item, response):
        players = Player()
        int = 0
        for player in response.xpath("//td[@class='sortcell']"):
            players['name'] = player.xpath("a/text()").extract()[0]
            players['position'] = player.xpath("following-sibling::td[1]/text()").extract()[0]
            players['age'] = player.xpath("following-sibling::td[2]/text()").extract()[0]
            players['height'] = player.xpath("following-sibling::td[3]/text()").extract()[0]
            players['weight'] = player.xpath("following-sibling::td[4]/text()").extract()[0]
            players['college'] = player.xpath("following-sibling::td[5]/text()").extract()[0]
            players['salary'] = player.xpath("following-sibling::td[6]/text()").extract()[0]
            yield players
        item['playerurl'] = response.xpath("//td[@class='sortcell']/a").extract()
        yield item
        print("gurp")

    def parsePlayer(self,item,response):
        
        item['playerurl'] = re.findall(r'"[^"]*"',"".join(item['playerurl']))

        for each in item['playerurl']:
            each = each[1:-1]
            request1 = scrapy.Request(each, callback = self.parsePlayerNow)
            yield request1

    def parsePlayerNow(self, response):
        print(response.xpath('//ul[contains(@class,"player-metadata")]/li[4]/text()'))
        mex = Player()
        mex = self.parsePlaye(mex, response)
        return mex
    def parsePlaye(self, mex, response):
        mex['exp'] = response.xpath('//ul[contains(@class,"player-metadata")]/li[4]/text()').extract
        print(mex['exp'])
