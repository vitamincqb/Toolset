#!/user/bin/python
#-*- coding:utf-8 -*-

import os
from multiprocessing import Pool

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

# 返回指定txt文件的第一行内容
def getspecifytxtfilefirstline(txtfilename):
    '''
    返回指定txt文件的第一行内容
    txt档要求与py档在同一目录
    '''
    currunningpyfilepath = os.path.split(os.path.realpath(__file__))[0]
    copyfile2phoneTXT = currunningpyfilepath + '\\' + txtfilename
    while(True):
        if os.path.exists(copyfile2phoneTXT) == True:
            with open(copyfile2phoneTXT, 'r') as f:
                filename = f.readline()
            if filename == '':
                print('txt档为空,输入重新写入待copy文件名.')
                f.close()
                f = open(copyfile2phoneTXT, 'w')
                fileStr = input('请输入你要copy文件的完整文件名\n(建议直接拖入文件至这里，会自动获取写入txt档)：')
                filenamelist = fileStr.split('\\')
                filename = filenamelist[len(filenamelist) - 1]
                f.write(filename)
                f.close()
                print('输入的文件名已写入.')
                return filename
            else:
                return filename
        else:
            print('copyfile2phone.txt文件不存在，将在当前目录新建一个此txt文件！')
            f = open(copyfile2phoneTXT, 'w')
            print('copyfile2phone.txt文件新建成功!')
            fileStr = input('请输入你要copy文件的完整文件名\n(建议直接拖入文件至这里，会自动获取写入txt档)：')
            filenamelist = fileStr.split('\\')
            filename = filenamelist[len(filenamelist) - 1]
            f.write(filename)
            f.close()
            print('输入的文件名已写入.')
            return filename
        
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
        
# Copy文件操作
def copyfile_task(deviceid, filename):
    copyfilepath = 'C:\\Users\\' + getusername() + '\\Desktop\\' + filename
    print(f'设备{deviceid}准备执行copy操作!')
    cmd = 'adb -s ' + deviceid + ' push ' +  copyfilepath + ' /sdcard/'
    # print(cmd)
    if os.system(cmd) == 0:
        print(f'设备{deviceid} 文件copy成功！\n')

def main():
    while(True):
        copyfilename = getspecifytxtfilefirstline('copyfile2phone.txt')
        if checkAdbConnectability() == True:
            copyfilepath = 'C:\\Users\\' + getusername() + '\\Desktop\\' + copyfilename
            if os.path.isfile(copyfilepath) == True:
                print(f'要copy的文件名:{copyfilename}\n')
                print('COPY文件，请稍候... ...\n')
                p = Pool(4)
                devicelist = getdevlist()
                for i in range(len(devicelist)):
                    p.apply_async(copyfile_task, args = (devicelist[i],copyfilename))
                p.close()
                p.join()
                print('所有的copy动作已完成!')
                os.system('pause')
                return
            else:
                print('TXT档中指定的文件名不存在TXT档将被删除并新建，需要重新输入文件名:')
                # 删除文件
                curfilepath = os.path.split(os.path.realpath(__file__))[0]
                TXTfilepath = curfilepath + '\\' + 'copyfile2phone.txt'
                os.remove(TXTfilepath)
                print('TXT档被删除成功')
            
# 主程序
if __name__ == '__main__':
    main()
    
