import scrapy


class ImmoweltSpider(scrapy.Spider):
    name = "immowelt"
    start_urls = [
        'https://www.immowelt.de/liste/berlin-lichtenberg/wohnungen/mieten?ama=60&ami=35&d=true&lids=499908&lids'
        '=499909&pma=700&rma=2&rmi=1&sd=DESC&sf=TIMESTAMP&sp=1 '
    ]

    def parse(self, response):
        for titles in response.css('div.EstateItem-1c115'):
            yield {
                'Titel': titles.css("h2::text").getall(),
                'Adresse': titles.css("div.IconFact-e8a23 span::text").get(),
                'Preis etc.': titles.css("div.KeyFacts-efbce div::text").getall()
            }
