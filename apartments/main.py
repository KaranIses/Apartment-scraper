import configparser

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
    deferred.addCallback(lambda results: print('Waiting 60 seconds before restart'))
    deferred.addCallback(sleep, seconds=60)
    deferred.addCallback(_crawl, spider)
    return deferred


config_file = configparser.ConfigParser(interpolation=None)
config_file.read("config.ini")
degewo_link = config_file.get('APARTMENTS', 'degewo')
ebay_link = config_file.get('APARTMENTS', 'ebay')
immonet_link = config_file.get('APARTMENTS', 'immonet')
immowelt_link = config_file.get('APARTMENTS', 'immowelt')
wbm_link = config_file.get('APARTMENTS', 'wbm')

if degewo_link != '':
    degewo.DegewoSpider.start_urls = [degewo_link]
    _crawl(None, degewo.DegewoSpider)
if ebay_link != '':
    ebay.EbaySpider.start_urls = [ebay_link]
    _crawl(None, ebay.EbaySpider)
if immonet_link != '':
    immonet.ImmonetSpider.start_urls = [immonet_link]
    _crawl(None, immonet.ImmonetSpider)
if immowelt_link != '':
    immowelt.ImmoweltSpider.start_urls = [immowelt_link]
    _crawl(None, immowelt.ImmoweltSpider)
if wbm_link != '':
    wbm.WbmSpider.start_urls = [wbm_link]
    _crawl(None, wbm.WbmSpider)
process.start()
