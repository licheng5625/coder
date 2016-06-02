import findspark
import path
findspark.init(spark_home='/Applications/spark-1.6.1')

from pyspark import SparkContext, SparkConf

from collections import namedtuple
oneline   = namedtuple('keyword', ('key', 'num'))

def getNum(rdd,word):#return the sum up
    return rdd.filter(lambda v1:"apple" in v1[0]).map(lambda v1: v1[1]).sum()


def filtermap(word,vector):
    newve=list()
    for se in vector:
        if word in se[0]:
            newve.append(se)
    return newve
def merge(v1,v2):
    print (v1)
    print (v2)
    if(v1 is None) and v2 is None:
        return v1
    if (v1 is None):
        return v2
    if (v2 is None):
        return v1
    else:
        return (v1[0],v1[1]+v2[1])
conf = SparkConf().setAppName("Spark Count")
sc = SparkContext(conf=conf)

wordcountnum=namedtuple('wordcount','word num key')
def creattuple(v1,v2,keyword=None):
    return wordcountnum(word=v1,num=v2,key=keyword)
def creattuple2(v1,keyword):
    dddd=list()
    for keyw in v1:
        wordcountnum(word=keyw[0],num=keyw[1],key=keyword)
        dddd.append(wordcountnum)
    return dddd
dict2={"apple3": 2, "apples pie": 7, "car": 2, "apple": 4, "storm": 3}
dict3=["apple","car","storm"]
map3 =sc.textFile(path.datapath+'test.txt').flatMap(lambda line:(line.split(" "))).distinct()
print (map3.collect())
map1 =sc.parallelize(dict2).map(lambda v1:(v1,dict2[v1]))

map2 = sc.parallelize(dict3)
map2=map2.cartesian(map1).filter(lambda v1:v1[0] in v1[1][0])
print(map2.collect())
map2=map2.reduceByKey(lambda v1,v2:merge(v1,v2)).map(lambda v1:(v1[0],v1[1][1]))
print(map2.collect())

rddput = sc.parallelize(dict2).map(lambda v1:(v1,dict2[v1])).filter(lambda v1:"apple" in v1[0]).map(lambda v1: v1[1]).sum()
#rddput= 13 it works fine for one word 'apple'

#rdd1 = sc.parallelize(dict2).map(lambda v1:(v1,dict2[v1]))
#if I want to use the second RDD combines with tht first one like blow it cause error
#rdd2 = sc.parallelize(dict3).map(lambda v1:(v1,getNum(rdd1,v1)))
#Exception: It appears that you are attempting to broadcast an RDD or reference an RDD from an action or transformation.
#  RDD transformations and actions can only be invoked by the driver,
#  not inside of other transformations; for example, rdd1.map(lambda x: rdd2.values.count() * x) is invalid because the
# values transformation and count action cannot be performed inside of the rdd1.map transformation. For more information,
#  see SPARK-5063.
