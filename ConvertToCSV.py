from pymongo import MongoClient, ASCENDING
import unicodecsv as csv
import json
import os
import sys

MONGO_CONNECTION = 'localhost'
MONGO_PORT = 27017
MONGO_NAME = 'climateData'
COLLECTION_MONTHLY = 'monthlyData'

if len(sys.argv) is not 2 :
	print "Invalid arguments: %s" % sys.argv
	sys.exit()

stationID = sys.argv[1]

client = MongoClient(MONGO_CONNECTION, MONGO_PORT)
db = client[MONGO_NAME]

monthlyDataCollection = db[COLLECTION_MONTHLY]
stationData = monthlyDataCollection.find({"stationID": stationID}).sort([['year', ASCENDING], ['month', ASCENDING]])

directory = 'data/stationID_%s' % stationID
if not os.path.exists(directory):
    os.makedirs(directory)

metadata = stationData[0]['metadata']
with open('%s/stationID_%s.csv' % (directory, stationID), 'wb') as csvfile:
	fieldnames = stationData[0]['dailyData'][0].keys()
	stationDataWriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
	stationDataWriter.writeheader()
	for monthlyData in stationData:
		for dailyData in monthlyData['dailyData']:
			stationDataWriter.writerow(dailyData)

with open('%s/stationID_%s.csv.meta' % (directory, stationID), 'wb') as metafile:	
	json.dump(metadata, metafile, indent=4)