from math import log
import random
import pickle
import numpy

NUM_FILES = 130
MAX_LINES_SHAKESPEARE = 0

hdict = dict ()
count = dict ()
freq = dict ()
words = []


def checkChar (c):
    return (0 <= ord (c) and ord(c) < 128) and (('0'<=c and c<='9') or ('a' <= c and c <='z') or c == '#')

def clean (word):
    ret = filter (checkChar, word)
    ret = ret.encode ("ascii", "ignore")
    return ret

def is_url (word):
    if word [0:4] == "http":
	return True
    return False

def read_shakespeare ():
    numlines = 0
    wordfile = open ('data/shakespeare.txt', 'r')
    if (MAX_LINES_SHAKESPEARE == 0):
	return []

    global words

    words = ["START"]
    for line in wordfile:
	if (numlines > MAX_LINES_SHAKESPEARE):
	    if (words [len (words) - 1] == "START"):
		break
	numlines += 1

	cur_words = line.split ()
	#if len (cur_words) == 0:

	for word in cur_words:
	    if (word [len (word) - 1] == '.'):
		words.append ("END")
		words.append ("START")

	    word_clean = clean (word.lower ())
	    if len (word_clean) > 0:
		words.append (word_clean)
    words.append ("END")
    return words

def read_in (file_addr):
    data = pickle.load (open (file_addr, 'rb'))
    words = []
    global hdict

    for pair in data:
	text = pair [0]
	hashtags = pair [1]
	words.append ("START")

	for hashtag in hashtags:
	    hashtag = clean (hashtag)
	    if hashtag not in hdict:
		hdict [hashtag] = dict ()
	    for word in text:
		if is_url (word):
		    continue
	    
		words.append (clean (word))
		
		#print hashtag, word
		if word in hdict [hashtag]:
		    hdict[hashtag][word] += 1.0
		else:
		    hdict[hashtag][word] = 1.0 
	
	words.append ("END")
    return words

def process (words):
    global count
    for i in range (len (words) - 1):
	if words [i] not in count:
	    count [words [i]] = dict ()
	    freq [words [i]] = 1
	else:
	    freq [words [i]] += 1

	if words [i + 1] in count[words [i]]:
	    count [words[i]][words[i + 1]] += 1.0
	else:
	    count [words[i]][words[i + 1]] = 1.0

def print_dict (d):
    for word in d:
	print d[word], word
    print "\n"

#merge dictionaries
def merge (cur_word, hashtag):
    global count
    global hdict

    if cur_word not in count:
	return hdict [hashtag]
    elif cur_word not in hdict:
	return count [cur_word]

    a = count [cur_word]
    b = hdict [hashtag]

    ret = dict ()
    for word in a:
	ret [word] = a [word]
	if word in b:
	    ret [word] *= b [word] / freq [word]
	else:
	    ret [word] *= .01 / freq [word]

    return ret

def normalize (d):
    weight_sum = 0.0
    for next_word in d:
	weight_sum += d[next_word] 

    for next_word in d:
	d [next_word] /= weight_sum

    return d

def sample (prob):
    p = random.uniform (0,1)

    for word in prob:
	p -= prob [word]
	if p <= 1e-9:
	    return word
    
    return word (len (prob) - 1)

def get_sentence (word, hashtag):
    cur_word = word
    ret = ""

    while (cur_word != "END"):
	if (len (ret) + len (cur_word) + 1 + len (hashtag) > 140):
	    break
	ret = ret + " " + cur_word
	#ret = ret + cur_word

	prob = normalize (merge (cur_word, hashtag))

	#end early
	if (len (ret) > 50):
	    if "END" in prob:
		break
	
	cur_word = sample (prob)

    return ret [1:]

def get_all_data ():
    global words, count, hdict
    words = []
    count = dict ()
    hdict = dict ()

    for i in range (NUM_FILES):
	read_in ('scraper/tweets' + str (i))

    words += read_shakespeare ()
    words += read_in ('csvconvert/yolotweets.csv.pickle')
    #words += read_in ('/csvconvert/iphonetweets.csv.pickle')
    #words += read_in ('/csvconvert/educationtweets.csv.pickle')
    words += read_in ('csvconvert/newstweets.csv.pickle')
    words += read_in ('csvconvert/syriatweets.csv.pickle')
    #words += read_in ('/csvconvert/economytweets.csv.pickle')

    process (words)

    pickle.dump (hdict, open ('sentGen/hdict.pickle', 'wb'))
    pickle.dump (count, open ('sentGen/count.pickle', 'wb'))
    print len (hdict)
    print len (count)

def load_data ():
    global count
    global hdict
    count = pickle.load (open ('sentGen/count.pickle', 'rb'))	
    hdict = pickle.load (open ('sentGen/hdict.pickle', 'rb'))
    print len (hdict)
    print len (count)

def generate (cur_hash):
    global hdict

    if (cur_hash not in hdict):
	return cur_hash + " is not a recognized hashtag"

    cur_word = sample (normalize (hdict [cur_hash]))

    result = get_sentence (cur_word, cur_hash) + " " + cur_hash
    #print result
    #print ""
    return result

def generate_multiple (cur_hash, num):
    result = []
    if (num <= 0):
	return "That is not a valid number"

    for i in range (num):
	result.append (generate (cur_hash))

    return result

load_data ()
print "Data finished loading"
#how to deal with nonunicode characters?
