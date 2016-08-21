# -*- coding: <utf-8> -*-
import sqlite3

conn = sqlite3.connect('Tweets.db')

conn.execute('''CREATE TABLE IF NOT EXISTS TWEET
       (tweet_id INT IDENTITY(0,1) PRIMARY KEY     NOT NULL,
       contain_photos      int    ,
       contain_photos_url      TEXT    ,
       Forname       TEXT     ,
       Initials    TEXT     ,
       Suffix        TEXT    );''')

conn.execute('''CREATE TABLE IF NOT EXISTS AUTHORS_DESCRIPTIONS
       ( Authors_ID  INT NOT NULL,
       Affiliation   TEXT    NOT NULL ,
       FOREIGN KEY (Authors_ID)  REFERENCES AUTHORS(ID)  ,
       PRIMARY KEY (Authors_ID,Affiliation));''')


conn.execute('''CREATE TABLE IF NOT EXISTS ARTICLES
       (PmID            INT PRIMARY KEY     NOT NULL,
       Title           TEXT    ,
       CreatData        Date);''')

conn.execute('''CREATE TABLE IF NOT EXISTS ARTICLES_TERMS
       ( Article_ID   INT    NOT NULL,
         DescriptorName       TEXT    NOT NULL ,
         QualifierName        TEXT ,
       FOREIGN KEY (Article_ID)  REFERENCES ARTICLES(PmID));''')

conn.execute('''CREATE TABLE IF NOT EXISTS ARTICLES_WRITERS
       ( Article_ID  INT    NOT NULL,
         Authors_ID   INT    NOT NULL ,
       FOREIGN KEY (Article_ID)  REFERENCES ARTICLES(PmID)  ,
       FOREIGN KEY (Authors_ID)  REFERENCES AUTHORS(ID) ,
       PRIMARY KEY (Article_ID,Authors_ID));''')

conn.execute('''CREATE TABLE IF NOT EXISTS JOURNALS
       (ID INTEGER  PRIMARY KEY     ,
       ISSN TEXT,
       Title TEXT);''')

conn.execute('''CREATE TABLE IF NOT EXISTS ARTICLES_PUBLISHER
       (Article_ID   INT    NOT NULL,
       Journal_ID    INT NOT NULL,
       FOREIGN KEY (Journal_ID) REFERENCES JOURNALS(ID),
       FOREIGN KEY (Article_ID)  REFERENCES ARTICLES(PmID)  ,
       PRIMARY KEY (Article_ID,Journal_ID));''')
cur = conn.cursor()
#jounalid=cur.execute("select * from JOURNALS").fetchall()
#query="insert into JOURNALS (ID,Title,ISSN) values(null,'%s','%s') "%('33223','32432423432423423')
#cur.execute("insert into ARTICLES (PmID,Title,CreatData) values('%s','%s','%s')" %('222','myarticle.title','2014-11-11'))

#cur.execute(query)
#conn.commit()
#print(len(cur.execute("select * from AUTHORS ").fetchall()))
#print(len(cur.execute("select * from ARTICLES ").fetchall()))
#print (cur.execute("select * from ARTICLES where pmid ='18074020' ").fetchall())
#print(cur.execute("select * from AUTHORS where Lastname ='Finkelman' ").fetchall())
#print (cur.execute("select Max( coun),id  from (select count(*)as coun, ARTICLES_WRITERS.Article_ID as id from ARTICLES_WRITERS  inner join ARTICLES  on ARTICLES_WRITERS.Article_ID =ARTICLES.PmID group BY ARTICLES_WRITERS.Article_ID )  ").fetchall())



#for line in  cur.execute("select Fullname ,Affiliation from AUTHORS inner join ARTICLES_WRITERS on AUTHORS.id = ARTICLES_WRITERS.Authors_ID inner join ARTICLES on ARTICLES_WRITERS.Article_ID =ARTICLES.PmID inner join AUTHORS_DESCRIPTIONS on AUTHORS_DESCRIPTIONS.Authors_ID=AUTHORS.ID  where Fullname='Tanaka, Shinji' order by Affiliation").fetchall():
   # print (line)
#for line in  cur.execute("select * from AUTHORS inner join AUTHORS_DESCRIPTIONS  on AUTHORS_DESCRIPTIONS.Authors_ID=AUTHORS.ID where Fullname='Tanaka, Shinji'  order by Affiliation").fetchall():
    #print (line)

#for line in cur.execute("select JOURNALS.Title from JOURNALS, JOURNALS as JOURNALS2 where  JOURNALS.ID<>JOURNALS2.ID and JOURNALS.Title = JOURNALS2.Title").fetchall():
#    print (line)
#for line in cur.execute("select AUTHORS.Fullname from AUTHORS, AUTHORS as AUTHORS2 where  AUTHORS.ID<>AUTHORS2.ID and AUTHORS.Fullname = AUTHORS2.Fullname").fetchall():
#    print (line)
print cur.execute("select Fullname from AUTHORS where ID = '1'").fetchone()

print cur.execute("select ID from AUTHORS where Fullname = '%s'"%('jjj')).fetchone()
print cur.execute("select * from ARTICLES where Pmid = 23213211").fetchone()

#print (cur.execute("select Max( coun),name  from (select count(*)as coun, AUTHORS.Fullname as name from ARTICLES_WRITERS  inner join AUTHORS  on ARTICLES_WRITERS.Authors_ID =AUTHORS.ID where ARTICLES_WRITERS.Authors_ID <> 71 group BY ARTICLES_WRITERS.Authors_ID )   ").fetchall())

#print((cur.execute("select * from AUTHORS where Fullname='Tanaka, Shinji'").fetchall()))
