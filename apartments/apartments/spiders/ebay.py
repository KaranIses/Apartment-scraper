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

    start_urls = [
        'https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/anzeige:angebote/preis:100:600/c203l3331+wohnung_mieten.etage_i:1%2C8+wohnung_mieten.qm_d:35%2C60+wohnung_mieten.swap_s:nein+wohnung_mieten.zimmer_d:1%2C2'
    ]

    def parse(self, response):
        for titles in response.css('article.aditem'):
            yield {
                'Titel': titles.css("a.ellipsis::text").extract_first().strip().replace('\n', '').replace('\t', ''),
                'Adresse': titles.css("div.aditem-main--top--left::text").extract()[1].strip().replace('\n', '').replace('\t', ''),
                'Größe': re.sub("[^0-9,]", "", titles.css("span.simpletag.tag-small::text").extract()[0]),
                'Zimmer': re.sub("[^0-9,]", "", titles.css("span.simpletag.tag-small::text").extract()[1]),
                'Preis': re.sub("[^0-9,]", "", titles.css("p.aditem-main--middle--price::text").extract_first())
            }
