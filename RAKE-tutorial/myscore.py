from __future__ import absolute_import
from __future__ import print_function
import nltk
import six
__author__ = 'a_medelyan'

import rake
import operator
import re


noun_types = ["NN", "NNP", "NNPS","NNS","PRP"]
verb_types = ["VB","VBD","VBG","VBN", "VBP", "VBZ"]
adjective_types = ["JJ","JJR","JJS"]
gammer_types = [":","$","#"]

stoppath = "SmartStoplist.txt"
clampath='Claim.txt'
rake_object = rake.Rake(stoppath, 3, 1, 1)
with open(clampath , mode='r') as Seenlist:
    for text in Seenlist:
        print ('\n'+text)
        tokens = nltk.word_tokenize(text)
        tags=nltk.pos_tag(tokens)
        tagdic=dict()
        for tag in tags:
            tagdic[tag[0].lower()]=tag[1]
        print (tagdic)

        stopwordpattern = rake.build_stop_word_regex(stoppath)
        sentenceList = rake.split_sentences(text)
        phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern)
        wordscores = rake.calculate_word_scores(phraseList)
        keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)
        print (keywordcandidates)
        tempdict=keywordcandidates.copy()
        for keyword in keywordcandidates.keys():
            wordlist = keyword.split(' ')
            if len(wordlist) !=1:
                score=keywordcandidates[keyword]
                if wordlist[0] in tagdic.keys() and wordlist[1] in tagdic.keys() :
                    if  (tagdic[wordlist[0]] in verb_types) and (tagdic[wordlist[1]] not in verb_types):
                        del tempdict[keyword]
                        tempdict[wordlist[0]]=score
                        tempdict[wordlist[1]]=score

                    if (tagdic[wordlist[0]] not in verb_types) and (tagdic[wordlist[1]] in verb_types):
                        del tempdict[keyword]
                        tempdict[wordlist[0]]=score
                        tempdict[wordlist[1]]=score
                else:
                    if wordlist[0] in tagdic.keys():
                        del tempdict[keyword]
                        tempdict[wordlist[0]]=score
                    else:
                        del tempdict[keyword]
                        tempdict[wordlist[1]]=score
        keywordcandidates=tempdict
        print (keywordcandidates)
        tempdict =keywordcandidates.copy()
        for keyword in keywordcandidates.keys():
            score=keywordcandidates[keyword]
            wordlist = keyword.split(' ')
            if len(wordlist) ==1:
                if keyword not in tagdic.keys():
                    del tempdict[keyword]
                    for keytag in tagdic.keys():
                        if keyword in keytag:
                            tempdict[keytag]=score
                    continue
                if tagdic[keyword] in noun_types:
                    tempdict[keyword]=score+1
                    continue
                if tagdic[keyword] in verb_types:
                    tempdict[keyword]=score+1
                    continue
            else:
                if  (tagdic[wordlist[0]] in noun_types) and (tagdic[wordlist[1]] in noun_types or tagdic[wordlist[1]] in adjective_types):
                    tempdict[keyword]=tempdict[keyword]+1
                    continue
                if  (tagdic[wordlist[1]] in noun_types) and (tagdic[wordlist[0]] in noun_types or tagdic[wordlist[0]] in adjective_types):
                    tempdict[keyword]=tempdict[keyword]+1
        keywordcandidates=tempdict
        print (keywordcandidates)


        sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
        print (sortedKeywords)