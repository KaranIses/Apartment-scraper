import re

import scrapy


class ImmoweltSpider(scrapy.Spider):
    name = "immowelt"
    custom_settings = {
        'FEEDS': {
            f'immowelt.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }

    start_urls = [
        'https://www.immowelt.de/liste/berlin-lichtenberg/wohnungen/mieten?ama=60&ami=35&d=true&lids=499908&lids=499909&pma=700&rma=2&rmi=1&sd=DESC&sf=TIMESTAMP&sp=1'
    ]

    def parse(self, response):
        for titles in response.css('div.EstateItem-1c115'):
            yield {
                'Titel': titles.css("h2::text").get(),
                'Adresse': titles.css("div.IconFact-e8a23 span::text").get(),
                'Größe': re.sub("[^0-9,]", "", titles.css("div.KeyFacts-efbce div::text").extract()[1]),
                'Zimmer': re.sub("[^0-9,]", "", titles.css("div.KeyFacts-efbce div::text").extract()[2]),
                'Preis': re.sub("[^0-9,]", "", titles.css("div.KeyFacts-efbce div::text").extract()[0]),
                'Link': f'{titles.css("a::attr(href)").extract_first()}'
            }
