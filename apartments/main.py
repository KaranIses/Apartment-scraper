from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet.task import deferLater

from apartments.apartments.spiders import wbm
from apartments.spiders import ebay
from apartments.spiders import immonet
from apartments.spiders import immowelt
from apartments.spiders import degewo


def sleep(self, *args, seconds):
    return deferLater(reactor, seconds, lambda: None)


process = CrawlerProcess(get_project_settings())


def _crawl(result, spider):
    deferred = process.crawl(spider)
    deferred.addCallback(lambda results: print('Waiting 15 seconds before restart'))
    deferred.addCallback(sleep, seconds=60)
    deferred.addCallback(_crawl, spider)
    return deferred


_crawl(None, ebay.EbaySpider)
_crawl(None, immonet.ImmonetSpider)
_crawl(None, immowelt.ImmoweltSpider)
_crawl(None, degewo.DegewoSpider)
_crawl(None, wbm.WbmSpider)
process.start()
