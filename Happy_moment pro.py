#!/user/bin/env python3
#-*- coding:utf-8 -*-

'''
主要待实现以下功能：
1. 每按回车，就显示一条糗百，开心一下.
2. 输入open再回车，则用默认浏览器打开当前这条糗百
3. 输入q再回车，退出小程序
4. 如输入的是数字，则代表只有>=输入数字点赞数的内容才能显示
5. 过滤掉image/video，只显示纯text的糗事
6. 显示的形式为：当前序号/内容/用户投票信息/当前糗百的Link
 
主要使用的第三方库为requests+lxml+xpath
当前code并未做异常处理，如在网络不通或不畅应该会出现异常报错退出，有兴趣的同学请自行完善。
'''

from lxml import etree
import requests
import os
import webbrowser

class SpideQSBK:

    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
        # 糗事百科页码
        self.pagenum = 2
        # 用于记录当前处于datalist中的位置
        self.curdatalistId = 0
        # 最低点赞数(显示的内容由最低点赞数约束，default=0)
        self.mininumOfZan = 0
        # 糗事内容保存在datalist中
        self.datalist = self.initQSData()
        
    def saveQbrec2Txt(self, qbrecordlist, file):
        for item in range(len(qbrecordlist)):
            if item >= len(qbrecordlist)-2:
                file.write('\n')
            file.write(qbrecordlist[item].replace('\n', ''))
            file.write('\n\n')
    
    # 初始化数据，获取首页的数据
    def initQSData(self):
        # 首页的url
        url = 'https://www.qiushibaike.com'
        # 获取首页的数据
        initdatalist = self.getPageData(url)
        return initdatalist
    
    # 过滤指定url页面的数据
    def getPageData(self, url):
        # 用来保存页面的数据
        pageDataList = []
        r = requests.get(url, headers = self.headers).text
        html = etree.HTML(r)
        
        # 当前页面糗百的数目.
        pageTotalQiubaiNum = len(html.xpath('//div[@id="content-left"]/child::*'))
        # 当前糗百的投票信息
        voteinfo = []
        
        # 将页面数据经过滤后来后pageDataList中
        for i in range(1, pageTotalQiubaiNum):
            filterpre = '//div[@id="content-left"]/div[' + str(i) + ']'
            findfilter = filterpre + '/a/div[@class="content"]/span/text()'
            qiushibaikecontent = html.xpath(findfilter)
        
            # 当前糗百的subpage
            href = html.xpath(filterpre + '/a[@class="contentHerf"]/@href')[0]
            # 投票情况数(点赞数)
            voteinfo = html.xpath(filterpre + '//span[@class="stats-vote"]/i[@class="number"]/text()')
            
            # 过滤掉点赞数不符合要求的记录
            if int(voteinfo[0]) < self.mininumOfZan:
                continue
                
            # 投票情况数(评论数)
            discussNum = html.xpath(filterpre + '//span[@class="stats-comments"]//i[@class="number"]/text()')
            # 将两个list合并
            voteinfo.extend(discussNum)
            voteinfo.insert(0, '点赞: ')
            voteinfo.insert(2, '     评论: ')
            # 将list转化为字符串
            voteinfostr = ''.join(voteinfo)
    
            # 判断当前糗百是否显示不全(如果有查看全文字段则是显示不全)
            isExistViewFulltext = html.xpath(filterpre + '//span[@class="contentForAll"]')
            # 判断当前糗百是否存在图片
            isExistImg = html.xpath(filterpre + '//img[@class="illustration"]')
            # 判断当前糗百是否存在video
            isExistVideo = html.xpath(filterpre + '//video')
            
            # 过滤掉带image和video的糗百
            if len(isExistImg) == 1 or len(isExistVideo) == 1:
                continue
            
            # 如当前糗百显示不全(有查看全文字段)，测需要单独打开这首糗百来获取完整的糗百内容
            urlpre = 'https://www.qiushibaike.com'
            if len(isExistViewFulltext) != 1:
                qiushibaikecontent.append(voteinfostr)
                qiushibaikecontent.append(urlpre + href)
                pageDataList.append(qiushibaikecontent)
            else:
                newUrl = urlpre + href
                newr = requests.get(newUrl, headers = self.headers).text
                newHtml = etree.HTML(newr)
                newqiushicontent = newHtml.xpath('//div[@class="content"]/text()')
                newqiushicontent.append(voteinfostr)
                newqiushicontent.append(newUrl)
                pageDataList.append(newqiushicontent)
                
        return pageDataList   
    
    # 加载非首页的数据,pagenum为列表的页码
    def getNextpageData(self, pageNum):
        url = 'https://www.qiushibaike.com/8hr/page/' + str(pageNum)
        nextdatalist = self.getPageData(url)
        return nextdatalist 
    
    # 获取一个糗百数据
    def getOneHappy(self):
        # 先大第一页开始读记录，如读完了就获取下一页的数据记录. 
        datalistlen = len(self.datalist)-1
        
        # 如果序号要找到，就返回数据，如找不到，则再加载一个页面的数据
        if self.curdatalistId <= datalistlen:
            data = self.datalist[self.curdatalistId]
            # 获取数据后将当前item设置为空，以后占太多的内存空间
            self.curdatalistId = self.curdatalistId + 1
            return data
        else:
            # 将新页面的数据直接加在之前的数据后面
            self.datalist.clear()
            self.datalist = self.getNextpageData(self.pagenum)
            self.pagenum  = self.pagenum + 1
            while len(self.datalist) == 0:
                    self.datalist = self.getNextpageData(self.pagenum)
                    self.pagenum  = self.pagenum + 1

            self.curdatalistId = 0
            return self.datalist[self.curdatalistId]
    
    # 开始嗨皮一下了        
    def startHappy(self):
        print('是时候嗨皮一下了(数据from糗事百科)!!!')
        print('回车键可接着嗨皮, q退出, open用默认浏览器查看当前糗百@_@')
        recordId = 2
        # 直接输出第一条糗百
        happycontent = self.getOneHappy()
        precontent = happycontent
        print(f'\n\n第1条:\n')
        for item in range(len(happycontent)):
            if item == len(happycontent)-2:
                print('\n')
            print(happycontent[item].replace('\n', ''))
            
        while True:
            openurl = happycontent[-1].strip()
            enter = input().strip().lower()
            if enter == 'q':
                break
            elif enter == 'open':
                webbrowser.open(openurl)
            else:
                if enter.isdigit() == True:
                    self.mininumOfZan = int(enter)
                    self.datalist = self.initQSData()
                os.system('cls')
                print('是时候嗨皮一下了(数据from糗事百科)!!!')
                print('回车键可接着嗨皮, q退出, open用默认浏览器查看当前糗百@_@')
                
                happycontent = self.getOneHappy()
                # 有时happycontent会无故为空，如为空，则自动获取下一条，直到不为空为止
                while(len(happycontent) == 0):
                    happycontent = self.getOneHappy()
                # while(cmp(happycontent, precontent) == 0):
                    # happycontent = self.getOneHappy()
                    
                precontent = happycontent
                print('\n')
                print(f'第{recordId}条:\n')
                for item in range(len(happycontent)):
                    if item == len(happycontent)-2:
                        print('\n')
                    print(happycontent[item].replace('\n', ''))
                recordId = recordId + 1
    
if __name__ == '__main__':
    kaixin = SpideQSBK()
    kaixin.startHappy()
