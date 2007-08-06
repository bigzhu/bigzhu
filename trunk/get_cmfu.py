#@+leo-ver=4-thin-encoding=gb2312,.
#@+node:BIGZHU.20070731160918:@thin d:/bigzhu/python/python_project/get_cmfu.py
#@+at 
#@nonl
# 起点小说爬虫
#@-at
#@@c
#@@language python
#@+others
#@+node:BIGZHU.20070731161308:import
import httplib,urllib2,urllib,cookielib,re,threading
import os
#@nonl
#@-node:BIGZHU.20070731161308:import
#@+node:BIGZHU.20070731160928:getCookie
def getCookie():
    cj = cookielib.CookieJar()#建立Cookie实例
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))#建立opener与Cookie关联
    return opener
#@-node:BIGZHU.20070731160928:getCookie
#@-others
#@<<getBookIdList>>
#@+node:BIGZHU.20070731160918.1:<<getBookIdList>>
def getBookIdList(opener,urlList):

    BookIdList = []
    for i in urlList:
        url=i
        print url
        request = urllib2.Request(url)
        cmfu = opener.open(request).read()
        #cmfuURL = re.findall("<a href='showbook.asp\?bl_id=\d{1,}'",cmfu)
        #BookIdListTemp = [re.sub("<a href='showbook.asp\?bl_id=",'',k) for k in cmfuURL]
        #BookIdListTemp = [re.sub("'",'',k) for k in BookIdListTemp]
        #起点的代码太不规范了,想一个更广泛性的匹配正则表达式
        """
        cmfuURL = re.findall("showbook.asp\?bl_id=\d{1,}",cmfu)
        BookIdListTemp = [re.sub("showbook.asp\?bl_id=",'',k) for k in cmfuURL]
        """
        #更大众化一些
        cmfuURL = re.findall("bl_id=\d{1,}",cmfu)
        BookIdListTemp = [re.sub("bl_id=",'',k) for k in cmfuURL]
        #BookIdListTemp = [re.sub("'",'',k) for k in BookIdListTemp]
        bookCount = len(BookIdList)
        for listTemp in BookIdListTemp:
            #检查该bookid是否在BookIdList中已有
            if listTemp in BookIdList:
                pass
            else:
                BookIdList.extend([listTemp])#加进去
        print "取得书本数目:%i"%(len(BookIdList)-bookCount)        
    print "合计取得下载书本:%i"%len(BookIdList)
    return BookIdList

#@-node:BIGZHU.20070731160918.1:<<getBookIdList>>
#@nl
#@<<getBookName>>
#@+node:BIGZHU.20070731164705:<<getBookName>>
def getBookName(opener,bookId=''):
    if bookId == '':
        print "传入BookIdList是空的"
    bookURL = 'http://www.cmfu.com/readbook.asp?bl_id=%s'%bookId
    request = urllib2.Request(bookURL)
    bookPage = opener.open(request).read()
    opener.close()
    bookname =  re.findall('bookname=\S{1,}',bookPage)

    bookname = [re.sub("bookname=",'',k) for k in bookname]
    bookname = [re.sub('"','',k) for k in bookname][0]

    return bookname

#@-node:BIGZHU.20070731164705:<<getBookName>>
#@nl
#@<<getTextFile>>
#@+node:BIGZHU.20070731171721:<<getTextFile>>
def getTextFile(opener,bookId):
        bookName = getBookName(opener,bookId)
        #判断文件是否已经存在
        if os.path.isfile(os.getcwd()+"\\起点\\%s.txt"%bookName):
            print "%s 已经存在"%bookName
        else:
            url = 'http://download.cmfu.com/pda/%s.txt'%bookId
            try:
                bookData = opener.open(url).read()
            except :
                print "2 %s"%bookName
                try:
                    bookData = opener.open(url).read()
                except :
                    print "last try %s"%bookName
                    try:
                        bookData = opener.open(url).read()
                    except :
                        print "end  try %s"%bookName

            opener.close()

            f=open(os.getcwd()+"\\起点\\%s.txt"%bookName,"wb")
            f.write(bookData)
            f.close()
            print 'get book %s 完毕'%bookName
