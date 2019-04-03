import jieba.posseg as pseg
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def get_stopped_words():
    words = [line.strip() for line in open("stoppedwords.txt", "r")]
    words.append(" ")
    return words

def extract_words(sentenceList):

    wordlist = []
    #sentenceList = [line.rstrip() for line in f]
    stopped_words = get_stopped_words()
    remain_pos = [line.rstrip() for line in open("remainPos.txt", "r")]
    for txt in sentenceList:
        seg_list_after_stop = []
        seg_list_after_postag = []
        words = pseg.cut(txt)
        for word, pos in words:
            if pos in remain_pos:
                seg_list_after_postag.append(word)
        for word in seg_list_after_postag:
            if word not in stopped_words:
                seg_list_after_stop.append(word)

        wordlist.append(" ".join(seg_list_after_stop))
    return wordlist

def calculate_tfidf(wordlist,sentenceList):
    tfidfDict = {}
    for txt in sentenceList:
        for i in range(len(txt)):
            if txt[i] == "《":
                for j in range(i + 1, len(txt)):
                    if txt[j] == "》":
                        tfidfDict[txt[i + 1:j]] = 2.0
    vectorizer = CountVectorizer()
    word_frequence = vectorizer.fit_transform(wordlist)
    words = vectorizer.get_feature_names()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(word_frequence)
    weight = tfidf.toarray()
    for i in range(len(weight)):
        for j in range(len(words)):
            getWord = words[j]
            getValue = weight[i][j]
            if getValue != 0:
                if getWord not in list(tfidfDict.keys()):
                    tfidfDict.update({getWord: getValue * len(getWord)})
                else:
                    if tfidfDict[getWord]!=2.0:
                       tfidfDict.update({getWord:tfidfDict[getWord]+getValue*len(getWord)})
                    # tfidfDict[getWord] += str.atof(getValue*len(getWord))
                # else:
                #    tfidfDict.update({getWord: getValue*len(getWord)})
    return tfidfDict

def list_to_file(filename,list):
    with open(filename,"w") as f:
        for word in list:
           f.writelines(word+"\n")

def LDA_modify_weight(wordDict):
    topic_words = [word.rstrip() for word in open("LDA_topic_word.txt","r")]
    for word in wordDict.keys():
        if word in topic_words:
            wordDict[word] = wordDict[word]*2
    return wordDict