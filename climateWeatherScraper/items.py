# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClimateWeatherScraperItem(scrapy.Item):

	stationID = scrapy.Field()
	month = scrapy.Field()
	year = scrapy.Field()
	metadata = scrapy.Field()
	dailyData = scrapy.Field()

class DailyDataItem(scrapy.Item):
	dateEntry = scrapy.Field()
	maxTemp = scrapy.Field()
	minTemp = scrapy.Field()
	meanTemp = scrapy.Field()
	heatDegDays = scrapy.Field()
	coolDegDays = scrapy.Field()
	totalRain = scrapy.Field()
	totalSnow = scrapy.Field()
	totalPrecipitation = scrapy.Field()
	snowOnGround = scrapy.Field()
	dirOfGust = scrapy.Field()
	speedOfMaxGust = scrapy.Field() 

class dateRangeItem(scrapy.Item):
	recentYear = scrapy.Field()
	recentMonth = scrapy.Field()
	lastYear = scrapy.Field()