#@-node:BIGZHU.20070731171721:<<getTextFile>>
#@nl
#@<<class runGetFile>>
#@+node:BIGZHU.20070801172939:<<class runGetFile>>
class runGetFile(threading.Thread):
    def __init__(self,bookId):
        threading.Thread.__init__(self)
        self.bookId = bookId
        #self.opener = opener
    def run(self):
        opener = getCookie()
        getTextFile(opener,self.bookId)
#@nonl
#@-node:BIGZHU.20070801172939:<<class runGetFile>>
#@nl
#@<<class ProcessURL>>
#@+node:BIGZHU.20070802171013:<<class ProcessURL>>
class ProcessURL:
    """对新输入url,save 到ini中
    对已有url,忽视
    每次使用,自动读取ini的url,提供使用"""
    def __init__(self):
        pass
    #@    <<saveURL>>
    #@+node:BIGZHU.20070802171013.1:<<saveURL>>
    def saveURL(self,urlList=[]):
        '''存储新的url到URL.ini中'''


        try:
            f=open(os.getcwd()+"\\起点\\URL.ini","wb")#追加内容
        except IOError:
            print "文件打开错误"
            #格式化成字符串
        s_urlList = ";".join(urlList)
        f.write(s_urlList)
        f.close()    
    #@-node:BIGZHU.20070802171013.1:<<saveURL>>
    #@nl
    #@    <<getURLIni>>
    #@+node:BIGZHU.20070802171013.2:<<getURLIni>>
    def getURLIni(self):
        """读取 URL.ini中的url
        返回一个URL list"""
         #判断目录是否存在
        if os.path.exists(os.getcwd()+"\\起点"):
            pass
        else:
            print "创建目录 \起点"
            os.mkdir("起点")

        iniData=''
        if os.path.isfile(os.getcwd()+"\\起点\\URL.ini"):
            f=open(os.getcwd()+"\\起点\\URL.ini","rb")
            iniData = f.read()
            f.close()
        else:
            print "URL.txt不存在,创建之"
            f=open(os.getcwd()+"\\起点\\URL.ini","wb")
            #iniData = f.read()
            f.close()
        return iniData.split(";")#格式化成list    
    #@-node:BIGZHU.20070802171013.2:<<getURLIni>>
    #@nl




#@-node:BIGZHU.20070802171013:<<class ProcessURL>>
#@nl
#@<<main>>
#@+node:BIGZHU.20070731164705.1:<<main>>
if __name__ == '__main__':
    opener = getCookie()
    #urlList =["http://www.cmfu.com/index.asp","http://www.cmfu.com/listbookqb.asp?pageid=2007-8-1%2012:26&status=down","http://www.cmfu.com/listbookqb.asp?pageid=2007-7-31%2023:03&status=down","http://www.cmfu.com/index_wxxx.asp"]
    #存放和读取url
    urlType = ProcessURL()
    urlList = urlType.getURLIni()
    saveIni = 0 # 标识是否有url 更新
    while True:
        url = raw_input("要截取的起点的某个页面:  ")
        if url=='':
            break
        if url in urlList:
            print "%s 已有,忽视之"%url
        else:
            urlList.extend([url])
            print "%s 是新的,添加之"%url
            saveIni =1 
    #url = 'http://www.cmfu.com/index.asp'


    bookIdList=getBookIdList(opener,urlList)


    for i in bookIdList:
        thread = runGetFile(i)
        thread.start()
    #存储到ini中
    if saveIni == 1:
        urlType.saveURL(urlList)
#@-node:BIGZHU.20070731164705.1:<<main>>
#@nl
#@nonl
#@-node:BIGZHU.20070731160918:@thin d:/bigzhu/python/python_project/get_cmfu.py
#@-leo
