from selenium import webdriver

from selenium.webdriver.common import keys
import time
from bs4 import BeautifulSoup
bowser =webdriver.Chrome('/Users/licheng5625/PythonCode/masterarbeit/coder/snopesCrawler/chromedriver')
html=bowser.get('https://twitter.com/search?f=tweets&vertical=default&q=(bigfoot AND (corpse OR corpses OR (dead body)) ) &src=typd')
maxerror=10
error=0
lenofhtml=0
for i in range(1,1000):
    bowser.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight," + "document.body.scrollHeight,document.documentElement.clientHeight));");
    time.sleep(0.1)
    if lenofhtml ==len(bowser.page_source):
        error=error+1
        print(error)
        if error >maxerror:
            break
    else:
        error=0
        lenofhtml=len(bowser.page_source)

html=bowser.page_source

soup = BeautifulSoup(html)

