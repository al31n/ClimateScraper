# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ClimateweatherscraperPipeline(object):
#     def process_item(self, item, spider):
#         return item

import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):

	def __init__(self):
		connection = pymongo.MongoClient	(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]

	def process_item(self, item, spider):
		for data in item:
			if not data:
				raise DropItem("Missing data!")
		self.collection.update({
			'stationID': item['stationID'],
			'month': item['month'],
			'year': item['year'],
			'metadata': item['metadata'],
			'dailyData': item['dailyData']
		}, dict(item), upsert=True)
		log.msg("Data added to MongoDB database!", 
			level=log.DEBUG, spider=spider)
		return item