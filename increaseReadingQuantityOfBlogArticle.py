#!/user/bin/env python3
#-*- coding:utf-8 -*-

'''
这是一个有点无聊的项目，因为是闲着无聊，就想着能不能利用爬虫来提高CSDN博文的阅读量呢？
纯属无聊之作，请误非法提高博文阅读量，因为：真实的数据是最感人的
'''

import requests
from lxml import etree
from time import sleep
import time
from multiprocessing import Pool
import os

hrefList = []
titleList = []
# 每个blog待增加浏览的总次数 #请根据实际情况来修改count
count = 2000 
# 博主博文的总页数
pagenum = 1
# 希望浏览量增加的主次数     #请根据实际情况来修改target
target = 30000
# 上网相关的url地址及headers #请根据实际情况来修改url/headers
url = 'https://blog.csdn.net/lxy210781/article/list/1?t=1'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36', 'Cookie': 'uuid_tt_dd=10_19034563310-1531198764165-516661; smidV2=20180713231822eaa9019ff413f2214c9204871b44523900229f439b2c410f0; UN=lxy210781; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=1788*1*PC_VC; dc_session_id=10_1532788986167.796530; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1532786621,1532786960,1532788988,1532820674; UserName=lxy210781; UserInfo=BwfxQ7URpaN5s%2FXpNbVjDpSniJz2s67Cqg6Ilrzk3QYlImEFgZ1mTXRLORYO8g5cFd9rWObqP1dy39p2QQYkNlNwD%2FFJSO9VEqAnAhrmNcBXS9sU5eekv3uQzBBoe%2FNZ; UserNick=%E4%BA%94%E5%8A%9B; AU=424; BT=1532820698393; UserToken=BwfxQ7URpaN5s%2FXpNbVjDpSniJz2s67Cqg6Ilrzk3QYlImEFgZ1mTXRLORYO8g5cFd9rWObqP1dy39p2QQYkNlNwD%2FFJSO9VEqAnAhrmNcDWCRkRccwEFToacHwRrbO1TZmJdVSY3ByizvbMcjpXGH3JjEUdizqVKD%2FJ4XKNtEE%3D; dc_tos=pclo27; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1532820752'}

r = requests.get(url, headers = headers)
html = etree.HTML(r.text)

# 获取时间和日期 
def getnowdatatime(flag = 0):
    '''
    flag = 0为时间和日期         eg:2018-04-11 10:04:55
    flag = 1仅获取日期           eg:2018-04-11
    flag = 2仅获取时间           eg:10:04:55
    flag = 3纯数字的日期和时间   eg:20180411100455 
    '''
    now = time.localtime(time.time())
    if flag == 0:
        return time.strftime('%Y-%m-%d %H:%M:%S', now)
    if flag == 1:
        return time.strftime('%Y-%m-%d', now)
    if flag == 2:
        return time.strftime('%H:%M:%S', now)
    if flag == 3:
        return time.strftime('%Y%m%d%H%M%S', now)

        
# 获取username, 如chinaren
def getusername():
    namelist = os.popen('echo %username%').readlines()
    username = namelist[0].replace("\n", "")
    # 获取当前的username
    return username
    
# 计算当前总共有几页的文章
def getpagenum():
    articletotal = html.xpath('//div[contains(@class, "data-info")]/dl[1]//span[@class="count"]/text()')
    if int(articletotal[0]) <= 20:
        return 1
    else:
        if int(articletotal[0])%20 == 0:
            return int(articletotal[0])//20
        else:
            return int(articletotal[0])//20 + 1
    
    
def initAlldata():
    global hrefList, titleList
    pagenum = getpagenum()
    if pagenum == 1:
        hrefList, titleList = getPageData(url)
    else:
        for i in range(1, pagenum + 1):
            newurl = 'https://blog.csdn.net/lxy210781/article/list/' + str(i) + '?t=1'
            temphreflist, temptitlelist = getPageData(newurl)
            hrefList.extend(temphreflist)
            titleList.extend(temptitlelist)
            
            
def getPageData(pageurl):
    hreflist = []
    titlelist = []
    rPage = requests.get(pageurl, headers = headers).text
    html = etree.HTML(rPage)
    
    hreflist = html.xpath('//div[@class="article-list"]/div[@class="article-item-box csdn-tracking-statistics"]/h4/a/@href')
    titleorignal = html.xpath('//div[@class="article-list"]/div[@class="article-item-box csdn-tracking-statistics"]/h4/a/text()')
        
    for i in range(len(titleorignal)):
        if i % 2 != 0:
            title = titleorignal[i].replace('\n', '').strip()
            titlelist.append(title)
            
    return hreflist, titlelist
    
    
def viewtask(viewhref, viewtitle):
    print(f'当前正在访问文章:\nTitle:{viewtitle}, \nHref:{viewhref}')
    try:
        access = requests.get(viewhref, headers = headers, timeout = 10)
        if access.status_code == 200:
            print(f'访问成功！status_code: {access.status_code}')
            print(f'时间：{getnowdatatime()}\n\n')
    except:
        print('访问异常，请不要担心，访问将继续... ...')
        path = 'C:\\Users\\' + getusername() + '\\Desktop\\temp.txt'
        with open(path, 'a') as f:
            f.write(getnowdatatime())
            f.write('访问异常，请不要担心，访问将继续... ...\n')
        print('*'*50)
    finally:
        if access.status_code != 200:
            sleep(10)
            print('本次访问失效!')


def startviewwebpage():
    articleDict = dict(zip(hrefList, titleList))
    articleNum = len(titleList)
    
    print(f'共有{len(titleList)}篇原创文章待提高阅读量, 请稍候，即将开始提高阅读量！！！\n\n')
    
    for t, h in articleDict.items():
        print(t, '  ', h)
    sleep(5)
    
    rtemp = requests.get(url, headers = headers).text
    htmltemp = etree.HTML(rtemp)
    viewnum = html.xpath('//div[@id="asideProfile"]/div[@class="grade-box clearfix"]/dl[2]/dd/@title')
    viewnum = int(viewnum[0])    
    
    for i in range(1, count + 1):
        os.system('cls')
        print(f'第{i}轮测试：')
        p = Pool(3)
        for href, title in articleDict.items():
            p.apply_async(viewtask, args = (href, title, ))
            # viewtask(href, title)
        p.close()
        p.join()
        
        # print(viewnum)
        viewnum += 24
        print(f'\n第{i}轮所有任务完成! 当前总阅读量{viewnum}次， 还剩{count - i}轮测试。')
        if int(viewnum) >= target:
            print('目标已达成. ')
            break
        i = i + 1
        sleep(5)
           
           
if __name__ == '__main__':
    initAlldata()
    startviewwebpage()
    
    