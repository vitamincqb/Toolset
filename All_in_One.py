#!/user/bin/env python
#-*- coding:utf-8 -*-

import os
from time import sleep
import time
from tkinter import *

# 当前py文件的路径
currunningpyfilepath = os.path.split(os.path.realpath(__file__))[0]

# 菜单定义
menus = '''===================Based on Python3.6.5=====================
0. Exit                                                    
1. 截图并copy至桌面                                        
2. Copy文件(MTKlog/DCIM/Copyfile)至桌面                 
3. 打开MTKlog                                              
4. Copy文件至手机                                          
5. 手机录屏并copy至桌面                                    
6. Check ADB连接性                                         
7. 安装APK                                                 
8. 导出APK to desk(前台正在使用的apk)                      
9. 抓Logcat                                                
a. 获取PC IP address                                       
b. 生成指定大小的TXT档                                     
c. 计时器(Stopwatch)                                       
                                                           
Others:cmd/exit/cls/read/write/help2/help3/help4/help8                             
------------------------------------------------------------
'''
        
cmdLogcat = '''echo 请按 CTRL+C 来停止log的录制! logcat.txt档将保存在桌面.
adb shell logcat >C:\\Users\\%username%\\Desktop\\logcat.txt
'''
cmdCallMtklogApp = '''echo Mtklog主界面将开启
echo=
adb shell am start com.mediatek.mtklogger/.MainActivity
'''
# start表示开启，stop表示关闭；7代表这三种，也可改为1/2/4，分别代表MobileLog/ModemLog/NetworkLog
cmdTurnOnMtklog = '''echo Mtklog将开启并录制
echo=
adb shell am start com.mediatek.mtklogger/.MainActivity
adb shell am broadcast -a com.mediatek.mtklogger.ADB_CMD -e cmd_name start --ei cmd_target 1
'''
# start表示开启，stop表示关闭；7代表这三种，也可改为1/2/4，分别代表MobileLog/ModemLog/NetworkLog
cmdTurnOffMtklog = '''echo Mtklog将关闭
echo=
adb shell am start com.mediatek.mtklogger/.MainActivity
adb shell am broadcast -a com.mediatek.mtklogger.ADB_CMD -e cmd_name stop --ei cmd_target 1
'''
cmdIpconfig = '''ipconfig
'''
cmdswitchConsolePy = '''echo 欢迎进入Console环境(cmd), 输入exit将再次返回python环境
echo=
C:\Windows\System32\cmd.exe
'''
    
# 装饰器,用于在执行函数前时清屏和执行完函数时打印出menus
def deco_cls_menus(*dargs, **dkw):
    '''
    dargs[0] = 0时, 不需要chek adb连接性
    dargs[0] = 1时, 需要chek adb连接性
    dargs[0] = 2时, 不需要cls和打印menus
    '''
    from functools import wraps
    def _deco_cls_menus(func):
        @wraps(func)
        def wrapper(*args, **kw):
            # dargs[0] = 1时, 需要chek adb连接性
            if dargs[0] == 1:
                os.system('cls')
                if checkAdbConnectability() == True:
                    print(f'正在执行所选操作, 请稍候... ...\n')
                    output = func(*args, **kw)
                    print(f'{menus}')
                    return output
                else:
                    print(f'\n\n{menus}')
            # dargs[0] = 0时, 不需要chek adb连接性
            if dargs[0] == 0:
                os.system('cls')
                print(f'正在执行所选操作, 请稍候... ...\n')
                output = func(*args, **kw)
                print(f'{menus}')
                return output
            if dargs[0] == 2:
                if checkAdbConnectability() == True:
                    print(f'正在执行所选操作, 请稍候... ...\n')
                    output = func(*args, **kw)
                    return output
        return wrapper
    return _deco_cls_menus
    
