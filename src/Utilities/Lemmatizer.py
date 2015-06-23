__author__ = 'bernhard'

import nltk
from nltk.corpus import wordnet

class Lemmatizer(object):

    def __init__(self):
        l = nltk.WordNetLemmatizer()
        self.__lemmatize = l.lemmatize

    def lemmatize(self, words):
        tokenized = []
        for (word, tag) in nltk.pos_tag(nltk.word_tokenize(words)):
            tokenized.append(self.__lemmatize(
                word=word,
                pos=self.__get_wordnet_tag(tag)
            ))
        return " ".join(tokenized)

    @staticmethod
    def __get_wordnet_tag(treebank_tag):

        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN  # default to NOUN if nothing else matches
