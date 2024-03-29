# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 12:29:50 2019

@author: jj
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 20:36:54 2019

@author: jj
"""

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import numpy as np
import requests
import json
import csv

def commentSave(list_comment):
    file = open('d:\\python_project\\JDComment_data.csv','w',newline = '',encoding='gbk')
    writer = csv.writer(file)
    writer.writerow(['用户ID','评论内容','会员级别','点赞数','回复数','得分','购买时间','手机型号'])
    for i in range(len(list_comment)):
        writer.writerow(list_comment[i])
    file.close()
    print('存入成功')

def getCommentData(maxPage):
    sig_comment = []
    global list_comment
    cur_page = 0
    while cur_page < maxPage:
        cur_page += 1
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv%s&score=%s&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1'%(proc,i,cur_page)
        try:
            response = requests.get(url=url, headers=headers)
            time.sleep(np.random.rand()*2)
            jsonData = response.text
            startLoc = jsonData.find('{')
            #print(jsonData[::-1])//字符串逆序
            jsonData = jsonData[startLoc:-2]
            jsonData = json.loads(jsonData)
            pageLen = len(jsonData['comments'])
            print("当前第%s页"%cur_page)
            for j in range(0,pageLen):
                userId = jsonData['comments'][j]['id']#用户ID
                content = jsonData['comments'][j]['content']#评论内容
                levelName = jsonData['comments'][j]['userLevelName']#会员级别
                voteCount = jsonData['comments'][j]['usefulVoteCount']#点赞数
                replyCount = jsonData['comments'][j]['replyCount']#回复数目
                starStep = jsonData['comments'][j]['score']#得分
                creationTime = jsonData['comments'][j]['creationTime']#购买时间
                referenceName = jsonData['comments'][j]['referenceName']#手机型号
                sig_comment.append(userId)#每一行数据
                sig_comment.append(content)
                sig_comment.append(levelName)
                sig_comment.append(voteCount)
                sig_comment.append(replyCount)
                sig_comment.append(starStep)
                sig_comment.append(creationTime)
                sig_comment.append(referenceName)
                list_comment.append(sig_comment)
                sig_comment = []
        except:
            time.sleep(5)
            cur_page -= 1
            print('网络故障或者是网页出现了问题，五秒后重新连接')
    return list_comment

if __name__ == "__main__":
    global list_comment
    ua=UserAgent()
    # headers={"User-Agent":ua.random}
    headers = {
    'Accept': '*/*',
    "User-Agent":ua.random,
    'Referer':"https://item.jd.com/100000177760.html#comment"
    }
    #手机四种颜色对应的产品id参数
    productid = ['35216&productId=5089271']
    list_comment = [[]]
    sig_comment = []
    for proc in productid:#遍历产品颜色
        i = 0
        url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv%s&score=%s&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1'%(proc,i,0)
        print(url)
        try:
                response = requests.get(url=url, headers=headers)
                jsonData = response.text
                startLoc = jsonData.find('{')
                jsonData = jsonData[startLoc:-2]
                jsonData = json.loads(jsonData)
                print("最大页数%s"%jsonData['maxPage'])
                getCommentData(jsonData['maxPage'])#遍历每一页
        except:
            i -= 1
            print("wating---")
            time.sleep(5)
                #commentSave(list_comment)
    print("爬取结束，开始存储-------")
    commentSave(list_comment)