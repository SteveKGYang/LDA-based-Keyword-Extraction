import jieba.posseg as pseg
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

wordlist = []
tfidfDict = {}

with open("sentenceList.txt","r") as f:
    sentenceList = [line.rstrip() for line in f]
    stopped_words = [line.rstrip() for line in open("stoppedwords.txt", "r")]
    remain_pos = [line.rstrip() for line in open("remainPos.txt", "r")]
    for txt in sentenceList:

        for i in range(len(txt)):
            if txt[i]=="《":
                for j in range(i+1,len(txt)):
                    if txt[j]=="》":
                       tfidfDict[txt[i+1:j]] = 2.0
        seg_list_after_stop = []
        seg_list_after_postag = []
        words = pseg.cut(txt)
        for word,pos in words:
            if pos in remain_pos:
                seg_list_after_postag.append(word)
        for word in seg_list_after_postag:
            if word not in stopped_words:
                seg_list_after_stop.append(word)

        wordlist.append(" ".join(seg_list_after_stop))
f.close()
#print("keyword num:",len(wordlist[0].rstrip().split(" ")),len(wordlist[1].rstrip().split(" ")))
vectorizer = CountVectorizer()
word_frequence = vectorizer.fit_transform(wordlist)
words = vectorizer.get_feature_names()
print(words)
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(word_frequence)
#print(tfidf)
weight = tfidf.toarray()
#print(weight)
for i in range(len(weight)):
    for j in range(len(words)):
        getWord = words[j]
        getValue = weight[i][j]
        if getValue != 0:
            if not getWord in list(tfidfDict.keys()):
                tfidfDict.update({getWord: getValue * len(getWord)})
                #tfidfDict[getWord] += str.atof(getValue*len(getWord))
            #else:
            #    tfidfDict.update({getWord: getValue*len(getWord)})
print(tfidfDict)
print(len(tfidfDict))



