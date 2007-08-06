#@+leo-ver=4-thin-encoding=gb2312,.
#@+node:BIGZHU.20070731160918:@thin d:/bigzhu/python/python_project/get_cmfu.py
#@+at 
#@nonl
# ���С˵����
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
    cj = cookielib.CookieJar()#����Cookieʵ��
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))#����opener��Cookie����
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
        #���Ĵ���̫���淶��,��һ�����㷺�Ե�ƥ��������ʽ
        """
        cmfuURL = re.findall("showbook.asp\?bl_id=\d{1,}",cmfu)
        BookIdListTemp = [re.sub("showbook.asp\?bl_id=",'',k) for k in cmfuURL]
        """
        #�����ڻ�һЩ
        cmfuURL = re.findall("bl_id=\d{1,}",cmfu)
        BookIdListTemp = [re.sub("bl_id=",'',k) for k in cmfuURL]
        #BookIdListTemp = [re.sub("'",'',k) for k in BookIdListTemp]
        bookCount = len(BookIdList)
        for listTemp in BookIdListTemp:
            #����bookid�Ƿ���BookIdList������
            if listTemp in BookIdList:
                pass
            else:
                BookIdList.extend([listTemp])#�ӽ�ȥ
        print "ȡ���鱾��Ŀ:%i"%(len(BookIdList)-bookCount)        
    print "�ϼ�ȡ�������鱾:%i"%len(BookIdList)
    return BookIdList

#@-node:BIGZHU.20070731160918.1:<<getBookIdList>>
#@nl
#@<<getBookName>>
#@+node:BIGZHU.20070731164705:<<getBookName>>
def getBookName(opener,bookId=''):
    if bookId == '':
        print "����BookIdList�ǿյ�"
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
        #�ж��ļ��Ƿ��Ѿ�����
        if os.path.isfile(os.getcwd()+"\\���\\%s.txt"%bookName):
            print "%s �Ѿ�����"%bookName
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

            f=open(os.getcwd()+"\\���\\%s.txt"%bookName,"wb")
            f.write(bookData)
            f.close()
            print 'get book %s ���'%bookName
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
    """��������url,save ��ini��
    ������url,����
    ÿ��ʹ��,�Զ���ȡini��url,�ṩʹ��"""
    def __init__(self):
        pass
    #@    <<saveURL>>
    #@+node:BIGZHU.20070802171013.1:<<saveURL>>
    def saveURL(self,urlList=[]):
        '''�洢�µ�url��URL.ini��'''


        try:
            f=open(os.getcwd()+"\\���\\URL.ini","wb")#׷������
        except IOError:
            print "�ļ��򿪴���"
            #��ʽ�����ַ���
        s_urlList = ";".join(urlList)
        f.write(s_urlList)
        f.close()    
    #@-node:BIGZHU.20070802171013.1:<<saveURL>>
    #@nl
    #@    <<getURLIni>>
    #@+node:BIGZHU.20070802171013.2:<<getURLIni>>
    def getURLIni(self):
        """��ȡ URL.ini�е�url
        ����һ��URL list"""
         #�ж�Ŀ¼�Ƿ����
        if os.path.exists(os.getcwd()+"\\���"):
            pass
        else:
            print "����Ŀ¼ \���"
            os.mkdir("���")

        iniData=''
        if os.path.isfile(os.getcwd()+"\\���\\URL.ini"):
            f=open(os.getcwd()+"\\���\\URL.ini","rb")
            iniData = f.read()
            f.close()
        else:
            print "URL.txt������,����֮"
            f=open(os.getcwd()+"\\���\\URL.ini","wb")
            #iniData = f.read()
            f.close()
        return iniData.split(";")#��ʽ����list    
    #@-node:BIGZHU.20070802171013.2:<<getURLIni>>
    #@nl




#@-node:BIGZHU.20070802171013:<<class ProcessURL>>
#@nl
#@<<main>>
#@+node:BIGZHU.20070731164705.1:<<main>>
if __name__ == '__main__':
    opener = getCookie()
    #urlList =["http://www.cmfu.com/index.asp","http://www.cmfu.com/listbookqb.asp?pageid=2007-8-1%2012:26&status=down","http://www.cmfu.com/listbookqb.asp?pageid=2007-7-31%2023:03&status=down","http://www.cmfu.com/index_wxxx.asp"]
    #��źͶ�ȡurl
    urlType = ProcessURL()
    urlList = urlType.getURLIni()
    saveIni = 0 # ��ʶ�Ƿ���url ����
    while True:
        url = raw_input("Ҫ��ȡ������ĳ��ҳ��:  ")
        if url=='':
            break
        if url in urlList:
            print "%s ����,����֮"%url
        else:
            urlList.extend([url])
            print "%s ���µ�,���֮"%url
            saveIni =1 
    #url = 'http://www.cmfu.com/index.asp'


    bookIdList=getBookIdList(opener,urlList)


    for i in bookIdList:
        thread = runGetFile(i)
        thread.start()
    #�洢��ini��
    if saveIni == 1:
        urlType.saveURL(urlList)
#@-node:BIGZHU.20070731164705.1:<<main>>
#@nl
#@nonl
#@-node:BIGZHU.20070731160918:@thin d:/bigzhu/python/python_project/get_cmfu.py
#@-leo