# 获取各个功能项的使用说明档
@deco_cls_menus(0)
def helpfile(cmd):
    if cmd == 'help2':
        print(copyMtklogOrPicToDesk.__doc__)
    if cmd == 'help3':
        print(turnOnOffMtklog.__doc__)
    if cmd == 'help4':
        print(copyfile2Phone.__doc__)
    if cmd == 'help8':
        print(exportapk.__doc__)
        
# 判断手机/sdcard/下是否存在指定的文件夹名
def isexistfolder(foldername):
    try:
        names = os.popen('adb shell ls /sdcard/').readlines()
        # 将file按line变成List中的项后，每个item是以\n结尾的.故foldername后需要+'\n'
        if foldername + '\n' in names:
            return True
        else:
            return False
    except Exception:
        print(f'根目录下存在中文名file/folder name, 可能会操作异常!\n')

# 记录CODE修改日志, 输入'readme'可进入日志记录界面
@deco_cls_menus(0)
def writeReadmefile():
    # 判断是否存在记录文件
    abspathOfRecfile = currunningpyfilepath + '\modifyRecord.txt'
    if os.path.exists(abspathOfRecfile) == True:
        print(f'修改日志保存在以下位置：\n{abspathOfRecfile}')
        with open(currunningpyfilepath + '\modifyRecord.txt', 'a') as f:
            endflag = 'end'
            modifyRec = []
            # 输入待记录的内容
            print('请输入Modidy Note:\n')
            for line in iter(input, endflag):
                modifyRec.append(line)
            # 写入输入的内容
            f.write('\n\n' + getnowdatatime(0) + '\n')
            for line in modifyRec:
                f.write(line + '\n')
            # 关闭文件
            f.close()
            print('记录已保存！')
    else:
        print(currunningpyfilepath,'\n以上目录文档不存在, 无法写入!请向Owner索要文档!')

