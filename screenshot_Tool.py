from PIL import Image
import os
import subprocess
import time
import shutil
import random


# 得到PC桌面路径
def getDesktopPath() -> str:
    return 'C:\\Users\\' + os.getlogin() + '\\Desktop\\'


class Screenshot(object):
    def __init__(self, cmd='1'):
        # 用于存储各个截图的位置
        self.imgPathList = list()
        # 用于存储Image.open()打开截图后的数据
        self.imgInfoList = list()
        # 用于存储每张截图在longimg上的paste坐标tuple(x, y)
        self.imgpasteLoctionList = list()
        # 用于存储每张截图待crop的box(x, y, w, h)
        self.imgcropboxList = list()

        # 要执行的截图类型
        self.cmd = cmd
        # 图片保存位置的flag
        self.save2destFlag = True
        # 自动滑动界面的距离
        self.swipe_distance = 0
        # 最终要拼接的长图的长充
        self.longimage_length = 0
        # 　截图的数量
        self.imgnum = 0

        # 头部相同区域的坐标info tuple(left,upper,right,lower)
        self.headoverlapBox = ()
        # 尾部相同区域的坐标info tuple(left,upper,right,lower)
        self.tailoverlapBox = ()

        # 尾部是否有重叠部分(注：头部一般是有重叠部分的)
        self.iscropTailoverlap = True

        # 在C根目录下新建test_screenshot目录
        if os.path.exists('c:\\test_screenshot') == False:
            os.mkdir('c:\\test_screenshot')

    # 执行截图动作
    def screenshot(self):
        imgname = str(time.time()).split('.')[0] + '.jpg'
        # 截图的cmd
        cmd = 'adb shell /system/bin/screencap -p /sdcard/' + imgname
        if subprocess.run(cmd, shell=True).returncode == 0:
            # 将截图文件copy至桌面的cmd
            if self.save2destFlag:
                cmd = 'adb pull /sdcard/' + imgname + ' ' + getDesktopPath() + imgname
            else:
                cmd = 'adb pull /sdcard/' + imgname + ' c:\\test_screenshot\\' + imgname
            if subprocess.run(cmd, shell=True).returncode == 0:
                self.imgPathList.append(imgname)
                if subprocess.run('adb shell rm /sdcard/' + imgname, shell=True).returncode == 0:
                    self.imgnum += 1
                    print('本次截图成功！')

    # 从self.imgList中取出图片并将各个图片的像素info存在imgInfoList中
    def openImg(self):
        for img in self.imgPathList:
            imgInfo = Image.open(img)
            self.imgInfoList.append(imgInfo)

    # 查找图1、图2头部的相同区域
    def findHeadOverlap(self, ratio=0.95):
        imginfo1, imginfo2 = self.imgInfoList[0], self.imgInfoList[1]
        img_width, img_height = imginfo1.size
        # print(img_width, img_height)
        find_h = 0
        # print(img_width, img_height)

        def findsame_h(imginfo1, imginfo2):
            for h in range(img_height):  # 比较每一行
                totalForSame = 0
                totalForSame1 = 0
                for w in range(img_width):  # 比较两张图片的每一个像素点info是否相同
                    a, b, c = imginfo1.getpixel((w, h+1))
                    x, y, z = imginfo2.getpixel((w, h+1))
                    a1, b1, c1 = imginfo1.getpixel((w, h + 5))
                    x1, y1, z1 = imginfo2.getpixel((w, h + 5))
                    if abs(a - x) < 20 and abs(b - y) < 20 and abs(c - z) < 20:
                        totalForSame += 1
                    if abs(a1 - x1) < 20 and abs(b1 - y1) < 20 and abs(c1 - z1) < 20:
                        totalForSame1 += 1
                # 每一行比较完成后，如果相同率小于0.85, 则会找到了相同的区域
                if totalForSame / img_width < ratio and totalForSame1 / img_width < ratio:
                    self.headoverlapBox = (0, 0, img_width, h)
                    # print(f'找到啦：{self.headoverlapBox}')
                    # xImg = self.imgInfoList[0].crop(self.headoverlapBox)
                    # xImg.save(getDesktopPath() + 'head.jpg')
                    # break
                    return h
            return 0

        h1 = findsame_h(imginfo1, imginfo2)
        tempbox = (0, 0, img_width, h1)
        # xImg = self.imgInfoList[1].crop(tempbox)
        # xImg.save(getDesktopPath() + 'temp.jpg')
        # 再查找一次,为何要再查找一次呢？
        # 因为在很多浏览器界面，打开一个网页时有一个网址栏，而这时的头部应该是手机状态栏+网址栏下面的菜单栏
        box = (0, 0, img_width, img_height - h1)
        imginfo1, imginfo2 = imginfo1.crop(box), imginfo2.crop(box)
        img_width, img_height = imginfo1.size
        # print(img_width, img_height)
        h2 = findsame_h(imginfo1, imginfo2)
        if h2 == 0:
            find_h = h1
        else:
            find_h = h1 + h1

        self.headoverlapBox = (0, 0, img_width, find_h)
        # print(f'找到啦：{self.headoverlapBox}')
        # xImg = self.imgInfoList[1].crop(self.headoverlapBox)
        # xImg.save(getDesktopPath() + 'head.jpg')

    # 查找图1、图2尾部的相同区域
    def findTailOverlap(self, ratio=1):
        imginfo1, imginfo2 = self.imgInfoList[0], self.imgInfoList[1]
        img_width, img_height = self.imgInfoList[0].size
        # print(img_width, img_height)
        # 从图像下面开始向上进行比较
        for h in range(img_height - 1, -1, -1):
            totalForSame = 0
            for w in range(img_width):  # 比较两张图片的每一个像素点info是否相同
                a, b, c = imginfo1.getpixel((w, h))
                x, y, z = imginfo2.getpixel((w, h))
                if abs(a - x) < 20 and abs(b - y) < 20 and abs(c - z) < 20:
                    totalForSame += 1
            # 每一行比较完成后，如果相同率小于0.95, 则会找到了相同的区域
            if totalForSame / img_width < ratio:
                # if h == img_height - 1:
                #     break
                self.tailoverlapBox = (0, h, img_width, img_height)
                # print(f'找到啦：{self.tailoverlapBox}')
                # xImg = self.imgInfoList[0].crop(self.tailoverlapBox)
                # xImg.save(getDesktopPath() + 'tail.jpg')
                break

    # 查打img2在img1看的重叠行
    def findoverlap(self, img1, img2, isFirst: bool, isEnd: bool):
        if self.iscropTailoverlap is False:
            pass  # 通过处理，可以不写.
            # return newimgfile
        if self.iscropTailoverlap is True:
            img1_cropbox_rm_tail = (0,
                                    0,
                                    img1.width,
                                    self.tailoverlapBox[1])
            # 如果img2为最后一张图片时，img2不用去掉tail部分
            if isEnd:
                img2_cropbox_rm_head_tail = (0,
                                             self.headoverlapBox[3],
                                             img2.width,
                                             img2.height
                                             )
            else:
                img2_cropbox_rm_head_tail = (0,
                                             self.headoverlapBox[3],
                                             img2.width,
                                             self.tailoverlapBox[1]
                                             )

            img1_cropfile = img1.crop(img1_cropbox_rm_tail)
            # img1_cropfilename = 'img1' + str(random.randint(1, 10000)) + '.jpg'
            # img1_cropfile.save(getDesktopPath() + img1_cropfilename)
            img2_cropfile = img2.crop(img2_cropbox_rm_head_tail)
            # img2_cropfilename = 'img2' + str(random.randint(1, 10000)) + '.jpg'
            # img2_cropfile.save(getDesktopPath() + img2_cropfilename)

            img1_cropfile_box = ()

            def findoverlapline():
                # 查找重叠的行
                # 1, 分别取img1的lin0, line15, line100行的RGB值进行比对
                # 2, 如果三个值都相同则找到
                img2_cropfile_pixel_list0 = list()
                img2_cropfile_pixel_list1 = list()
                img2_cropfile_pixel_list2 = list()
                for w in range(int(img2_cropfile.width * 3 / 4)):
                    img2_cropfile_pixel_list0.append(img2_cropfile.getpixel((w, 3)))
                    img2_cropfile_pixel_list1.append(img2_cropfile.getpixel((w, 100)))
                    img2_cropfile_pixel_list2.append(img2_cropfile.getpixel((w, 200)))

                # 在图片img1中自上而下的查找重叠的行
                for h in range(img1_cropfile.height - 200):
                    line0sum, line1sum, line2sum = 0, 0, 0
                    img1_cropfile_pixel_list0 = list()
                    img1_cropfile_pixel_list1 = list()
                    img1_cropfile_pixel_list2 = list()
                    for w in range(int(img1_cropfile.width * 3 / 4)):
                        img1_cropfile_pixel_list0.append(img1_cropfile.getpixel((w, h + 3)))
                        img1_cropfile_pixel_list1.append(img1_cropfile.getpixel((w, h + 100)))
                        img1_cropfile_pixel_list2.append(img1_cropfile.getpixel((w, h + 200)))

                    for i in range(int(img1_cropfile.width * 3 / 4)):
                        # a/b/c为img1的RGB value
                        # x/y/z为img2的RGB value
                        a0, b0, c0 = img1_cropfile_pixel_list0[i]
                        a1, b1, c1 = img1_cropfile_pixel_list1[i]
                        a2, b2, c2 = img1_cropfile_pixel_list2[i]
                        x0, y0, z0 = img2_cropfile_pixel_list0[i]
                        x1, y1, z1 = img2_cropfile_pixel_list1[i]
                        x2, y2, z2 = img2_cropfile_pixel_list2[i]
                        if abs(a0 - x0) < 20 and abs(b0 - y0) < 20 and abs(c0 - z0) < 20:
                            line0sum += 1
                        if abs(a1 - x1) < 20 and abs(b1 - y1) < 20 and abs(c1 - z1) < 20:
                            line1sum += 1
                        if abs(a2 - x2) < 20 and abs(b2 - y2) < 20 and abs(c2 - z2) < 20:
                            line2sum += 1
                    # print(f'line0sum:{line0sum}  line1sum:{line1sum}  line2sum:{line2sum}')
                    if line0sum == line1sum == line2sum == int(img1_cropfile.width * 3 / 4):
                        # print(f'h_tail:{h}')
                        # img1_cropfile_box = (0, 0, img1_cropfile.width, h)
                        return h
                # 如果找不到，就返回整个整页高度-滑动的距离-头部重叠h-尾部重叠h
                return img1_cropfile.height - self.swipe_distance - self.tailoverlapBox[3] - self.headoverlapBox[3]

            hFlag = findoverlapline()
            # if hFlag == False:
            #     # print('没有找到重叠的行')
            #     img1_cropfile_box = (0, 0, img1_cropfile.width, img1_cropfile.height - self.swipe_distance)
            #     self.imgcropboxList.append(img1_cropfile_box)
            # else:
            if isFirst is True:
                img1_cropfile_box = (0, 0, img1_cropfile.width, hFlag)
                location = (0, 0)
                self.longimage_length += hFlag
                self.imgcropboxList.append(img1_cropfile_box)
                self.imgpasteLoctionList.append(location)
            else:
                img1_cropfile_box = (0, self.headoverlapBox[3], img1_cropfile.width, hFlag)
                location = (0, self.longimage_length)
                self.longimage_length += hFlag - self.headoverlapBox[3]
                self.imgcropboxList.append(img1_cropfile_box)
                self.imgpasteLoctionList.append(location)

    # 将所有截图拼接成一个长图
    def sewImg(self):
        if len(self.imgPathList) == 1:
            shutil.move(self.imgPathList[0], getDesktopPath())
            return

        print('等待长图生成至桌面ing... ...')
        self.openImg()
        self.findHeadOverlap()
        self.findTailOverlap()
        # 在给img1赋值前将img1的类型转换成与newImg返回值类型一样
        img1 = self.imgInfoList[0].crop(self.imgInfoList[0].getbbox())
        # print(f'type: {type(img1)}')

        if self.tailoverlapBox == ():
            self.iscropTailoverlap = False

        # 前除最后一张的所有图片的待paste的info:location/pastebox
        for i in range(self.imgnum - 1):
            img1 = self.imgInfoList[i]
            img2 = self.imgInfoList[i + 1]
            if i == 0:
                self.findoverlap(img1, img2, True, False)
            else:
                self.findoverlap(img1, img2, False, False)

        # 添加最后一张图片的paste info进去.
        location = (0, self.longimage_length)
        self.longimage_length += self.imgInfoList[self.imgnum - 1].height - self.headoverlapBox[3]
        self.imgcropboxList.append((0, self.headoverlapBox[3], self.imgInfoList[self.imgnum - 1].width,
                                    self.imgInfoList[self.imgnum - 1].height))
        self.imgpasteLoctionList.append(location)

        # print(f'imgnum:{self.imgnum}')
        # print(f'imgInfoList:{self.imgInfoList}')
        # print(f'imgcropboxList:{self.imgcropboxList}')
        # print(f'imgpasteLoctionList:{self.imgpasteLoctionList}\n\n')

        # paste所有图片至longimage
        longImage = Image.new('RGB', (self.imgInfoList[0].width, self.longimage_length))
        for index in range(self.imgnum):
            print(f'正在进行第{index + 1}张图的拼接... ...')
            im = self.imgInfoList[index].crop(self.imgcropboxList[index])
            longImage.paste(im, self.imgpasteLoctionList[index])
        print(f'长图拼接完成，已保存在桌面.')
        longImage.save(getDesktopPath() + 'longImage.jpg')

    def run(self):
        # 只截一张图的case
        subprocess.run("cls", shell=True)
        print('wait for device to connect... ...')
        subprocess.run('adb wait-for-device', shell=True)
        # 需要截长图的case
        if self.cmd == '1':
            # 修改工作目录
            os.chdir('c:\\test_screenshot')
            # 修改save2destFlag，保证截长图时保存至c:\\test_screenshot
            self.save2destFlag = False
            # 截图过程
            self.screenshot()
            w, h = Image.open(self.imgPathList[0]).size
            cmd = 'adb shell input swipe ' + str(int(w / 2)) + ' ' + str(int(h * 2.5 / 4)) + ' ' + str(
                int(w / 2)) + ' ' + str(int(h / 4))
            self.swipe_distance = int(h * 3 / 4) - int(h / 4)
            enter = input('输入回车键继续截图,q结束长截图:').strip().lower()
            while True:
                if enter == 'q':
                    print(f'当前共截图{len(self.imgPathList)}张.')
                    break
                elif enter == '':
                    subprocess.run(cmd, shell=True, encoding='utf-8', capture_output=True)
                    self.screenshot()
                    enter = input('输入回车键继续截图,q结束长截图:').strip().lower()
                else:
                    enter = input('输入回车键继续截图,q结束长截图:').strip().lower()
            # 长图拼接过程
            start = time.time()
            self.sewImg()
            end = time.time()
            print(f'共耗时：{end - start:>0.2f}秒')


if __name__ == '__main__':
    key = input('(截图请输入1, 长截图请输入1,):')
    if key.strip() == '1':
        Screenshot(key).run()
    else:
        print('输入有误!!!')