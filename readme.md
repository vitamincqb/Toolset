# Blog Link:
    https://blog.csdn.net/lxy210781

# All_in_One
平时工作时的一个小工具（限android平台+python3.6.x)

此应用就是用于平时工作时的便利，因为在测试过程中有时要反正的抓取log和截图，都是一些常见的操作，但是又没有一个集中的tool. 

    2，Copy文件(MTKlog/DCIM/Copyfiles)至桌面 用法：
    -------------------------------------------
    1:仅删除mtklog文件夹
    可输入:'d m', 'd,m', 'd mtklog', 'd,mtklog', 'del mtklog', 'del,mtklog', 'del m', 'del,m'
    2:仅删除DCIM文件夹
    可输入:'d d','d,d',  'del d', 'del,d', 'del dcim','d dcim', 'del,dcim', 'd,dcim'
    3:仅删除00Tempfile文件夹
    可输入:'d cf', 'd c','d,cf', 'd,c', 'del cf', 'del c',  'del,cf', 'del,c',
    4:复制Mtklog至桌面then删除手机中的Mtklog文件夹
    可输入：'2', '2,', '2m', 'mtklog', '2mtklog',
    5:复制Mtklog/DCIM文件夹then删除手机中的Mtklog/DCIM文件夹
    可输入:'2mp','mp','2md', 'md'`
    6:复制DCIM文件夹至桌面then删除DCIM文件夹
    可输入：'2d', '2dcim', 'dcim'
    7:复制00Tempfile至桌面then询问是否删除00Tempfile文件夹
    可输入：'2c', '2cf', 'cf', 'Copyfile', 'copyfile'
    
    
    3，打开MTKlog 用法：
    ----------------
    cmd = '3', 打开mtklog主界面
    cmd = ('3 0', '3,0'), 关闭mtklog
    cmd = ('3 1', '3,1'), 开启mtklog

    4，Copy文件至手机　用法:
    -----------------------------------------
    cmd='4' , 复制手机中的00Tempfile文件夹至桌面
    cmd='4,', 在手机根目录新建00Tempfile
    
    
    8，导出APK to desk(前台正在使用的apk)　用法:
    -----------------------------------------
    cmd='8' , 将导出当前前台正在使用的apk至桌面
    cmd='8,', 仅输出当前信息的包信息
    
    #2018/6/24
    今天将有道翻译整合进去了.
    
# Copyfile2phone.py
当有以下这种需求时刚好可以用用这个tool（限android平台+python3.6.x)

    >>>重要提示 --请将待copy文件放置在桌面再进行操作<<<
    如要将PC上一个大文件复现到N台手机的根目录时，如果单台的Copy效率很慢；
    如用这个Tool, 可多台手机同时连接PC，只要确保每台手机adb连接成功;
    run Copyfile2phone.py，就可以多进程同时给多台手机复制文件，减少花在Copy文件上的总时间

    第一次run时，会在py同目录下自动新建一个coyfile2phyone.txt，并要求输入待copy的文件名；
    建议将要copy的文件直接拖入，会自动获取文件名并写入txt档中；
    下次run就会自动读取写入的文件名，不再要求输入待copy的文件名。

# youdao_translate
 爬虫的一个简单应用，利用有道翻译来进行中英文的互译。
    
    可进行中英文的互译. 

# Happy_moment
 利用爬虫实时在线爬的一个糗百小开心，有事没事，开心一下。
 
    主要待实现以下功能（based on python3.6.5)：
    1. 每按回车，就显示一条糗百，开心一下.
    2. 输入open回车，则用默认浏览器打开当前这条糗百
    3. 过滤掉image/video，只显示纯text的糗事
    4. 显示的形式为当前序号/内容/用户投票信息/当前糗百的Link
    
    如要run此pycode, 需要安装以下3rd lib
    1. requests (pip install requests)
    2. lxml (pip install lxml)
    
    如果不想安装python或3rd lib就想玩玩这个开心时刻小程序，可直接在列表中的Dist中下载Happy_moment.exe。