# 读取修改记录
@deco_cls_menus(0)
def readModifyrecord():
    abspathOfRecfile = currunningpyfilepath + '\modifyRecord.txt'
    if os.path.exists(abspathOfRecfile) == True:
        lineId = 1
        with open(abspathOfRecfile, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                print(lineId, '      ', line)
                lineId += 1
    else:
        print(currunningpyfilepath,'\n以上目录文档不存在, 无法读取!请向Owner索要文档!')
    
# 读取菜单Item
def readMenuItem(num):
    menuitem = menus.splitlines()[num + 1]
    print(f'正在执行 {menuitem}\n')

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
        
# 获取设备SN列表
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
    
# 测试Adb连接性
def checkAdbConnectability(flag = 0):
    '''
    flag =0时，当连接正常时返回True(default)
    flag!=0时，直接打印出结果
    '''
    connectstring = '''ADB连接失败, 请check以下项:
    1. 是否有连接上手机？请连接上手机选并重新check连接性!
    2. 是否有开启"开发者选项\\USB调试模式"?\n'''
    connectinfolist = getdevlist()
    
    if len(connectinfolist) == 0:
        print(connectstring)
        return False
    if len(connectinfolist) == 1:
        if flag != 0:
            print('连接正常')
            print(f'设备SN: {connectinfolist[0]}')
        else:
            return True
    if len(connectinfolist) >= 2:
        print('连接正常，但当前有连接多台设备，请确保只连接一台才能正常操作. ')
        for i in range(len(connectinfolist)):
            print(f'设备{i + 1} SN: {connectinfolist[i]}')
        return False
            
# 安装应用
@deco_cls_menus(1)
def installapk():
    try:
        while(True):
            path = input('请将待安装apk或apk folder拖入Console中:')
            if os.path.exists(path) == False:
                print('路径不存在或路径中不要出现中文，请确认?!')
                break
            else:
                # 如果拖入的是一个apk文件
                if os.path.isfile(path) == True:
                    cmdinstall = 'adb install ' + path
                    print('apk正在安装... ...')
                    if os.system(cmdinstall) == 0:
                        print('apk已安装成功!')
                    else:
                        print('apk安装Fail, 请check是否已安装过.')
                # 如果拖入的是一个文件夹
                else:
                    okCount, failCount = (0, 0)
                    apklist = os.listdir(path)
                    print(f'待安装的apk有{len(apklist)}个')
                    for i in range(len(apklist)):
                        print(f'当前正在安装第{i+1}个apk:\n{apklist[i]}')
                        cmdinstall = 'adb install ' + path + '\\' + apklist[i]
                        if os.system(cmdinstall) == 0:
                            print(f'第{i+1}个apk已安装成功!')
                            okCount = okCount + 1
                        else:
                            failCount = failCount + 1
                            print('此apk安装fail, 请check是否已安装过.')
                    print(f'所有应用共{len(apklist)}个, 已成功安装: {okCount}个，fail: {failCount}个.')
                break
    except KeyboardInterrupt:
        print('\n手动中止操作:KeyboardInterrupt')
    except EOFError:
        print('\n未知异常: EOFError')

# 导出手机当前前台正在使用的apk
@deco_cls_menus(1)
def exportapk(cmd = '8'):
    '''
    导出APK to desk(前台正在使用的apk)　用法:
    -----------------------------------------
    cmd='8' , 将导出当前前台正在使用的apk至桌面
    cmd='8,', 仅输出当前信息的包信息
    '''
    # 获取包info
    packagefileline = os.popen('adb shell dumpsys window | findstr mCurrentFocus').readlines()
    # 打印包info, 在PPTS做设置时会用到apk的包信息
    packageinfo = packagefileline[len(packagefileline) -1].strip()
    beg = packageinfo.find('u0')
    print('PackageInfo: ', packageinfo[beg+3:len(packageinfo)-1])
    # 打印出包info
    # 如手机为锁屏状态，无法获取则退出, 并提示当前为锁屏状态
    # mtk/xiaomi/samsung=Keyguard
    # huawei=StatusBar
    if packageinfo.find('Keyguard') != -1 or \
    packageinfo.find('StatusBar') != -1:
        print('手机处于锁屏状态, 无法获取应用info.请退出锁屏状态再导出apk!!!')
        return
    else:
        # 获取package名称
        packagelist = packageinfo.split('/')
        # print(packagelist)
        startpos = packagelist[0].find('u0') + 3
        packagename = packagelist[0][startpos:]
        print('PackageName: ', packagename)
        if cmd == '8':
            # 获取package安装路径
            pathinfo = os.popen('adb shell pm path ' + packagename).readlines()[0].strip()
            sourcepath = pathinfo[8:]
            print('当前应用的安装路径: ', sourcepath)
            # 导出apk
            destinationpath = 'C:\\Users\\' + getusername() + '\\Desktop\\' + packagename + '.apk'
            os.system('adb pull ' + sourcepath + ' ' + destinationpath)
            print('Apk已导出至桌面.')
        else:
            return
    
# 复制文件、文件夹至手机中的00Copyfile文件夹
@deco_cls_menus(1)
def copyfile2Phone(cmd = '4'):
    '''
    Copy文件至手机　用法:
    -----------------------------------------
    cmd='4' , 复制手机中的00Copyfile文件夹至桌面
    cmd='4,', 在手机根目录新建00Copyfile
    '''
    try:
        if cmd == '4':
            while(True):
                soursefilepath = input('请将要copy的文件或文件夹拖入Console中:')
                if os.path.exists(soursefilepath) == False:
                    print('路径不存在，请确认?!')
                    break
                else:
                    destinationpath = ' /sdcard/00Copyfile'
                    if isexistfolder('00Copyfile') == True: 
                        print('根目录下已存在00Copyfile folder，文件将直接copy至00Copyfile内!')
                        print('Copy操作准备中(按CTRC+C可中止copy!)，请稍候.... ...')
                        if os.system('adb push ' + soursefilepath + ' ' + destinationpath) == 0:
                            print('文件已copy至根目录下的Copyfile folder中!')
                    else:
                        print('在手机根目录新建folder:00Copyfile成功，copy的文件将保存在此folder中!')
                        print('Copy操作准备中(按CTRC+C可中止copy!)，请稍候.... ...')
                        os.system('adb shell mkdir sdcard/00Copyfile')
                        if os.system('adb push ' + soursefilepath + destinationpath) == 0:
                            print('文件已copy至根目录下的Copyfile folder中!')
                    break
        if cmd == '4,':
            os.system('adb shell mkdir sdcard/00Copyfile')
            print('新建文件夹00Copyfile成功!')
    except KeyboardInterrupt:
        print('\n手动中止操作:KeyboardInterrupt')
    except EOFError:
        print('\n未知异常:EOFError')

# 从手机里copy mtklog至桌面
@deco_cls_menus(1)
def copyMtklogOrPicToDesk(cmdflag = '2'):
    '''
    Copy文件(MTKlog/DCIM/00Copyfile)至桌面 用法：
    -------------------------------------------
    1:仅删除mtklog文件夹
    可输入:'d m', 'd,m', 'd mtklog', 'd,mtklog', 'del mtklog', 'del,mtklog', 'del m', 'del,m'
    2:仅删除DCIM文件夹
    可输入:'d d','d,d',  'del d', 'del,d', 'del dcim','d dcim', 'del,dcim', 'd,dcim'
    3:仅删除00Copyfile文件夹
    可输入:'d cf', 'd c','d,cf', 'd,c', 'del cf', 'del c',  'del,cf', 'del,c'
    4:复制Mtklog至桌面then删除手机中的Mtklog文件夹
    可输入：'2', '2,', '2m', 'mtklog', '2mtklog', 
    5:复制Mtklog/DCIM文件夹then删除手机中的Mtklog/DCIM文件夹 
    可输入:'2mp','mp','2md', 'md'
    6:复制DCIM文件夹至桌面then删除DCIM文件夹
    可输入：'2d', '2dcim', 'dcim'
    7:复制00Copyfile至桌面then询问是否删除00Copyfile文件夹
    可输入：'2c', '2cf', 'cf', 'Copyfile'
    '''
    try:
        path = 'C:\\Users\\' + getusername() + '\\Desktop'
        cmdMtklogPre = 'adb pull /sdcard/mtklog C:\\Users\\%username%\\Desktop\\'
        cmdPicPre = 'adb pull /sdcard/DCIM C:\\Users\\%username%\\Desktop\\'
        cmd00CopyfilePre = 'adb pull /sdcard/00Copyfile C:\\Users\\%username%\\Desktop\\'
        cmdDELMtklog = 'adb shell rm -r /sdcard/mtklog'
        cmdDELPic = 'adb shell rm -r /sdcard/DCIM'
        cmdDEL00Copyfile = 'adb shell rm -r /sdcard/00Copyfile'
                 
        # 可以根据输入分别删除mtklog/DCIM/00Copyfile        
        def delfolder():
            try:
                if cmdflag in ('del mtklog', 'del m', 'd m', 'd mtklog', 'del,mtklog', 'del,m', 'd,m', 'd,mtklog'):
                    if os.system(cmdDELMtklog) == 0:
                        print('mtk文件夹删除成功!')
                if cmdflag in ('del dcim', 'del d', 'd d', 'd dcim', 'del,dcim', 'del,d','d,d', 'd,dcim'):
                    if os.system(cmdDELPic) == 0:
                        print('DCIM文件夹删除成功!')
                if cmdflag in ('del cf', 'del c', 'd cf', 'd c', 'del,cf', 'del,c', 'd,cf', 'd,c'):
                    if os.system(cmdDEL00Copyfile) == 0:
                        print('00Copyfile文件夹删除成功!')
            except Exception:
                print('文件夹不存在,无法删除')
                
        # 仅copy 00Copyfile folder至桌面
        def copyCopyfileOnly():
            if isexistfolder('00Copyfile') == True:
                # foldername = creatfolder(path, '00Copyfile')
                # cmd00Copyfile = cmd00CopyfilePre + foldername
                # 如果copy成功，将询问是否删除手机内00Copyfile文件夹
                if os.system(cmd00CopyfilePre) == 0:
                    print('00Copyfile copy完成!')
                    while(True):
                        askme = input('是否删除手机中的00Copyfile folder?(y or n?)')
                        if askme in ('yes', 'YES', 'Yes', 'Y', 'y'):
                            os.system(cmdDEL00Copyfile)
                            print('手机中的00Copyfile已del完成!')
                            return
                        elif askme in ('no', 'NO', 'No', 'N', 'n'):
                            print('手机中的00Copyfile将保留!')
                            return
                        else:
                            print('输入有误, 请重新输入！')
                            return
                else:
                    print('00Copyfile文件夹copy失败!')
            else:
                print('00Copyfile文件夹不存在,无法copy!')
                    
        # 仅copy Mtklog至桌面
        def copyMtklogOnly(confilename = '', flag = 0):
            '''
            flag =0, 会在桌面创建文件夹
            flag!=0, 不在桌面创建文件夹
            '''
            if isexistfolder('mtklog') == True:
                if flag == 0:
                    foldername = creatfolder(path, 'Mtklog')
                    cmdMtklog = cmdMtklogPre + foldername
                else:
                    cmdMtklog = cmdMtklogPre + confilename
                # 如果copy成功，将删除手机内mtklog文件夹
                if os.system(cmdMtklog) == 0:
                    print('mtklog copy完成!')
                    if confilename != '2,':
                        os.system(cmdDELMtklog)
                        print('手机中的mtklog已del完成!')
                    else:
                        print('手机中的mtklog将保留!')
                else:
                    print('Mtklog文件夹copy失败!')
            else:
                print('mtklog文件夹不存在,无法copy!')
            
        # 仅copy DCIM文件夹至桌面
        def copyPicOnly(confilename = '', flag = 0):
            '''flag=0, 会在桌面创建文件夹/flag!=0, 不在桌面创建文件夹'''
            if isexistfolder('DCIM') == True:
                if flag == 0:
                    foldername = creatfolder(path, 'DCIM')
                    cmdPic = cmdPicPre + foldername
                    print(cmdPic)
                else:
                    cmdPic = cmdPicPre + confilename
                if os.system(cmdPic) == 0:
                    print('DCIM已copy完成!')
                    os.system(cmdDELPic)
                    print('手机中的DCIM已del完成!')
                else:
                    print('DCIM文件夹copy失败!')
            else:
                print('DCIM文件夹不存在,无法copy!')
                
        # copy Mtklog及DCIC文件至桌面
        def copyMtklogDcimOrOthers():
            if isexistfolder('mtklog') == True and isexistfolder('DCIM') == True:
                newfoldername = creatfolder(path, 'MtklogPic')
                copyMtklogOnly(newfoldername, 1)
                copyPicOnly(newfoldername, 1)
            elif isexistfolder('mtklog') == True:
                print('Mtklog folder:有\nDCIM folder:无')
                copyMtklogOnly()
            elif isexistfolder('DCIM') == True:
                print('Mtklog folder:无\nDCIM folder:有')
                copyPicOnly()
            else:
                print('Mtklog/DCIM文件夹均不存在,无法copy!')
        
        # 对不同要求的处理. 
        if cmdflag in ('2', '2m', 'mtklog', '2mtklog', '2,'):
            copyMtklogOnly()
        elif cmdflag in ('2md','md', 'mp', '2mp'):
            copyMtklogDcimOrOthers()
        elif cmdflag in ('2d', '2dcim', 'dcim'):
            copyPicOnly()
        elif cmdflag in ('2c', '2cf', 'cf', 'Copyfile', 'Copyfile'):
            copyCopyfileOnly()
        else:
            delfolder()
            
    # 用于处理:当根目录下有中文文件夹且无mtklog folder时,可能会由于编码问题而出导致程序报错退出.
    except Exception:
        print('操作异常, 请check目录中是否存在mtklog&DCIM folder!')

# 截图并copy至桌面            
@deco_cls_menus(1)
def screenshot():
    filename = getnowdatatime(3) + '.png'
    if os.system('adb shell /system/bin/screencap -p /sdcard/' + filename ) == 0:
        if os.system('adb pull /sdcard/' + filename + ' C:\\Users\\%username%\\Desktop\\' + filename) == 0:
            if os.system('adb shell rm /sdcard/' + filename) == 0:
                print('截图成功并保存至桌面!')

# 执行cmd命令
@deco_cls_menus(2)
def executeCMD(cmd):
    stringList = cmd.splitlines() 
    for i in range(len(stringList)):
        try:
            os.system(stringList[i])
        except KeyboardInterrupt:
            print('\n异常退出: KeyboardInterrupt')

# 开、关、调用mtklog
@deco_cls_menus(1)
def turnOnOffMtklog(cmd = '3'):
    '''
    打开MTKlog 用法：
    ----------------
    cmd = '3', 打开mtklog主界面
    cmd = ('3 0', '3,0'), 关闭mtklog
    cmd = ('3 1', '3,1'), 开启mtklog
    '''
    if cmd == '3':
        executeCMD(cmdCallMtklogApp)
    elif cmd in ('3 0', '3,0'):
        # 当前默认只开启mobile log，因为这个最常用
        executeCMD(cmdTurnOffMtklog)
    else: 
        # ('3 1', '3, 1')
        executeCMD(cmdTurnOnMtklog)
        
# 生成指定大小的TXT档
@deco_cls_menus(0)
def generateTXTFile(cmd = 'b'):
    fileSize = 0
    # 判断输入是否有误
    while True:
        size = input('请输入你想生成的TXT文件大小(MB):')
        if size.strip().isdigit() != True:
            print('只能输入整数，请重新输入!')
            continue
        else:
            fileSize = int(size)
            break            
    if fileSize >= 200:
       print('正在生成TXT文件，请稍候... ...')
    # 生成指定大小的TXT档
    filename = getnowdatatime(3) + '_' + size + 'MB.txt'
    print(f'文件名：{filename}')
    # 设置文件保存的路径
    filepath = 'C:\\Users\\' + getusername() + '\\Desktop\\'
    f = open(filepath + filename, 'w')
    # 获取开始时间
    starttime = getnowdatatime() 
    startclock = time.clock()
    for i in range(fileSize):
        if i >= 100:
            if i%100 == 0:
                print(f'已生成{i//100 * 100}MB数据.')
        for j in range(1024):
            try:
                f.write('01'*512)
            except KeyboardInterrupt:
                print('\n异常中断:KeyboardInterrupt')
                f.close()
                exit(-1)
    f.close()
    print(f'文件已成生并保存在桌面,  文件大小:{fileSize}MB.\n')
    print(f'DetailInfo:')
    print(f'保存路径: {filepath + filename}')
    print(f'开始时间:{starttime}')
    print(f'结束时间:{getnowdatatime()}')
    print(f'总共耗时:{(time.clock() - startclock):<.3}sec.')

# 安卓手机录屏,文件保存后将copy至桌面
@deco_cls_menus(1)
def recordScreen():
    filename = getnowdatatime(3) + '.mp4'
    print('video正在录制中(请按CTRL + C结束video录制)')
    try:
        os.system('adb shell screenrecord sdcard/' + filename )
    except KeyboardInterrupt:
        print('\n手动中止录制')
        print('正在将video copy至桌面,请稍候... ...')
        if os.system('adb pull /sdcard/' + filename + ' C:\\Users\\%username%\\Desktop\\' + filename) == 0:
            print('video copy至桌面完成!')
        print('正在删除手机中的video记录... ...')
        if os.system('adb shell "rm /sdcard/' + filename) == 0:
            print('手机中的video已删除.')
    finally:
        if isexistfolder(filename) == True:
            print('\n手动中止录制, call finally!')
            print('正在将video copy至桌面,请稍候... ...')
            if os.system('adb pull /sdcard/' + filename + ' C:\\Users\\%username%\\Desktop\\' + filename) == 0:
                print('video copy至桌面完成!')
            print('正在删除手机中的video记录... ...')
            if os.system('adb shell "rm /sdcard/' + filename) == 0:
                print('手机中的video已删除.')            
    
# 获取电脑的IP地址
@deco_cls_menus(0)
def getIpconfigKeyData(cmd):
    resultapklist = os.popen(cmd).readlines()
    startIndex = 0
    for index in range(len(resultapklist)):
        if resultapklist[index].strip().find('本地链接') != -1:
            startIndex = index
            break
    for line in range(startIndex, startIndex + 4):
        print(resultapklist[line], end = ' ')
        
    print('\n电脑的', resultapklist[startIndex + 1].lstrip())
    
# 获取username, 如mtk08814
def getusername():
    namelist = os.popen('echo %username%').readlines()
    username = namelist[0].replace("\n", "")
    # 获取当前的username
    return username

# 在指定路径新建一个指定前缀_当前系统时间文件夹,并返回foldername(eg:Mtklog_20180411100455)
def creatfolder(path, folderprefix):
    os.chdir(path)
    foldername = folderprefix + '_' + getnowdatatime(3)
    os.mkdir(foldername)
    return foldername
    
# 计时器类
class StopWatch(Frame):
    msec = 50
    # 初始化
    def __init__(self,parent = None,**kw):
        Frame.__init__(self,parent,kw)
        self.__start = 0.0
        self.__elapsedtime = 0.0
        self.__running = False
        self.timestr = StringVar()
        self.makeWidgets()
        # print('__init__')
        
    # 新增时间Label
    def makeWidgets(self):
        lable = Label(self,textvariable = self.timestr, font = ("宋体, 120"))
        self.setTime(self.__elapsedtime)
        lable.pack(fill = Y, expand = NO, pady = 2, padx = 2, anchor = CENTER)
        # print('makeWidgets')
        
    # 用逝去的时间更新标签
    def update(self):
        self.__elapsedtime = time.time() - self.__start
        self.setTime(self.__elapsedtime)
        self.__timer = self.after(self.msec,self.update)
        # print('update')
        
    # 将时间格式改为分:秒:千分秒(00:00:000)
    def setTime(self,elap):
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0-seconds)*1000)
        # self.timestr.set('{:0>2d}:{:0>2d}:{:0>3d}'.format(minutes,seconds,hseconds))
        self.timestr.set(f'{minutes:0>2d}:{seconds:0>2d}:{hseconds:0>3d}')
        # print('setTime')
        
    # 启动计时器，如果已启动则忽略
    def start(self):
        if not self.__running:
           self.__start = time.time() - self.__elapsedtime
           self.update() 
           self.__running = True
           print('计时器开始计时.')
           # print('start')
           
    # 停止计时器，若已停止则忽略
    def stop(self):
        if self.__running:
            self.after_cancel(self.__timer)
            self.__elapsedtime = time.time() - self.__start
            self.setTime(self.__elapsedtime)
            self.__running = False
            print('计时器停止计时.')
            # print('stop')
    
    # 重设计时器
    def reset(self):
        self.__start = time.time()
        self.__elapsedtime = 0.0
        self.setTime(self.__elapsedtime)
        print('计时器恢复默认状态.')
        # print('reset')
        
