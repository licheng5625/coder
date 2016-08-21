import path

urlset=set()

with open(path.datapath+'/webpagefortwitter/Tweet_JSON/'+'URLs.txt', mode='r')as Seenlist2:
     for line in Seenlist2:
         line=line.replace("\n",'')
         urlset.add(line)
with open(path.datapath+'/webpagefortwitter/Tweet_JSON/'+'URLs.txt', mode='w')as Seenlist2:
        for url in urlset:
            Seenlist2.write(url+"\n")