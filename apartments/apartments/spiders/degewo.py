import re

import scrapy


class DegewoSpider(scrapy.Spider):
    name = "degewo"
    custom_settings = {
        'FEEDS': {
            f'degewo.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }

    start_urls = []

    def parse(self, response):
        for titles in response.css('article.article-list__item.article-list__item--immosearch'):
            yield {
                'Titel': titles.css("h2.article__title::text").get(),
                'Adresse': titles.css("span.article__meta::text").get(),
                'Größe': re.sub("[^0-9,]", "", titles.css("li.article__properties-item span.text::text").extract()[1]),
                'Zimmer': re.sub("[^0-9,]", "", titles.css("li.article__properties-item span.text::text").extract()[0]),
                'Preis': re.sub("[^0-9,]", "", titles.css("div.article__price-tag span::text").extract()[1]),
                'Link': f'https://immosuche.degewo.de{titles.css("a::attr(href)").extract_first()}'
            }
