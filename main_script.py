# -*- coding: utf-8 -*-
#分词并且遍历停用词表去除停用词-停用词失效，添加句子序号
#from pyltp import SentenceSplitter

from pyltp import SentenceSplitter
inputs = open('E:/360MoveData/Users/jj/Desktop/data/iphoneXR.txt', 'r', encoding='utf-8')
outputs = open('E:/360MoveData/Users/jj/Desktop/data/iphoneXR_sentence.txt', 'w',encoding='utf-8')
a=[]
for line in inputs:
    sents = SentenceSplitter.split(line)
    sents=('\n'.join(sents))
    sents=sents.replace('，','\r\n')
    a.append(sents)
print("分句完成")
outputs.writelines(a)
outputs.close()
inputs.close()
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import Parser
import os
inputs = open('E:/360MoveData/Users/jj/Desktop/data/iphoneXR_sentence.txt', 'r', encoding='utf-8-sig')
LTP_DATA_DIR = r'd:\pyltp\ltp\ltp_data_v3.4.0'   # LTP模型目录路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径， 模型名称为'cws.model'

segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)  # 加载模型
pos=Postagger()
pos_path=os.path.join(LTP_DATA_DIR,"pos.model") #加载词性语料库
pos.load(pos_path)
parser=Parser()
parser_path=os.path.join(LTP_DATA_DIR,"parser.model")
parser.load(parser_path)
sentence_order=[]
words=[]
position=[]
related_word=[]
relation=[]
order=0
word_order=[]
for word in inputs:
    sentence_seged = segmentor.segment(word)
    words_pos = pos.postag(sentence_seged)
    relat = parser.parse(sentence_seged, words_pos)

    str1=(' '.join(sentence_seged))

    for line in str1.splitlines():
        order=order+1
        worder=0
        for i in sentence_seged:
            words.append(' '.join(i))
            sentence_order.append(order)
            worder=worder+1
            word_order.append(worder)
    for j in words_pos:
        position.append(' '.join(j) )
    for arc in relat:
        related_word.append(' '.join("%d" % (arc.head)))
    for arc in relat:
        relation.append(' '.join("%s" % (arc.relation)))
print("分析完成，正在写入文件...")

#print(list(zip(words,position,related_word,relation)))


import pandas as pd
list = [word_order,sentence_order,words, position, related_word,relation]
name = ['word_order','sentence_order','words', 'position', 'related_word','relation']
dataframe = pd.DataFrame({'word_order':word_order,'sentence_order':sentence_order,'words':words,'position':position,'related_word':related_word,'relation':relation})
dataframe.to_csv('E:/360MoveData/Users/jj/Desktop/data/iphoneXR_result.csv',index=False, encoding='utf-8-sig')
print(dataframe)

inputs.close()
segmentor.release()
pos.release()
parser.release()
