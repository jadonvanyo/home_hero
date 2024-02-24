import asyncio
from twisted.internet import asyncioreactor
asyncioreactor.install(asyncio.get_event_loop())

from datetime import date
from homescraper.spiders.homespider import HomespiderSpider
from homescraper.spiders.rentspider import RentspiderSpider
from homescraper.spiders.taxspider import TaxspiderSpider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings



settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(HomespiderSpider)
    yield runner.crawl(TaxspiderSpider)
    yield runner.crawl(RentspiderSpider)
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished