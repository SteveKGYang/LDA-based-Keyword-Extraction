import argparse
import re
import tools
'''parser = argparse.ArgumentParser(description='keyword extraction')
#parser.add_argument('-is_training',type=bool,default='False')
#parser.add_argument('-save_dir',type=str,default='checkpoints/')
parser.add_argument('-input_str',type=str)
args = parser.parse_args()'''

input_str = "学习词语词典并返回文档矩阵"
threshold = 1.0
sentence = []
sentence.append(input_str)
word_list = tools.extract_words(sentence)
corpus_word_list = [line.rstrip() for line in open("corpus_word.txt","r")]
corpus_word_list.append(word_list[0])
word_dict = {}
dict = {}
dict = tools.calculate_tfidf(corpus_word_list,sentence)

for word in dict.keys():
    if not re.search(word,input_str)==None:
        word_dict.update({word:dict[word]})
LDAword = [word.rstrip() for word in open("LDA_topic_word.txt","r")]
for word in word_dict.keys():
    if word in LDAword:
        i = word_dict[word]
        word_dict.update({word: i*2})
print("抽得的关键词如下：")
for word in word_dict.keys():
    if word_dict[word]>threshold:
        print(word+" ")
