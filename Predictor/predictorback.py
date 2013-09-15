import numpy, math
from predictor_helper import get_example, run_tests, clean

num_train = 0
num_words = 0

uni_freq = dict ()
uni_hash_freq = dict ()
hcount = dict ()
hprior = dict ()
h_avg_len = dict ()

def total_length (example):
    return len (' '.join (example))

def add_word (word):
    global uni_freq, num_words

    if word not in uni_freq:
	uni_freq [word] = 0
    uni_freq [word] += 1
    num_words += 1

def add_train (text, hashtag):
    if len (text) == 0:
	return
	#text.append ("AAAAAAAAAAAAAAAAA")

    if hashtag not in hprior:
	hprior [hashtag] = 0
	h_avg_len [hashtag] = 0
    hprior [hashtag] += 1
    h_avg_len [hashtag] += total_length (text)

    for unigram in text:
	if hashtag not in uni_hash_freq:
	    uni_hash_freq [hashtag] = dict ()
	
	if unigram not in uni_hash_freq [hashtag]:
	    uni_hash_freq [hashtag][unigram] = 0

	if hashtag not in hcount:
	    hcount [hashtag] = 0
	hcount [hashtag] += 1
	
	uni_hash_freq [hashtag][unigram] += 1
	add_word (unigram)

def train ():
    global num_words, num_train, uni_freq, uni_hash_freq, hcount, hprior, h_avg_len

    while (True):
	ex = get_example ()
	if (ex == False):
	    break

	num_train += 1 
	text = ex [0]
	hashtags = ex [1]
	for hashtag in hashtags:
	    add_train (text, hashtag)

	    #print text, hashtag, total_length (text)	

def set_priors ():
    global hprior, h_avg_len, num_train
    for hashtag in hprior:
	#print hashtag, h_avg_len [hashtag], hprior [hashtag]
	h_avg_len [hashtag] = float (h_avg_len [hashtag]) / hprior [hashtag]
	assert (h_avg_len != 659.0)
	hprior [hashtag] = math.log (float (hprior[hashtag]) / num_train)

def normalize (d):
    weighted_sum = 0
    for word in d:
	weighted_sum += d [word]
    average = weighted_sum / len (d)
    for word in d:
	d [word] -= average

    return d

def predictor_func (example):
    for unigram in example:
	if (unigram not in hprior):
	    add_train (example, clean (unigram).lower ())
	    assert (unigram in hprior)

    ret = dict (hprior)
    tlen = total_length (example)

    for unigram in example:
	unigram = clean (unigram.lower ())
	add_word (unigram)

	for hashtag in ret:
	    if (unigram == hashtag):
		continue

	    if (hashtag not in hprior) or (hcount [hashtag] < 0):
		ret [hashtag] = -5
	    else:
		assert (len (uni_hash_freq [hashtag]) > 0)
		p_word_given_hashtag = 1e-12
		if unigram in uni_hash_freq[hashtag]:
		     p_word_given_hashtag = float (uni_hash_freq [hashtag][unigram]) / hcount [hashtag]

		#p_word_given_not_hashtag = (float (freq [word]) - hashtag_word_pairs)/ (num_words - len (example))

		ret [hashtag] += math.log (p_word_given_hashtag) #- math.log (float (uni_freq [unigram]) / num_words)

		len_dif = abs (tlen - h_avg_len [hashtag])

		if unigram in uni_hash_freq[hashtag]:
		    print p_word_given_hashtag, uni_freq[unigram], num_words
		    print unigram, hashtag, tlen, h_avg_len [hashtag], len_dif
		ret [hashtag] -= .01 * math.log (1 + len_dif)
		
    print ret ["harvard"]

    return normalize (ret)
