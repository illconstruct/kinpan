#/usr/bin/python3
# ldaTopics.py

import time
import re
import csv
import json
import sys

import nltk
import gensim

from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel

from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

from stopwords_custom import list_of_words

# use LDA to guess topics from subtiles
def getTopics(ID, path):
    
    err = 0
    path = path + "/"

    # Get subtitle file
    f = open(path + ID + '.json')
    documents = json.dumps(json.load(f))
    f.close()
 
    words = documents.split()
    p_list = "".join(documents.replace('"','')).replace(',','')
    documents = [p_list]
    n_topics = 1
    n_words = 10

    # List of words to ignore
    stoplist=set(stopwords.words('english'))
    
    stoplist = stopwords.words('english')
    stoplist.extend(list_of_words)
    stoplist=set(stoplist)
    texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

    all_tokens = sum(texts, [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
         for text in texts]

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=n_topics)
    
    # Return LDA topics
    topics = lda.print_topics(num_words=n_words)

    # Convert topics to list
    topic_list = list(topics[0][1].split("+"))
    for idx, i in enumerate(topic_list):
        topic = "".join(re.split("[^a-zA-Z]*", i))
        topic_list[idx] = str(topic)

    return topic_list
