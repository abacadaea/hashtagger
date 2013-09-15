import numpy
from predictor_helper import get_example, run_tests 

num_train = 0
num_words = 0

freq = dict ()
word_hash_freq = dict ()
hcount = dict ()
hprior = dict ()

def add_word (word):
    global freq, num_words

    if word not in freq:
	freq [word] = 0
    freq [word] += 1
    num_words += 1


def train ():
    global num_words, num_train, freq, word_hash_freq, hcount, hprior

    while (True):
	ex = get_example ()
	if (ex == False):
	    break

	num_train += 1 
	text = ex [0]
	hashtags = ex [1]

	if len (text) == 0:
	    text.append ("AAAAAAAAAAAAAAAAA")
	for word in text:
	    for hashtag in hashtags:
		if hashtag not in word_hash_freq:
		    word_hash_freq [hashtag] = dict ()
		
		if word not in word_hash_freq [hashtag]:
		    word_hash_freq [hashtag][word] = 0

		if hashtag not in hcount:
		    hcount [hashtag] = 0
		hcount [hashtag] += 1
		
		word_hash_freq [hashtag][word] += 1
		add_word (word)

	for hashtag in hashtags:
	    if hashtag not in hprior:
		hprior [hashtag] = 0
	    hprior [hashtag] += 1

def set_priors ():
    global hprior, num_train
    for hashtag in hprior:
	hprior [hashtag] = log (float (hprior[hashtag]) / num_train)

def normalize (d):
    weighted_sum = 0
    for word in d:
	weighted_sum += d [word]
    for word in d:
	d [word] = float (d [word]) / float (weighted_sum)

    return d

def predictor_func (example):
    ret = dict (hprior)

    for word in example:
	add_word (word)
	for hashtag in ret:
	    if hashtag not in hprior:
		ret [hashtag] = 1e-7
	    else:
		assert (len (word_hash_freq [hashtag]) > 0)
		hashtag_word_pairs = 1e-7
		if word in word_hash_freq[hashtag]:
		     hashtag_word_pairs = float (word_hash_freq [hashtag][word])

		p_word_given_hashtag = hashtag_word_pairs / hcount [hashtag]
		p_word_given_not_hashtag = (float (freq [word]) - hashtag_word_pairs)/ (num_words - len (example))

		#print p_word_given_hashtag, p_word_given_not_hashtag
		p = ret[hashtag]
		pgood = p * p_word_given_hashtag
		pbad = (1 - p) * p_word_given_not_hashtag

		#print p, p_word_given_not_hashtag, pgood, pbad
		assert (pbad >= 0 and pgood >= 0)

		ret [hashtag] = log (pgood) - log (float (freq [word]) / num_words)
		assert (ret [hashtag] <= 1)

    #for i in ret:
#	if ret[i] > 1:
#	    print i,ret[i]
    for hashtag in ret:
	if ret[hashtag] == 1:
	    ret[hashtag] = 1-1e-7
	if ret[hashtag] == 0:
	    ret[hashtag] = 1e-7

    return normalize (ret)
    
print "Begin Training"
train ()
print "Training Complete"
print "Setting Priors"
set_priors ()
print "Priors Set"
run_tests (predictor_func)
