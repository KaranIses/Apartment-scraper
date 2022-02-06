import scrapy


class DegewoSpider(scrapy.Spider):
    name = "degewo"
    start_urls = [
        'https://immosuche.degewo.de/de/search?size=10&page=1&property_type_id=1&categories%5B%5D=1&lat=&lon=&area'
        '=&address%5Bstreet%5D=&address%5Bcity%5D=&address%5Bzipcode%5D=&address%5Bdistrict%5D=&district=33%2C+46%2C'
        '+3%2C+2%2C+28%2C+29%2C+71%2C+64%2C+4-8%2C+58%2C+60%2C+7%2C+40-67&property_number=&price_switch=true'
        '&price_radio=null&price_from=&price_to=&qm_radio=custom&qm_from=&qm_to=&rooms_radio=custom&rooms_from=1'
        '&rooms_to=2&wbs_required=&order=rent_total_without_vat_asc'
    ]

    def parse(self, response):
        for titles in response.css('article.article-list__item.article-list__item--immosearch'):
            yield {
                'Titel': titles.css("h2.article__title::text").getall(),
                'Adresse': titles.css("span.article__meta::text").getall(),
                'Groeße etc.': titles.css("li.article__properties-item span.text::text").getall(),
                'Preis': titles.css("div.article__price-tag span::text").getall()
            }
