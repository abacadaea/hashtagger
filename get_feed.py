from TwitterAPI import TwitterAPI
from time import gmtime, clock 

consumer_key = 'e3xIgxEQmn3knlbpqEThxw'
consumer_secret = 'KIoFyRhaVRlBOBEsyNDyHg1pSWVC62ADjUpAhyo0kgc'
access_token_key = '1049595348-5rkCP0p2XqiLAGW3VzotzIsDjIuesPxV3DS2x5r'
access_token_secret = 'Xocm1c0cr7X9qnPEqxuhoHlheduiFVxpfsiy889QRg'

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

from TwitterAPI import TwitterAPI
import re
 
def clean(raw):
 
  	#I'm sure most of this can be squished into a couple of lines
  	raw = raw.replace("\'", "")
	raw = re.sub(r'http\S*\s+', '', raw)
	raw = re.sub(r'http\S*$', '', raw)
	raw = re.sub(r'#\S*\s+', '', raw)
	raw = re.sub(r'#\S*$', '', raw)
	raw = re.sub(r'@\S*\s+', '', raw)
	raw = re.sub(r'@\S*$', '', raw)
	raw = re.sub(r'\W+', ' ', raw)
	raw = re.sub(r'\n+', ' ', raw)
	raw = re.sub('[^0-9a-zA-Z ]+', '', raw)
	raw = raw.lower()
 
	return raw

num_result = 0
start_time = gmtime ()

#api.request('search/tweets', {'q':'zzz'})
api.request('statuses/filter', {'languages': 'en', 'locations':'-74,40,-73,41'})
iter = api.get_iterator()
for item in iter:
    if 'text' in item.keys():
	if len (item["entities"]["hashtags"]) > 0:
	    print item ["text"]
	    print item ["entities"]["hashtags"]
	    num_result += 1
	    print num_result, float (num_result) / (gmtime () - start_time)

'''
api.request('statuses/filter', {'locations':'-74,40,-73,41'})
iter = api.get_iterator()
for item in iter:
    print item
    num_result += 1
    print num_result
'''
