#!/user/bin/python
#-*- coding:utf-8 -*-

import os
from time import sleep

# 获取username, 如mtk08814
def getusername():
    namelist = os.popen('echo %username%').readlines()
    username = namelist[0].replace("\n", "")
    # 获取当前的username
    return username
    
# 获取设备id列表
def getdevlist():
    devlist = []
    connectfile = os.popen('adb devices')
    list = connectfile.readlines()
    # print(list)
    for i in range(len(list)):
        if list[i].find('\tdevice') != -1:
            temp = list[i].split('\t')
            devlist.append(temp[0])
    return devlist

# 返回指定txt文件的第一行内容
def getspecifytxtfilefirstline(txtfilename):
    '''
    返回指定txt文件的第一行内容
    txt档要求与py档在同一目录
    '''
    currunningpyfilepath = os.path.split(os.path.realpath(__file__))[0]
    copyfile2phoneTXT = currunningpyfilepath + '\\' + txtfilename
    if os.path.exists(copyfile2phoneTXT) == True:
        with open(copyfile2phoneTXT, 'r') as f:
            filename = f.readline()
    if filename == '':
        return 'nofilename'
    else:
        return filename
        
# 测试Adb连接性
def checkAdbConnectability(flag = 0):
    '''
    flag=0 时，当连接正常时返回True(default)
    flag!=0时，直接打印出结果
    '''
    constring = '''ADB连接失败, 请check以下项:
    1. 是否有连接上手机？请连接上手机选择选项6重新check连接性!
    2. 是否有开启"开发者选项"?\n'''
    connectfile = os.popen('adb devices')
    list = connectfile.readlines()
    liststr = ','.join(list).replace('\n', '').strip()
    if len(list) == 2:
        print(constring)
        return False
    # 确保只连接一个设备
    elif liststr.count('device ') > 1:
        print('当前连接了多个设备，请确保只连接一个设备才能正常操作!')
        os.system('adb devices')
        return False
    elif len(list) == 3:
        if flag != 0:
            print('adb连接正常')
            print(list[1])
        else:
            return True
    elif len(list) > 3:
        if liststr.find('daemon') != -1:
            print(constring)
            return False
        else:
            print('当前ADB连接异常:')
            for i in range(1, len(list)-1): # 打印出当前的连接信息.
                if list[i] == '\n':
                    continue
                print(list[i], end = ' ')
            sleep(1)
            # 修复异常
            print('正在修复... ...')
            os.system('TASKKILL /F /IM adb.exe')
            os.system('adb devices')
            # check修复结果
            list = os.popen('adb devices').readlines()
            if len(list) == 2:
                print('修复失败, 请自行check\n')
                return False
            elif len(list) == 3:
                print('修复成功, adb连接正常')
                print(list[1])
                return True