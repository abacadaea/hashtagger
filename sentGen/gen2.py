from math import log
from random import choice
from string import ascii_lowercase
import numpy
import pickle

NUM_FILES = 5
MAX_LINES_SHAKESPEARE = 100000

wordfile = open ('../data/shakespeare.txt', 'r')
count = dict ()
hdict = dict ()

def clean (word):
    ret = ""
    for c in word:
	if c in ascii_lowercase:
	    ret = ret + c
    return ret

def is_url (word):
    if word [0:4] == "http":
	return True
    return False

def read_shakespeare ():
    numlines = 0

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


def process (words):
    for i in range (len (words) - 1):
	words [i]
	if words [i] not in count:
	    count [words [i]] = dict ()

	if words [i + 1] in count[words [i]]:
	    count [words[i]][words[i + 1]] += 1.0
	else:
	    count [words[i]][words[i + 1]] = 1.0


words = []

def read_in (file_addr):
    data = pickle.load (open (file_addr, 'rb'))
    for pair in data:
	text = pair [0]
	hashtags = pair [1]
	words.append ("START")

	for hashtag in hashtags:
	    if hashtag not in hdict:
		hdict [hashtag] = dict ()
	    for word in text:
		if is_url (word):
		    continue
	    
		words.append (word)
		
		#print hashtag, word
		if word in hdict [hashtag]:
		    hdict[hashtag][word] += 1.0
		else:
		    hdict[hashtag][word] = 1.0 
	
	words.append ("END")


def print_dict (d):
    for word in d:
	print d[word], word
    print "\n"

#merge dictionaries
def merge (cur_word, hashtag):
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
	    ret [word] *= b [word]
	else:
	    ret [word] *= .01
    #for word in b:
	#if word in ret:
	    #continue
	#ret [word] = 0 * b [word]

    return ret

def normalize (d):
    weight_sum = 0.0
    for next_word in d:
	weight_sum += d[next_word] 

    for next_word in d:
	d [next_word] /= weight_sum
	#print d[next_word],
    #print "\n\n"
    

    return d

def sample (prob):
    p = numpy.random.uniform ()

    for word in prob:
	p -= prob [word]
	if p <= 1e-9:
	    return word

def get_sentence (word, hashtag):
    cur_word = word
    ret = ""

    while (cur_word != "END"):
	if (len (ret) + len (cur_word) + 1 > 140): #hashtags don't count to length?
	    break
	ret = ret + " " + cur_word
	

	prob = normalize (merge (cur_word, hashtag))
	#prob = normalize (count [cur_word])

	#end early
	if (len (ret) > 120):
	    if "END" in prob:
		break
	
	cur_word = sample (prob)

    return ret
 

for i in range (NUM_FILES):
    read_in ('../scraper/tweets' + str (i))

read_shakespeare ()
read_in ('../csvconvert/yolotweets.csv.pickle')
#read_in ('../csvconvert/iphonetweets.csv.pickle')
#read_in ('../csvconvert/educationtweets.csv.pickle')
read_in ('../csvconvert/newstweets.csv.pickle')
read_in ('../csvconvert/syriatweets.csv.pickle')
read_in ('../csvconvert/economytweets.csv.pickle')

process (words)

def generate (cur_hash):
    if (cur_hash not in hdict):
	return cur_hash + " is not a valid hashtag"

    #print_dict (hdict [cur_hash])
    cur_word = sample (normalize (hdict [cur_hash]))

    result = get_sentence (cur_word, cur_hash) + " " + cur_hash
    return result
