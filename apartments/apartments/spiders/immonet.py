import scrapy


class ImmonetSpider(scrapy.Spider):
    name = "immonet"
    start_urls = [
        'https://www.immonet.de/immobiliensuche/sel.do?pageoffset=1&listsize=26&objecttype=1&locationname=Berlin&acid'
        '=&actype=&district=7603&district=7604&district=7605&district=7879&ajaxIsRadiusActive=true&sortby=19&suchart'
        '=1&radius=0&pcatmtypes=1_2&pCatMTypeStoragefield=1_2&parentcat=1&marketingtype=2&fromprice=100&toprice=600'
        '&fromarea=35&toarea=60&fromplotarea=&toplotarea=&fromrooms=1&torooms=2&objectcat=-1&wbs=-1&fromyear=&toyear'
        '=&fulltext=&absenden=Ergebnisse+anzeigen'
    ]

    def parse(self, response):
        if not response.css('div.selList.clearfix.sel-bg-gray-lighter'):
            for titles in response.css('main.container-fluid.max-page-width.pos-relative'):
                yield {
                    'Titel': titles.css("h1.headline-250.line-height-normal::text").getall(),
                    'Adresse': titles.css("p.text-100.pull-left::text").getall(),
                    'Groeße': titles.css("div[id=areaid_1]::text").getall(),
                    'Zimmer': titles.css("div[id=equipmentid_1]::text").getall(),
                    'Preis': titles.css("div[id=priceid_4]::text").getall()
                }

        yield from response.follow_all(css='div.flex-grow-1.overflow-hidden.box-25 a', callback=self.parse)
