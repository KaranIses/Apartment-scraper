import scrapy


class EbaySpider(scrapy.Spider):
    name = "ebay"
    custom_settings = {
        'FEEDS': {
            f'ebay.json': {
                'format': 'json',
                'overwrite': False
            }
        }
    }

    start_urls = [
        'https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/anzeige:angebote/preis:100:600/c203l3331'
        '+wohnung_mieten.etage_i:1%2C8+wohnung_mieten.qm_d:35%2C60+wohnung_mieten.swap_s:nein+wohnung_mieten'
        '.zimmer_d:1%2C2'
    ]

    def parse(self, response):
        for titles in response.css('article.aditem'):
            yield {
                'Adresse': titles.css("div.aditem-main--top--left::text").getall(),
                'Titel': titles.css("a.ellipsis::text").getall(),
                'Preis': titles.css("p.aditem-main--middle--price::text").getall(),
                'Zusatz': titles.css("p.text-module-end span.simpletag.tag-small::text").getall()
            }
