from scrapy.spider import *
from scrapy.selector import HtmlXPathSelector
from climateWeatherScraper.items import *
import datetime
import time

class MonthlySpider(Spider):
	name = "ClimateWeatherMonthly"
	
	def __init__(self, stationID=None, *args, **kwargs):
		super(MonthlySpider, self).__init__(*args, **kwargs)
		self.stationID = stationID

	def start_requests(self):
		url_init = "http://climate.weather.gc.ca/climateData/dailydata_e.html?StationID=%s" % self.stationID
		yield scrapy.Request(url_init, self.parse)

	def parse(self, response):
		"""
		Obtain date range and parse data
		"""
		recentYear = response.xpath("//*[@id='Year1']/option[last()]/@value").extract()[0]
		recentMonth = response.xpath("//*[@id='Month2']/option[last()]/@value").extract()[0]
		lastYear = response.xpath("//*[@id='Year1']/option[1]/@value").extract()[0]
		lastMonth = response.xpath
		

		url_template = 'http://climate.weather.gc.ca/climateData/dailydata_e.html?timeframe=1&Prov=&StationID={stationID}&cmdB1=Go&Year={year}&Month={month}'
		currentYear = int(recentYear)
		currentMonth = int(recentMonth)
		while (currentYear >= int(lastYear)):
			while(currentMonth > 0):
				# log.msg("Crawling station %s Month = %s Year = %s" %(stationID, currentMonth, currentYear))
				url = url_template.format(stationID=self.stationID, month=currentMonth, year=currentYear)
				print url
				yield scrapy.Request(url, callback=self.parse_data)
				currentMonth -= 1
			currentMonth = 12
			currentYear -= 1

	def parse_data(self, response):
		# Retrieve Rows for MetaDeta
		metadataTable = response.xpath("//table[@class='margin-bottom-none']/tbody/tr")
		
		# Retrieve station name and province
		stationName = metadataTable[0].xpath('th/b/text()').extract()[0].strip("\r\n").strip()
		stationProv = metadataTable[0].xpath('th/b/text()').extract()[1].strip("\r\n").strip()
		
		# Retrieve latitude, longitude and elevation
		latitudeValue = metadataTable[1].xpath('td/text()').extract()[0:3]
		longitudeValue = metadataTable[1].xpath('td/text()').extract()[4:7]
		elevationValue = metadataTable[1].xpath('td/text()').extract()[8]
		units = metadataTable[1].xpath('td/abbr/text()').extract()

		# format latitude, longitude and elevation into dictionaries
		latitude = {
			"degrees": latitudeValue[0],
			"minute": latitudeValue[1],
			"second": latitudeValue[2],
			"direction": units[3]
		}

		longitude = {
			"degrees": latitudeValue[0],
			"minute": latitudeValue[1],
			"second": latitudeValue[2],
			"direction": units[7]
		}

		elevation = {
			"value": elevationValue,
			"unit": units[8]
		}

		# Retrieve IDs
		ids = map((lambda item: item.strip("<td>").strip("</td>").strip()), metadataTable[2].xpath('td').extract())
		climateID = ids[0]
		WHOID = ids[1]
		TCID = ids[2]

		metadata = {
			"stationName": stationName,
			"stationProv": stationProv,
			"latitude": latitude,
			"longitude": longitude,
			"elevation": elevation,
			"climateID": climateID,
			"WHOID": WHOID,
			"TCID": TCID
		}

		dailyDataList = []
		dataTableRows = response.xpath("//div[@id='dynamicDataTable']/table/tbody/tr[position()>1]")
		for row in dataTableRows:
			dailyData = DailyDataItem()
			# Extract date
			dateString = row.xpath("td/abbr/@title").extract()
			if "Sum" in dateString:
				break
			if len(dateString) == 0:
				continue
			else:
				dailyData["dateEntry"] = datetime.datetime.strptime(str(dateString[0]), "%B %d, %Y")

			# Get rest of data in row
			restOfRow = row.xpath("td[position()>1]/text()|td[position()>1]/a/text()").extract()

			dailyData["maxTemp"] = restOfRow[0]
			dailyData["minTemp"] = restOfRow[1]
			dailyData["meanTemp"] = restOfRow[2]
			dailyData["heatDegDays"] = restOfRow[3]
			dailyData["coolDegDays"] = restOfRow[4]
			dailyData["totalRain"] = restOfRow[5]
			dailyData["totalSnow"] = restOfRow[6]
			dailyData["totalPrecipitation"] = restOfRow[7]
			dailyData["snowOnGround"] = restOfRow[8]
			dailyData["dirOfGust"] = restOfRow[9]
			dailyData["speedOfMaxGust"] = restOfRow[10]

			# Append to list
			dailyDataList.append(dict(dailyData))

		# Create Scraper Item
		monthFromList = dailyDataList[0]["dateEntry"].strftime("%m")
		yearFromList = dailyDataList[0]["dateEntry"].strftime("%Y")
		thisMonth = response.request.url.split("&")[-1].split("=")[1]
		thisYear = response.request.url.split("&")[-2].split("=")[1]

		if len(thisMonth) == 1:
			thisMonth = "0%s" % thisMonth

		if len(dailyDataList) > 0 and thisMonth == monthFromList and thisYear == yearFromList:
			item = ClimateWeatherScraperItem()
			item["metadata"] = metadata
			item["month"] = thisMonth
			item["year"] = thisYear
			item["stationID"] = self.stationID
			item["dailyData"] = dailyDataList
			yield item
		else:
			log.msg("%s, %s, %s, %s not match" %(thisMonth, monthFromList, thisYear, yearFromList), level=log.DEBUG)



			