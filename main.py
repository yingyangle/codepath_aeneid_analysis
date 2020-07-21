#!/Users/christine/anaconda3/bin/python
# -*- coding: utf-8 -*-
# https://github.com/GITenberg/Aeneidos_227
# http://kyle-p-johnson.com/assets/most-common-latin-words.txt

import os, re, random
from nltk import word_tokenize
from collections import Counter

# define Book class
class Book():
    def __init__(self, filename='aeneid.txt'):
        # get most common words in this book's language
        with open('most_common_words_latin.txt', 'r') as ein:
            self.most_common_words_latin = ein.read().strip().split()
        # get book text
        with open((filename), 'r') as ein:
            # raw text as str
            self.text = ein.read().strip().lower()
            # list of chapters as strs
            self.chapters = re.split(r'\n\s*liber \S+\n', self.text)
            # tokenized text
            self.tokens = word_tokenize(self.text)
            # tokenized chapters
            self.chapter_tokens = [word_tokenize(x) for x in self.chapters]
            # get rid of punctuation 
            self.tokens = [x for x in self.tokens if re.match(r'[a-zA-Z0-9]', x)]
            self.chapter_tokens = [[x for x in chapter if re.match(r'[a-zA-Z0-9]', x)] for chapter in self.chapter_tokens]
            # word counts
            self.counts = Counter(self.tokens)
    
    # get total number of words in book
    def getTotalNumberOfWords(self):
        return len(self.tokens) 

    # get total number of unique words in book
    def getTotalUniqueWords(self):
        return len(set(self.tokens))
    
    # get n most frequent words in book
    def get20MostFrequentWords(self, n=20):
        return [list(x) for x in self.counts.most_common(n)]
    
    # get n most frequent words in book, ignoring m most frequent words in language
    def get20MostInterestingFrequentWords(self, n=20, m=100):
        interesting_counts = self.counts
        # delete N most common word in language
        for word in self.most_common_words_latin[:m]:
            if word in interesting_counts:
                del interesting_counts[word]
        return [list(x) for x in interesting_counts.most_common(n)]
    
    # get n lease frequent words in book
    def get20LeastFrequentWords(self, n=20):
        return [[x, self.counts[x]] for x in list(self.counts)[::-1][:n]]
    
    # get top n words for each chapter
    def get20MostFrequetWordsPerChapter(self, n=20):
        counters = [Counter(x) for x in self.chapter_tokens]
        return [c.most_common(n) for c in counters]
    
    # get number of times a word appears in each chapter
    def getFrequencyOfWord(self, word):
        return [x.count(word.lower()) for x in self.chapter_tokens]
    
    # get chapter number of the first chapter in which the quote appears
    def getChapterQuoteAppears(self, quote):
        quote = quote.lower()
        for i,chapter in enumerate(self.chapters):
            if quote in chapter: return i + 1
        return -1
    
    # generate a sentence using bigrams in the text
    def generateSentence(self):
        sent_words = ['hic']
        for j in range(19):
            # indices of potential next words
            indices = [i+1 for i,word in enumerate(self.tokens) if word == sent_words[-1]]
            next_word = self.tokens[random.choice(indices)]
            sent_words.append(next_word)
        return ' '.join(sent_words)


##### EXECUTE #####

book = Book('aeneid.txt')

print('chapters:', len(book.chapters))
a = book.getTotalNumberOfWords()
print('word count:', a)
a = book.getTotalUniqueWords()
print('unique word count:', a, '\n')

a = book.get20MostFrequentWords(20)
print('most frequent words:', a, '\n')
a = book.get20MostInterestingFrequentWords(n=20, m=100)
print('most frequent interesting words:', a, '\n')
a = book.get20LeastFrequentWords(20)
print('least frequent words:', a, '\n')

a = book.getFrequencyOfWord('Dido')
print('word frequency: Dido', a,'\n')

a = book.getChapterQuoteAppears('Flectere si nequeo superos, Acheronta movebo')
print('quote: Flectere si nequeo superos, Acheronta movebo\nquote found in book', a,'\n')

a = book.generateSentence()
print('generated sentence:', a)









