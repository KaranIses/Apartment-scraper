import re
import scrapy


class EbaySpider(scrapy.Spider):
    name = "ebay"
    custom_settings = {
        'FEEDS': {
            f'ebay.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }

    start_urls = []

    def parse(self, response):
        for titles in response.css('article.aditem'):
            yield {
                'Titel': titles.css("a.ellipsis::text").extract_first().strip().replace('\n', '').replace('\t', ''),
                'Adresse': titles.css("div.aditem-main--top--left::text").extract()[1].strip().replace('\n', '').replace('\t', ''),
                'Größe': re.sub("[^0-9,]", "", titles.css("span.simpletag.tag-small::text").extract()[0]),
                'Zimmer': re.sub("[^0-9,]", "", titles.css("span.simpletag.tag-small::text").extract()[1]),
                'Preis': re.sub("[^0-9,]", "", titles.css("p.aditem-main--middle--price::text").extract_first()),
                'Link': f'https://www.ebay-kleinanzeigen.de{titles.css("a.ellipsis::attr(href)").extract_first()}'
            }
