from math import log
from random import choice
from string import ascii_lowercase
import numpy

wordfile = open ('../data/shakespeare.txt', 'r')
words = ["START"]

def clean (word):
    ret = ""
    for c in word:
	if c in ascii_lowercase:
	    ret = ret + c
    return ret

for line in wordfile:
    cur_words = line.split ()
    if len (cur_words) == 0:
	words.append ("END")
	words.append ("START")
    for word in cur_words:
	word_clean = clean (word.lower ())
	if len (word_clean) > 0:
	    words.append (word_clean)

words.append ("END")

count = dict ()

for i in range (len (words) - 1):
    if words [i] in count:
	count [words [i]].append (words [i + 1])
    else:
	count [words [i]] = [words[i + 1]]


def normalize (word):
    for word in count:
	weight_sum = 0.0
	for p in count[word]:
	    weight_sum += p [1]
	

def get_sentence (word):
    cur_word = word
    ret = ""

    while (cur_word != "END"):
	ret = ret + " " + cur_word
	next_word = choice (count [cur_word])
	cur_word = next_word

    return ret

