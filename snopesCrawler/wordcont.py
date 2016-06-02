from __future__ import print_function

import sys
from operator import add
import findspark
findspark.init(spark_home='/Applications/spark-1.6.1')
import re
import sys
import topicextract
import html2text
from pyspark import SparkContext, SparkConf
import path
from nltk.stem.wordnet import WordNetLemmatizer

def remove_emoji(data):
    """
    去除表情
    :param data:
    :return:
    """
    try:
        basestring
    except NameError:
        basestring = str
    if not data:
        return data
    if not isinstance(data, basestring):
        return data

    try:
    # UCS-4
        patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
    # UCS-2
        patt = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
    return patt.sub('', data)

def getword(sentence):
        sentence=html2text.html2text(sentence)
        sentence.lstrip(' ')
        #if len(sentence)>0 and (re.match('^[0-9a-z]+$',sentence[0])) and not sentence[0:2]== 'if' and not sentence[0:3]== 'var':
        if len(sentence)>0 :
            #sentence=remove_emoji(sentence)
            removeword={'\n',"[","]","\'s","’s","“","\\"}
            #for sen in sentence:
            #    if(sen not in removeword):
            #        newsen=newsen+sen
            sentence=sentence.replace("\n", "")
            sentence=sentence.replace("[", "")
            sentence=sentence.replace("]", "")
            sentence=sentence.replace("\'s", "")
            sentence=sentence.replace("’s", "")
            sentence=sentence.replace("“", "")
            np_extractor = topicextract.NPExtractor(sentence)
            result = np_extractor.extract(3)
            return result
        return ''
            #if path =doc

if __name__ == "__main__":

    # create Spark context with Spark configuration
    conf = SparkConf().setAppName("Spark Count")
    sc = SparkContext(conf=conf)
    lmtzr = WordNetLemmatizer()

    #print(lmtzr.lemmatize("Apples"))
    # get threshold
    threshold = 1
    datapath=path.datapath+'./webpages/*.html'
    # read in text file and split each document into words
    #tokenized = sc.textFile(sys.argv[1]).flatMap(lambda line: getword(line))
     # count the occurrence of each word
    wordCounts = sc.textFile(datapath).flatMap(lambda doc: getword(doc)).map(lambda word: (word, 1)).reduceByKey(lambda v1,v2:v1 +v2)

    # filter out words with fewer than threshold occurrences
    #filtered = wordCounts.filter(lambda pair:pair[1] >= threshold)

#    print (filtered.collect())
    with open(path.datapath+'countwords.txt', encoding='utf-8', mode='w') as Seenlist:
        for pari in wordCounts.collect():
            try:
                Seenlist.write(pari[0]+'    '+str(pari[1])+'\n')
            except UnicodeEncodeError:
                pass
    # count characters
    #charCounts = filtered.flatMap(lambda pair:pair[0]).map(lambda c: c).map(lambda c: (c, 1)).reduceByKey(lambda v1,v2:v1 +v2)

    #list = charCounts.collect()
