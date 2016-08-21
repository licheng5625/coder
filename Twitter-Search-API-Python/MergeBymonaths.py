import findspark
import os
os.environ['LC_ALL'] = 'en_US.UTF-8'


os.environ['LANG'] = 'en_US.UTF-8'
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib

import path
findspark.init(spark_home='/Applications/spark-1.6.1')

from pyspark import SparkContext, SparkConf

import datetime


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



map3 =sc.textFile('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Thailand_Snake_Girl.txt').map(lambda line:(line.split("   ")[0][:7],1)).filter(lambda v1:len(v1[0])==7 and v1[0][:2]=="20").reduceByKey(lambda v1,v2:v1+v2).sortByKey(True,1)
dates=map3.map(lambda v1:datetime.datetime.strptime(v1[0],"%Y-%m")).collect()
times=map3.map(lambda v1:v1[1]).collect()
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator(interval=4)  # every month
daysFmt = mdates.DateFormatter('%Y-%m-%d')
yearsFmt = mdates.DateFormatter('%Y-%m')

fig, ax = plt.subplots()
dates = matplotlib.dates.date2num(dates)

ax.plot_date(dates, times,'-' )

ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)
ax.autoscale_view()

def price(x):
    return   x
ax.fmt_xdata = yearsFmt
ax.fmt_ydata = price
ax.grid(True)

fig.autofmt_xdate()
plt.show()
