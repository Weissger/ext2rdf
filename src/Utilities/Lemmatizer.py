__author__ = 'bernhard'

import nltk
from nltk.corpus import wordnet

class Lemmatizer(object):
    """
    Use for easier lemmatizing of a whole sentence or part of sentence.
    """

    def __init__(self):
        l = nltk.WordNetLemmatizer()
        self.__lemmatize = l.lemmatize

    def lemmatize(self, words):
        """
        Returns the given sentence or part of sentence where each word is lemmatized.
        The lemmatizer is the nltk.WordNetLemmatizer and is is pos-tagged before with
        the default pos-tagger from nltk.pos_tag.
        Note that the pos-tagger may give wrong results if the sentence is to short or is only one word.
        :param words: The words to lemmatize
        :type words: str
        :return:
        """
        tokenized = []
        for (word, tag) in nltk.pos_tag(nltk.word_tokenize(words)):
            tokenized.append(self.__lemmatize(
                word=word,
                pos=self.__get_wordnet_tag(tag)
            ))
        return " ".join(tokenized)

    @staticmethod
    def __get_wordnet_tag(treebank_tag):
        """
        Returns the corresponding wordnet tag for the given treebank tag.
        If it can't determine a wordnet tag, it defaults to wordnet.NOUN.
        Example: 'NNS' => wordnet.NOUN
        :param treebank_tag: the treebank tag to convert
        :type treebank_tag: str
        :return:
        """

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
