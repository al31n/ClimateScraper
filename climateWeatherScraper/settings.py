# -*- coding: utf-8 -*-

# Scrapy settings for climateWeatherScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'climateWeatherScraper'

SPIDER_MODULES = ['climateWeatherScraper.spiders']
NEWSPIDER_MODULE = 'climateWeatherScraper.spiders'


ITEM_PIPELINES = ['climateWeatherScraper.pipelines.MongoDBPipeline', ]

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "climateData"
MONGODB_COLLECTION = "monthlyData"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'climateWeatherScraper (+http://www.yourdomain.com)'
