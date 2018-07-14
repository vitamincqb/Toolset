#!/user/bin/env python3
#-*- coding:utf-8 -*-

from lxml import etree
from time import sleep
import requests
import os
import webbrowser

from tkinter import *
import tkinter as tk
from tkinter.filedialog import *

class SpideQSBK(Frame):
    def __init__(self, parent = None, **kw):
        Frame.__init__(self, parent, kw)
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
        # 糗事百科页码
        self.pagenum = 2
        # 用于记录当前处于datalist中的位置
        self.curdatalistId = 0
        # 最低点赞数(显示的内容由最低点赞数约束，default=0)
        self.mininumOfZan = 0
        # 糗事内容保存在datalist中
        self.datalist = self.initQSData()
        # Logo图标
        self.photo = PhotoImage(file = r'C:\Users\qbgao\Desktop\happy_moment\qsbk2.gif')
        self.openurl = ''
        # 初始化界面并显示第一条信息
        self.makeUi()

    def list2String(self, list = None):
        str = ''
        for item in range(len(list)):
            if item == len(list)-2:
                str += '\n\n'
            str = str + list[item].replace('\n', '')
        return str
        
    def makeUi(self):
        # 初始化各种widget
        font9 = "-family {Microsoft YaHei UI} -size 12 -weight normal "

        def onBindentry():
            pass
            
        def onGetNextBtn():
            happycontent = self.getOneHappy()
            # 有时happycontent会无故为空，如为空，则自动获取下一条，直到不为空为止
            while(len(happycontent) == 0):
                happycontent = self.getOneHappy()
                
            str = self.list2String(happycontent)
            disContentText.delete('1.0', END)
            disContentText.insert('insert', str)
            self.openurl = happycontent[-1].strip()    
            
        def onOpenUrl():
            webbrowser.open(self.openurl)    
            
        def onCopyContent():
            pass
            
        def onConfirm():
            str = entry.get()
            if entry.get().isdigit() == True:
                self.mininumOfZan = int(str)
                self.datalist = self.initQSData()
            labelZan_1.configure(text = str)

        disContentText = Text()
        disContentText.place(relx=0.01, rely=0.29, relheight=0.58, relwidth=0.98)
        disContentText.configure(background="white")
        disContentText.configure(font="TkTextFont")
        disContentText.configure(foreground="black")
        disContentText.configure(highlightbackground="#d9d9d9")
        disContentText.configure(highlightcolor="black")
        disContentText.configure(insertbackground="black")
        disContentText.configure(selectbackground="#c4c4c4")
        disContentText.configure(selectforeground="black")
        disContentText.configure(width=584)
        disContentText.configure(wrap=WORD)
        
        #当启动应用后先显示第一条糗百
        firstList = self.getOneHappy()
        self.openurl = firstList[-1].strip()
        disContentText.insert('insert', self.list2String(self.getOneHappy()))
        
        entry = Entry()
        entry.bind('<Return>', onBindentry)
        entry.place(relx=0.03, rely=0.89,height=27, relwidth=0.19)
        entry.configure(background="white")
        entry.configure(disabledforeground="#a3a3a3")
        entry.configure(font="TkFixedFont")
        entry.configure(foreground="#000000")
        entry.configure(highlightbackground="#d9d9d9")
        entry.configure(highlightcolor="black")
        entry.configure(insertbackground="black")
        entry.configure(selectbackground="#c4c4c4")
        entry.configure(selectforeground="black")

        nextBtn = Button(command=onGetNextBtn)
        nextBtn.place(relx=0.49, rely=0.89, height=28, width=59)
        nextBtn.configure(activebackground="#d9d9d9")
        nextBtn.configure(activeforeground="#000000")
        nextBtn.configure(background="#d9d9d9")
        nextBtn.configure(disabledforeground="#a3a3a3")
        nextBtn.configure(foreground="#000000")
        nextBtn.configure(highlightbackground="#d9d9d9")
        nextBtn.configure(highlightcolor="black")
        nextBtn.configure(pady="0")
        nextBtn.configure(text="下一条")

        openUrl = Button(command=onOpenUrl)
        openUrl.place(relx=0.66, rely=0.89, height=28, width=59)
        openUrl.configure(activebackground="#d9d9d9")
        openUrl.configure(activeforeground="#000000")
        openUrl.configure(background="#d9d9d9")
        openUrl.configure(disabledforeground="#a3a3a3")
        openUrl.configure(foreground="#000000")
        openUrl.configure(highlightbackground="#d9d9d9")
        openUrl.configure(highlightcolor="black")
        openUrl.configure(pady="0")
        openUrl.configure(text='打开链接')

        copyBtn = Button(command=onCopyContent)
        copyBtn.place(relx=0.82, rely=0.89, height=28, width=59)
        copyBtn.configure(activebackground="#d9d9d9")
        copyBtn.configure(activeforeground="#000000")
        copyBtn.configure(background="#d9d9d9")
        copyBtn.configure(disabledforeground="#a3a3a3")
        copyBtn.configure(foreground="#000000")
        copyBtn.configure(highlightbackground="#d9d9d9")
        copyBtn.configure(highlightcolor="black")
        copyBtn.configure(pady="0")
        copyBtn.configure(text='复制内容')

        firmBtn = Button(comman=onConfirm)
        firmBtn.place(relx=0.24, rely=0.89, height=28, width=59)
        firmBtn.configure(activebackground="#d9d9d9")
        firmBtn.configure(activeforeground="#000000")
        firmBtn.configure(background="#d9d9d9")
        firmBtn.configure(disabledforeground="#a3a3a3")
        firmBtn.configure(foreground="#000000")
        firmBtn.configure(highlightbackground="#d9d9d9")
        firmBtn.configure(highlightcolor="black")
        firmBtn.configure(pady="0")
        firmBtn.configure(text='确认')
        
        Label1 = Label()
        Label1.place(relx=0.01, rely=0.01, height=103, width=197)
        Label1.configure(activebackground="#f9f9f9")
        Label1.configure(activeforeground="black")
        Label1.configure(background="#d9d9d9")
        Label1.configure(disabledforeground="#a3a3a3")
        Label1.configure(foreground="#000000")
        Label1.configure(highlightbackground="#d9d9d9")
        Label1.configure(highlightcolor="black")
        Label1.configure(image=self.photo)
        Label1.configure(relief=RIDGE)
        Label1.configure(text='Label')
        
        labelZan = Label()
        labelZan.place(relx=0.4, rely=0.16, height=43, width=170)
        labelZan.configure(activebackground="#f9f9f9")
        labelZan.configure(activeforeground="black")
        labelZan.configure(background="#d9d9d9")
        labelZan.configure(disabledforeground="#a3a3a3")
        labelZan.configure(font=font9)
        labelZan.configure(foreground="#000000")
        labelZan.configure(highlightbackground="#d9d9d9")
        labelZan.configure(highlightcolor="black")
        labelZan.configure(justify=RIGHT)
        labelZan.configure(text='当前对点赞数的限定:')
        
        labelZan_1 = Label()
        labelZan_1.place(relx=0.67, rely=0.16, height=43, width=77)
        labelZan_1.configure(activebackground="#f9f9f9")
        labelZan_1.configure(activeforeground="black")
        labelZan_1.configure(background="#d9d9d9")
        labelZan_1.configure(disabledforeground="#a3a3a3")
        labelZan_1.configure(font=font9)
        labelZan_1.configure(foreground="#000000")
        labelZan_1.configure(highlightbackground="#d9d9d9")
        labelZan_1.configure(highlightcolor="black")
        labelZan_1.configure(justify=RIGHT)
        labelZan_1.configure(text='0')
    
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
            
            timer = 0
            while len(self.datalist) == 0:
                # 为防止要求的点赞数太高一直查找不到而不断的循环
                if timer >= 10:
                    self.mininumOfZan = 0
                    return ['服务器无响应! 点赞数限制恢复为0, 这是Server端开的一个玩笑，是不是很好笑，我自己都忍不住笑出了声*_*!']
                sleep(0.8)
                timer = timer + 1
                print(f'正在查找数据,第{timer}次... ...')
                self.datalist = self.getNextpageData(self.pagenum)
                self.pagenum  = self.pagenum + 1

            self.curdatalistId = 0
            return self.datalist[self.curdatalistId]    

if __name__ == '__main__':
    root = Tk()
    root.title('糗事百科')
    app = SpideQSBK(root)
    root.geometry("594x382")
    root.configure(background="#d9d9d9")
    root.configure(highlightbackground="#d9d9d9")
    root.configure(highlightcolor="black")
    root.resizable(0,0)
    root.mainloop()