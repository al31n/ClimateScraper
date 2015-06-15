#!/usr/bin/python

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from climateWeatherScraper.spiders.MonthlySpider import MonthlySpider
from scrapy.utils.project import get_project_settings
import sys
import os

LOG_DIR = "log"

if len(sys.argv) == 2:
	stationID = sys.argv[1]
	spider = MonthlySpider(stationID)
	settings = get_project_settings()
	crawler = Crawler(settings)
	crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
	crawler.configure()
	crawler.crawl(spider)
	crawler.start()
	if not os.path.exists(LOG_DIR):
		os.makedirs(LOG_DIR)
	log.start(logfile="%s/%s.log" % (LOG_DIR, stationID), loglevel=log.DEBUG)
	reactor.run() # the script will block here until the spider_closed signal was sent
else:
	print "Invalid arguments: %s" % sys.argv
	sys.exit()