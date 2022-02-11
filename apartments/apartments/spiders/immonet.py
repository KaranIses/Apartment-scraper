import re

import scrapy


class ImmonetSpider(scrapy.Spider):
    name = "immonet"
    custom_settings = {
        'FEEDS': {
            f'immonet.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }

    start_urls = [
        'https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&listsize=26&objecttype=1&locationname=Berlin&acid'
        '=&actype=&city=87372&ajaxIsRadiusActive=false&sortby=19&suchart=2&radius=0&pcatmtypes=1_2&pCatMTypeStoragefi'
        'eld=1_2&parentcat=1&marketingtype=2&fromprice=100&toprice=600&fromarea=35&toarea=60&fromplotarea=&toplotarea'
        '=&fromrooms=1&torooms=2&objectcat=-1&wbs=-1&fromyear=&toyear=&fulltext=&absenden=Ergebnisse+anzeigen'
    ]

    def parse(self, response):
        number_of_objects = int(re.sub("[^0-9]", "", response.css('h1.box-50::text').extract_first()))
        i = 0
        for titles in response.css('div.flex-grow-1.display-flex.flex-direction-column.box-25.overflow-hidden.cursor-hand'):
            yield {
                'Titel': titles.css("a.block.ellipsis.text-225.text-default::attr(title)").extract_first().strip().replace('\n', '').replace('\t', ''),
                'Adresse': re.sub("[^.]*• ", "", titles.css("span.text-100::text").extract_first().strip().replace('\n', '').replace('\t', '')),
                'Größe': re.sub("[^0-9,]", "", titles.css("p.text-250.text-strong.text-nowrap::text").extract_first()),
                'Zimmer': re.sub("[^0-9,]", "", titles.css("p.text-250.text-strong.text-nowrap::text").extract()[2]),
                'Preis': re.sub("[^0-9,]", "", titles.css("span.text-250.text-strong.text-nowrap::text").extract_first()),
                'Link': f'https://www.immonet.de{titles.css("a.block.ellipsis.text-225.text-default::attr(href)").extract_first()}'
            }
            i += 1
            if i == number_of_objects:
                break
