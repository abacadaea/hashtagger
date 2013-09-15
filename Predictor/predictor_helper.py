import numpy, pickle, math
from random import choice

NUM_FILES = 100
freq = dict ()
words = []
examples = []

cur_example = 0
num_train = 100000
num_test = 100
score = 0.0

#utilities
def checkChar (c):
    if 0 <= ord (c) and ord(c) < 128:
	if '0' <= c and c <= '9':
	    return True
	if 'a' <= c and c <= 'z':
	    return True
	    
    return False

def clean (word):
    ret = filter (checkChar, word)
    ret = ret.encode ("ascii", "ignore")
    return ret

def is_url (word):
    if word [0:4] == "http":
	return True
    return False

#input
def read_in (file_addr):
    data = pickle.load (open (file_addr, 'rb'))
    words = []
    global hdict

    for pair in data:
	text = pair [0]
	hashtags = pair [1]

	clean_text = []
	clean_hashtags = []

	for hashtag in hashtags:
	    clean_hashtags.append (clean (hashtag))
	    for word in text:
		if is_url (word):
		    continue
	    
		clean_text.append (clean (word))
	examples.append ([clean_text, clean_hashtags])

def get_all_data ():
    for i in range (NUM_FILES):
	read_in ('scraper/tweets' + str (i))

    read_in ('csvconvert/yolotweets.csv.pickle')
    #read_in ('csvconvert/iphonetweets.csv.pickle')
    #read_in ('csvconvert/educationtweets.csv.pickle')
    #read_in ('csvconvert/newstweets.csv.pickle')
    read_in ('csvconvert/syriatweets.csv.pickle')
    #read_in ('csvconvert/economytweets.csv.pickle')

def get_example ():
    global examples, cur_example, num_train

    if (cur_example >= num_train):
	return False

    ex = examples [cur_example]
    cur_example += 1
    return ex

def test (example, predictor_func):
    global cur_example

    distrib = predictor_func (example)
    
    top_hashtags = []
    for key,value in distrib.iteritems ():
	top_hashtags.append ((value, key))
    top_hashtags = sorted (top_hashtags)
    top_hashtags.reverse ()

    cur_example += 1

    return (top_hashtags [:10], top_hashtags [-10:])

def run_tests (predictor_func):
    global examples, cur_example, score

    while (cur_example < num_train + num_test):
	#ex = examples [cur_example]
	ex = choice (examples)
	test (ex [0], predictor_func)
	print ' '.join (ex[0]), ex [1]
	#if (cur_example % 100 == 0):
	    #print "Average score so far (" + str(cur_example) + " examples):",
	    #print score / cur_example 


get_all_data ()