# 计时器
@deco_cls_menus(0)
def stopwatchApp():
    print('计时器将以弹窗形式呈现，请关闭计时器窗口来退出计时器回到主菜单. ')
    root = Tk()
    root.title('Stopwatch for UX test')
    app = StopWatch(root)
    app.pack(side = TOP)
    Button(root, text = '开始计时', command = app.start).pack(side = LEFT, anchor = S, fill= X, expand = YES)
    Button(root, text = '停止计时', command = app.stop).pack(side = LEFT, anchor = S, fill= X, expand = YES)
    Button(root, text = '重置计时', command = app.reset).pack(side = LEFT, anchor = S, fill= X, expand = YES)
    
    ''' 
    窗口位置和修改窗口大小，要用到是tk对象提供的geometry方法。https://jingyan.baidu.com/article/ad310e801dd5261848f49e6b.html
    该方法的用法是geometry(字符串)，这个字符串格式为：
    "窗口宽x窗口高+窗口位于屏幕x轴+窗口位于屏幕y轴"
    得到屏幕宽度/高度 
    '''
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    # 窗口宽高
    ww = 750
    wh = 200
    x = (sw - ww)/2
    y = (sh - 2*wh)/2
    # root.geometry("{}x{}+{:.0f}+{:.0f}".format(ww,wh,x,y))
    root.geometry(f"{ww}x{wh}+{x:.0f}+{y:.0f}")
    # 为使用的方便,启动时就自动计时
    app.start()
    root.mainloop()

