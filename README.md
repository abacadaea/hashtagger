Hashtagger
==========

Created at HackCMU 2013

Description
-----------

An app which predict hashtags for given tweets
and randomly generates tweets for a given hashtags.
The hashtag prediction uses Naive Bayes treating the words
in the tweet as features.
The sentence generation uses a Markov Chain on individual words,
where the next word is sampled so that 
* words which more frequently follow the
current word in a sentence are weighted more heavily
* words which appear more frequently in a tweet with the
given hashtag are also weighted more heavily

Usage
-----
Run the app with
    python frontend.py
It may take some time to initialize
