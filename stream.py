import urllib2
import pprint
import json
import requests
import time
import ast
import NLProcessor as nlp
from firebase import firebase
from pymongo import MongoClient
import otherAPIs as api

client = MongoClient()
client = MongoClient("mongodb://hophacks-bipartisan-rachitag22.c9users.io:27017")
db = client.Bipartisan
aggregatedDict = {}
def getNewsAPI():
	articles = urllib2.urlopen("https://newsapi.org/v1/sources").read()
	articles = ast.literal_eval(articles)
	articles = articles.items()[1]
	articles = articles[1]
	counter = 0
	for x in range(0, len(articles)):
		articleid = articles[x]['id']
		topic = articles[x]['category']
		if topic == 'entertainment' or (topic == 'gaming') or topic == 'music':
			topic = 'entertainment'
		if topic == 'science-and-nature':
			topic = 'science'
		payload = {'source': articleid, 'apiKey': '6f62a98cbb734492abbdba50a4bdff86', 'sortBy': 'top'}
		r = requests.get('https://newsapi.org/v1/articles', params=payload)
		if str(r.json()['status']) == 'ok':
			presentArticles = json.loads(json.dumps(r.json()['articles']))
			for y in range(0, len(presentArticles)):
				jsonReceived = presentArticles[y]
				title = jsonReceived[u'title']
				author = jsonReceived[u'author']
				url = jsonReceived[u'url']
				credRating = -1
				try:
					locations = nlp.HTMLParser(url)
					for z in range(0, len(locations)):
						location = str(getAddress(str(locations[z])))
						print location
						if location not in aggregatedDict:
							aggregatedDict[location] = []
						listInfo = aggregatedDict[location]
						tempDict = {}
						tempDict['url'] = url
						tempDict['author'] = author
						tempDict['title'] = title
						tempDict['credRating'] = credRating
						tempDict['topic'] = topic
						listInfo.append(tempDict)
						aggregatedDict[location] = listInfo
						pprint.pprint(aggregatedDict)
				except:
					None
def addToDict():
	masterList = api.generateResponse()
	for x in range(0, len(masterList)):
		for y in range(0, len(masterList[x])):
			for z in range(0, 4):
				try:
					locations = nlp.HTMLParser(masterList[x][y][1])
					for z in range(0, len(locations)):
						if locations[z] not in aggregatedDict:
							aggregatedDict[locations[z]] = []
						listInfo = aggregatedDict[locations[z]]
						tempDict = {}
						tempDict['url'] = masterList[x][y][1]
						tempDict['author'] = masterList[x][y][2]
						tempDict['title'] = masterList[x][y][0]
						tempDict['credRating'] = -1
						if x is 0:
							tempDict['topic'] = 'general'
						if x is 1:
							tempDict['topic'] = 'technology'
						if x is 2:
							tempDict['topic'] = 'sports'
						if x is 3:
							tempDict['topic'] = 'business'
						if x is 4:
							tempDict['topic'] = 'entertainment'
						if x is 5:
							tempDict['topic'] = 'science'
						listInfo.append(tempDict)
						aggregatedDict[locations[z]] = listInfo
				except:
					None

def getAddress(toSearch):
	addresses = []
	toSearch = str(toSearch)
	payload = {'address': toSearch, 'components':'administrative_area_level_1', 'key': 'AIzaSyBW5C6SvSUUebg5Atsj3beYMtDgwbIR6PI'}
	r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params=payload)
	json = r.json()[u'results'][0]
	for x in range(len(json[u'address_components']) - 1, len(json[u'address_components']) - 3, -1):
		print str(json[u'address_components'][x][u'short_name'])
		try:
			addresses.append(str(json[u'address_components'][x][u'short_name']))
		except:
			None
	return addressses[len(addresses)-1]

def main():
	getNewsAPI()
	addToDict()



if __name__ == "__main__":
  main()