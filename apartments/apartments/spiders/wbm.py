import re

import scrapy


class WbmSpider(scrapy.Spider):
    name = "wbm"
    custom_settings = {
        'FEEDS': {
            f'wbm.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }

    start_urls = []

    def parse(self, response):
        for titles in response.css('div.row.openimmo-search-list-item'):
            yield {
                'Titel': titles.css("h2.imageTitle::text").extract_first(),
                'Adresse': titles.css("p.address::text").extract()[0] + ' ' + titles.css("p.address::text").extract()[1],
                'Größe': re.sub("[^0-9,]", "", titles.css("li.main-property div::text").extract()[3]),
                'Zimmer': re.sub("[^0-9,]", "", titles.css("li.main-property div::text").extract()[5]),
                'Preis': re.sub("[^0-9,]", "", titles.css("li.main-property div::text").extract()[1]),
                'Link': f'https://www.wbm.de{titles.css("a.btn.sign::attr(href)").extract_first()}'
            }