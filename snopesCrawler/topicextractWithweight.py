# coding=UTF-8
import nltk
import path
import topicextract
from nltk.corpus import brown
from nltk.stem.wordnet import WordNetLemmatizer
# This is a fast and simple noun phrase extractor (based on NLTK)
# Feel free to use it, just keep a link back to this post
# http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/
# Create by Shlomi Babluki
# May, 2013

# This is our fast Part of Speech tagger
#############################################################################



#


# Main method, just run "python np_extractor.py"
def main():

    sentence = "    Apple CEO Tim Cook wrote an open letter to customers explaining why the company was fighting a court order to unlock an iPhone tied to the San Bernardino attack."
    lmtzr = WordNetLemmatizer()
    #print ("This sentence is about: %s" % ", ".join(result))
    wighttable=dict()
    with open(path.datapath+'countwords.txt', encoding='utf-8', mode='r') as Seenlist3:
        for sentence in Seenlist3:
                word=sentence.split("    ")
                wighttable[word[0]]=word[1]
    with open(path.datapath+'Claim2.txt', encoding='utf-8', mode='w') as Seenlist2:
        with open(path.datapath+'Claim.txt', encoding='utf-8', mode='r') as Seenlist:
            for sentence in Seenlist:
                np_extractor = topicextract.NPExtractor(sentence)
                result = np_extractor.extract(3)
                output=str()
                for re in result:
                    countnum=0
                    for wight in wighttable.keys():
                        if re in wight or lmtzr.lemmatize(re)  in wight:
                           countnum=countnum+int( wighttable[wight])
                output=output+re+" "+str(countnum)+','
                sentence=sentence.replace(u'\xa0',' ').lstrip(u' ')
                Seenlist2.write(sentence)
                Seenlist2.write(output.rstrip(',')+'\n'+'\n')
if __name__ == '__main__':
    main()
