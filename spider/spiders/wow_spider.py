# -*- coding: utf-8 -*-
import scrapy


class WowSpider(scrapy.Spider):
    name = 'wow'
    allowed_domains = ['www.worldofwargraphs.com']
    start_urls = [
        'https://www.worldofwargraphs.com/pvp-stats/best-players/deathknight',
        'https://www.worldofwargraphs.com/pvp-stats/best-players/monk',
        'https://www.worldofwargraphs.com/pvp-stats/best-players/druid',
        'https://www.worldofwargraphs.com/pvp-stats/best-players/warlock',
        'https://www.worldofwargraphs.com/pvp-stats/best-players/mage',
        'https://www.worldofwargraphs.com/pvp-stats/best-players/hunter',
        'https://www.worldofwargraphs.com/pvp-stats/best-players/warrior',
        'https://www.worldofwargraphs.com/pvp-stats/best-players/priest',
        'https://www.worldofwargraphs.com/pvp-stats/best-players/paladin',
        'https://www.worldofwargraphs.com/pvp-stats/best-players/demonhunter',
        'https://www.worldofwargraphs.com/pvp-stats/best-players/rogue',
        ]

    def parse(self, response):
        table = response.css('table.data_table')
        all_rows = table.css('tr')
        header = all_rows[0]
        rows = all_rows[1:]

        colIdx = {}

        # create an index for location:headerName
        for index, el in enumerate(header.css('th')):
            header = el.css('::text').get()
            colIdx[index] = header

        #get data from rows
        for row in rows:
            cols = row.css('td')
            row_data = {}
            for idx, col in enumerate(cols):                
                #determine our css extraction based on column name
                headerName = colIdx[idx]
                if(headerName == 'Rank'):
                    colVal = col.css('div::text').get().replace('.','')
                elif(headerName in ('Class', 'Spec')):
                    colVal = col.css('a img::attr(title)').get()
                elif(headerName == 'Race'):
                    colVal = col.css('img::attr(title)').get()
                elif(headerName == 'Score'):
                    colVal = col.css('i::text').get()
                elif(headerName in ('Realm', 'Name')):
                    colVal = col.css('a::text').get()
                else:
                    colVal = col.css('::text').get()

                row_data[headerName] = colVal.strip()

            yield(row_data)

