#!/user/bin/env python
#-*- coding:utf-8 -*-

import os
from time import sleep
import time

# 重连动作
def reconnectAction(deviceid):
    devtuple = tuple(getdevlist())
    print(f'设备{deviceid}正在尝试重连.')
    id = 1
    while deviceid not in devtuple:
        print(f'第{id}次 ', end = ' ')
        devtuple = tuple(getdevlist())
        id = id + 1
    print(f'\n设备{deviceid}重新建立连接成功.')
    sleep(1)

# 执行普通的cmd命令
def exeCmd(cmdInfo, deviceid):
    if deviceid == '':
        cmd = 'adb shell ' + cmdInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell ' + cmdInfo[0]
    if os.system(cmd) != 0:
        print(f'设备{deviceid}:exeCmd():{cmdInfo[1]}.')
        return False
    else:
        print(f'设备{deviceid}:exeCmd():{cmdInfo[1]}.')  
        return True

# 按键动作
def pressKeyevent(keycodeInfo, deviceid = ''):
    if deviceid == '':
        cmd = 'adb shell input keyevent ' + keycodeInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell input keyevent ' + keycodeInfo[0]
    if os.system(cmd) != 0:
        print(f'设备{deviceid}:pressKeyevent():{keycodeInfo[1]}.')
        return False
    else:
        print(f'设备{deviceid}:pressKeyevent():{keycodeInfo[1]}.')
        return True
    
# 点击屏幕的动作
def clickScreen(positionInfo, deviceid = ''):
    if deviceid == '':
        cmd = 'adb shell input tap ' + positionInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell input tap ' + positionInfo[0]  
    if os.system(cmd) != 0:
        print(f'设备{deviceid}:clickScreen():{positionInfo[1]}.')
        return False
    else:
        print(f'设备{deviceid}:clickScreen():{positionInfo[1]}.')
        return True

# 输入文本信息
def inputText(tTextInfo, deviceid = ''):
    if deviceid == '':
        cmd = 'adb shell input text ' + tTextInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell input text ' + tTextInfo[0]   
    if os.system(cmd) != 0:
        print(f'设备{deviceid}:inputText():{tTextInfo[1]}.')
        return False
    else:
        print(f'设备{deviceid}:inputText():{tTextInfo[1]}')
        return True
    
# 滑动屏幕的动作
def swipeScreen(positionInfo, deviceid = ''):
    if deviceid == '':
        cmd = 'adb shell input swipe ' + positionInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell input swipe ' + positionInfo[0]  
    if os.system(cmd) != 0:
        print(f'设备{deviceid}:swipeScreen():{positionInfo[1]}.')
        return False
    else:
        print(f'设备{deviceid}:swipeScreen():{positionInfo[1]}')
        return True

# 运行app
def launchApp(appactivityInfo, deviceid = ''):
    if deviceid == '':
        cmd = 'adb shell am start ' + appactivityInfo[0]
    else:
        cmd = 'adb -s ' + deviceid + ' shell am start ' + appactivityInfo[0]   
    if os.system(cmd) != 0:
        print(f'设备{deviceid}:launchApp():{appactivityInfo[1]}.')
        return False
    else:
        print(f'设备{deviceid}:launchApp():{appactivityInfo[1]}')
        return True
        
# 获取username,  如chinaren
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
    
# 执行cmd命令
def executeCMD(cmd):
    stringList = cmd.splitlines() 
    for i in range(len(stringList)):
        try:
            os.system(stringList[i])
        except KeyboardInterrupt:
            print('\n异常退出: KeyboardInterrupt')
            
# 在指定路径新建一个指定前缀_当前系统时间文件夹,并返回foldername(eg:Mtklog_20180411100455)
def creatfolder(path, folderprefix):
    os.chdir(path)
    foldername = folderprefix + '_' + getnowdatatime(3)
    os.mkdir(foldername)
    return foldername
    
# 判断手机/sdcard/下是否存在指定的文件夹名
def isexistfolder(foldername):
    '''
    :type foldername: str
    :rtype: bool
    '''
    try:
        names = os.popen('adb shell ls /sdcard/').readlines()
        # 将file按line变成List中的项后，每个item是以\n结尾的.故foldername后需要+'\n'
        if foldername + '\n' in names:
            return True
        else:
            return False
    except Exception:
        print(f'根目录下存在中文名files/folder,可能会操作异常!\n')

def isAwaked(deviceid = ''):
    '''
    判断的依据是'    mAwake=false\n'
    '''
    if deviceid == '':
        cmd = 'adb shell dumpsys window policy'
    else:
        cmd = 'adb -s ' + deviceid + ' shell dumpsys window policy'
    screenAwakevalue = '    mAwake=true\n' 
    allList = os.popen(cmd).readlines()
    if screenAwakevalue in allList:
        return True
    else:
        return False
        
# 获取时间和日期 
def getnowdatatime(flag = 0):
    '''
    flag = 0为时间和日期         eg:2018-04-11 10:04:55
    flag = 1仅获取日期           eg:2018-04-11
    flag = 2仅获取时间           eg:10:04:55
    flag = 3纯数字的日期和时间   eg:20180411100455 
    
    :type flag: int
    :rtype: str
    '''
    now = time.localtime(time.time())
    if flag == 0:
        return time.strftime('%Y-%m-%d_%H-%M-%S', now)
    if flag == 1:
        return time.strftime('%Y-%m-%d', now)
    if flag == 2:
        return time.strftime('%H:%M:%S', now)
    if flag == 3:
        return time.strftime('%Y%m%d%H%M%S', now)
        
        