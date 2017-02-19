import requests

keywords = ['politics', 'us', 'world', 'technology', 'sports', 'business', 'entertainment', 'science', 'health']
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

# format of return will be:
# [general, technology, sports, business, entertainment, science, other]
# OTHER IS A DICTIONARY
# within each element of this list, you will have:
# [name of article, url, provider, description]

def bing_search(query):
    url = 'https://api.cognitive.microsoft.com/bing/v5.0/news?category='+query+'&mkt=en-us'
    # query string parameters
    payload = {'q': query, 'freshness' : 'Week'}
    # custom headers
    headers = {'Ocp-Apim-Subscription-Key': '22207001cbdc4c2487ad91d1cec1bdf2'}
    #22207001cbdc4c2487ad91d1cec1bdf2
    # make GET request
    r = requests.get(url, params=payload, headers=headers)
    # get JSON response
    listOfArticles = r.json()['value']
    masterList = []
    for article in listOfArticles:
    	if('clusteredArticles' in article):
    		information = article['clusteredArticles']
    	else:
    		information = article
    	thisList = []
    	if(type(information) is dict):
	    	thisList.append(article.get('name'))
	    	thisList.append(information['url'])
	    	provider = information['provider'][0]
	    	thisList.append(provider['name'])
	    	thisList.append(str(information['description'].encode("ascii", "ignore")))
		masterList.append(thisList)
    return masterList

def generateResponse():
	politicsList = bing_search('politics')
	usList = bing_search('us')
	worldList = bing_search('world')

	generalList = politicsList + usList + worldList
	techList = bing_search('technology')
	sportsList = bing_search('sports')
	buisnessList = bing_search('business')
	entertainmentList = bing_search('entertainment')
	scienceList = bing_search('science')
	scienceList += bing_search('health')
	otherDict = getAllStates()

	masterList = []

	masterList.append(generalList)
	masterList.append(techList)
	masterList.append(sportsList)
	masterList.append(buisnessList)
	masterList.append(entertainmentList)
	masterList.append(scienceList)
	masterList.append(otherDict)

	return masterList

def generateStates(query):
	finalResult = []
	url = 'https://api.cognitive.microsoft.com/bing/v5.0/news/trendingtopics'
	# query string parameters
	payload = {'q': query}
	# custom headers
	headers = {'Ocp-Apim-Subscription-Key': '028fb806bc014b3baf2426e3ac1292dc '}

	r = requests.get(url, params=payload, headers=headers)

	articles = r.json()['value']
	max = 10
	for article in articles:
		if (max == 0):
			break
		max -= 1
		if(type(article) is dict):
			result = []
			result.append(str(article['name'].encode("ascii", "ignore")))
			result.append(str(article['webSearchUrl'].encode("ascii", "ignore")))
			provider = article['image']['provider']
			result.append(str(provider[0]['name'].encode("ascii", "ignore")))
			result.append('No description available.')
			finalResult.append(result)
	return finalResult


def getAllStates():
	d = {}
	i = 0
	for key, value in states.iteritems():
		d[key] = generateStates(value)

	return d
