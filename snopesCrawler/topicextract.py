# coding=UTF-8
import nltk
from nltk.corpus import brown
import path
from nltk.stem.wordnet import WordNetLemmatizer

# This is a fast and simple noun phrase extractor (based on NLTK)
# Feel free to use it, just keep a link back to this post
# http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/
# Create by Shlomi Babluki
# May, 2013


# This is our fast Part of Speech tagger
#############################################################################



# This is our semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
#cfg["JJ+NNS"] = "NNS"
cfg["JJ+JJ"] = "JJ"
#cfg["JJ+NN"] = "NNI"
cfg["VBP+VBN"] = "VBX"
cfg["VBP+VBG"] = "VBQ"

#############################################################################
stopword={'any'}

class NPExtractor(object):

    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self,lenofword):

        tokens = self.tokenize_sentence(self.sentence)
        #tags = self.normalize_tags(bigram_tagger.tag(tokens))
        #print (tags)
        tags = nltk.pos_tag(tokens)
        #print (tags)

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                if tags[x][0].lower() in stopword:
                    continue
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break
        lmtzr = WordNetLemmatizer()

        matches = []
        for t in tags:
            if len(t[0])>=lenofword:
                if t[1] == "NNP" or t[1] == "NNI"  or t[1] == "NNS" or  t[1] == "NN":
                #if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                    matches.append(lmtzr.lemmatize(t[0].lower()))
                if t[1] == "VBD" or t[1] == "VBP" or t[1] == "VB":
                    matches.append(lmtzr.lemmatize(t[0].lower(),'v'))
                if t[1]=='VBX' :
                    matches.append(lmtzr.lemmatize(t[0].split()[1].lower(),'v'))

                if t[1]=='VBQ':
                    matches.append(lmtzr.lemmatize(t[0].split()[1].lower(),'v'))
        return matches

def getword(sentence):
        sentence=sentence.replace("\n", "")
        sentence=sentence.replace("[", "")
        sentence=sentence.replace("]", "")
        sentence=sentence.replace("\'s", "")
        sentence=sentence.replace("’s", "")
        sentence=sentence.replace("“", "")
        np_extractor = NPExtractor(sentence)
        result = np_extractor.extract(3)
        #print(result)
        return result
# Main method, just run "python np_extractor.py"
def main():

    sentence = "    Apple CEO Tim Cook wrote an open letter to customers explaining why the company was fighting a court order to unlock an iPhone tied to the San Bernardino attack."
    np_extractor = NPExtractor(sentence)
    #print ("This sentence is about: %s" % ", ".join(result))
    wordcount=dict()
    with open(path.datapath+'countwordsweight.txt', encoding='utf-8', mode='r') as Seenlist3:
            for sentence in Seenlist3:
                word=sentence.split('    ')
                wordcount[word[0]]=word[1].replace('\n','')

    with open(path.datapath+'Claim2.txt', encoding='utf-8', mode='w') as Seenlist2:
        with open(path.datapath+'Claim.txt', encoding='utf-8', mode='r') as Seenlist:
            for sentence in Seenlist:
                result = getword(sentence)
                counter=0
                sumup=0
                filterresult=list()
                for re in result:
                    re=re.replace('\n','')
                    try:
                        num= int(wordcount[re])
                        if num<=2000:
                            sumup =sumup+num
                            counter =counter+1
                            filterresult.append(re)
                    except:
                        pass
                if (not counter ==0) and len(filterresult)>=5:
                    averweight=sumup/counter
                    output=str()
                    for re in filterresult:
                        if int(wordcount[re])<= averweight:
                            output=output+re+'   '+wordcount[re]+','
                    sentence=sentence.replace(u'\xa0',' ').lstrip(u' ')
                    Seenlist2.write(sentence)
                    Seenlist2.write(output.rstrip(',')+'\n')
if __name__ == '__main__':
    main()