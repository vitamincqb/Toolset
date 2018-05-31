#!/user/bin/python
#-*- coding:utf-8 -*-

import os
from time import sleep
from commonlib import *
from multiprocessing import Pool
    
# Copy文件操作
def copyfile_task(deviceid, filename):
    copyfilepath = 'C:\\Users\\' + getusername() + '\\Desktop\\' + filename
    print(f'设备{deviceid}准备执行copy操作!')
    cmd = 'adb -s ' + deviceid + ' push ' +  copyfilepath + ' /sdcard/'
    # print(cmd)
    if os.system(cmd) == 0:
        print(f'设备{deviceid} 文件copy成功！\n')

def main():
    copyfilename = getspecifytxtfilefirstline('copyfile2phone.txt')
    if checkAdbConnectability(0) == True:
        if copyfilename != 'nofilename':
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
            else:
                print(f'桌面不存在文件{copyfilename}，请先将文件copy至桌面.')
        else:
            print('没有指定待copy的文件!')            
# 主程序
if __name__ == '__main__':
    main()
    