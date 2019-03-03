# -*- coding: utf-8 -*-
import scrapy
from spider.items import JournalItem
from scrapy.loader import ItemLoader

class JournalsSpider(scrapy.Spider):
    name = 'journals'
    allowed_domains = ['eric.ed.gov']
    start_urls = ['https://eric.ed.gov/?journals']

    custom_settings = {
        'PG_DB': 'scraper',
        'PG_HOST': 'localhost',
        'PG_USER': 'scraper',
        'PG_PASS': 'scraper',
        'PG_TABLE': 'journal'
    }

    def parse(self, response):
        # for each link in this page, parse the journal page
        links = response.css("div p a::attr(href)").getall()

        #commented out till everything is working, only follow 1 link
        #for link in links:
        #    yield response.follow(link, self.parse_journal)

        yield response.follow(links[0], self.parse_journal)

    def parse_journal(self, response):
        links = response.css("div.r_i div.r_t a::attr(href)").getall()

        #commented out till everything is working, only follow 1 link
        # for each link in this page, parse the journal
        #for link in links:
        #    yield response.follow(link, self.parse_journal_impl)
        yield response.follow(links[0], self.parse_journal_impl)

        # now follow the 'next' links on this page  to find more journals
        # next_links = response/css("[id='rrm'] div div a::attr(href)").getall()
        # if(len(next_links) == 1):
            
        #     yield response.follow(next_links[0], parse_journal)
        # else:
        #     yield response.follow(next_links[1], parse_journal)

    def parse_journal_impl(self, response):
        #details = response.css('div#details')

        loader = ItemLoader(item=JournalItem(), response=response)

        loader.add_css('title', 'div.title::text')
        loader.add_css('author', 'div.r_a div::text')
        loader.add_css('journal', 'div.r_a div cite::text')
        loader.add_xpath('doi', '//div[contains(@class, "r_a")]/div[2]/text()')
        loader.add_css('abstract', 'div.abstract::text')
        loader.add_css('keywords', 'div.keywords a::text')        

        #resolve extra details, they are a little wonky
        extra_details = response.css('div#r_colR div')[1]

        extra_dets = {}

        dets = extra_details.css("::text").extract()
        for det in range(0, int(len(dets)/2)):
            field = dets[det*2]
            val = dets[(det*2)+1]
            extra_dets[field] = val.strip()

        item = loader.load_item()
        item['extra_details'] = extra_dets

        yield item