# 主函数
def main():
    # check adb的连接性
    checkAdbConnectability() 
    print(menus)
    inputErrorNum = 0
    selItem2Tuple = (
                'del mtklog', 'del m', 'd m', 'd mtklog', 'del,mtklog', 'del,m', 'd,m', 'd,mtklog', \
                'del dcim', 'del d', 'd d', 'd dcim', 'del,dcim', 'del,d','d,d', 'd,dcim', \
                'del cf', 'del c', 'd cf', 'd c', 'del,cf', 'del,c', 'd,cf', 'd,c', \
                '2', '2m', 'mtklog', '2mtklog', '2,', \
                '2mp','mp','2md', 'md', \
                '2d', '2dcim', 'dcim', \
                '2c', '2cf', 'Copyfile', 'Copyfile', 'cf')
    while True:
        try:
            num = input('请输入需要执行项的序号:')
            selString = num.strip().lower()
            if selString in ('0', 'exit'):
                break
            elif selString == '1':
                screenshot()
            elif selString in selItem2Tuple:
                copyMtklogOrPicToDesk(selString)
            elif selString in ('3', '3 0', '3 1', '3,0', '3,1'):
                turnOnOffMtklog(selString)
            elif selString in ('4', '4,'):
                copyfile2Phone(selString)
            elif selString == '5':
                recordScreen()
            elif selString == '6':
                checkAdbConnectability(1)
            elif selString == '7':
                installapk()
            elif selString in ('8', '8,'):
                exportapk(selString)
            elif selString == '9':
                os.system('cls')
                executeCMD(cmdLogcat)
                print(f'{menus}')
            elif selString == 'a':
                getIpconfigKeyData(cmdIpconfig)
            elif selString in ('b', 'b,', 'b,sd'):
                generateTXTFile()
            elif selString == 'c':
                stopwatchApp()
            # 输入'cmd'会进入console环境
            elif selString == 'cmd':
                os.system('cls')
                executeCMD(cmdswitchConsolePy)
                print(f'{menus}')
            # 输入'cls'会清屏
            elif selString == 'cls':
                os.system('cls')
                print(f'{menus}')
            elif selString == 'write':
                writeReadmefile()
            elif selString == 'read':
                readModifyrecord()
            elif selString in ('help2', 'help3', 'help4', 'help8'):
                helpfile(selString)
            else:
                # 如果连续输入序号错误7次会清屏一次，避免看不到菜单
                inputErrorNum = inputErrorNum + 1
                print('当前输入有误!')
                if inputErrorNum >= 7: 
                    inputErrorNum = 0
                    os.system('cls')
                    print(f'{menus}')
                continue
        except (KeyboardInterrupt, EOFError):
            print('@_@　捕捉到了异常. 请重新输入或重新启动tool!')
            print(f'\n\n{menus}')
                
#--------------------主程序--------------------
if __name__ == '__main__':
    main()
