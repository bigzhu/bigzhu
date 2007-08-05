# -*- coding: GB2312 -*-
import httplib, urllib,re
import datetime

FUND_CODE = "161706"
SALE_DATE="2007-06-22"
SALE_MONEY = 5000.0
TODAY_DATE=datetime.date.today()

PANEL = "biz.finance.sina.com.cn"
USERAGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv: 1.8.0.1) Gecko/20060111 Firefox/1.5.0.1'
PATH="/fundinfo/open/lsjz.php?fund_code="

"""
用来自动抓取基金的值，获取对应的利润情况.
author:jun tsai
revision:$Revision: 3191 $
since:0.1
""" 
def get_found_value(fund_code,sale_date,sale_money):
    """自动抓取基金净值的脚本程序,通过给定的基金代码，买基金的日期，以及投入使用的钱,
    来自动抓取基金的净值，以及利润
    """
    
    params = urllib.urlencode({"startdate1":sale_date,"enddate1":TODAY_DATE}) 
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
               'Referer' :'https://'+PANEL+PATH+fund_code, 'User-Agent':USERAGENT 
               }
    conn = httplib.HTTPConnection(PANEL)
    conn.request("POST", PATH+fund_code, params, headers)
    response = conn.getresponse()
    data = response.read()
    data=data.decode ("gb2312")
    conn.close();
    pattern = '<title>(.+)\('+fund_code+'\)'
    all_matches = re.findall(pattern,data);

    fund_name =  all_matches[0].encode("GB2312") 
#    print all_matches[0]
    
    pattern='<a href=\'./lsjz_dwjz.php\?jzrq=(.*)\'[\s]+target=_blank>(.*)</a>'
    all_matches=re.findall(pattern,data);
    
    today_value =  float(all_matches[0][1]) 
    sale_value = float(all_matches[len(all_matches)-1][1])
    sale_count = sale_money/sale_value
    value=(today_value-sale_value)*sale_count
    print "基金代码："+construct_block(10,fund_code)+"名称："+construct_head_block(20,fund_name)+"购买净值：" +construct_block(10,sale_value.__str__())+"购买数：" +construct_block(20,sale_count.__str__())+"今日净值：" +construct_block(10,today_value.__str__())+"利润：" +construct_block(20,value.__str__())+"|" 
def construct_block(length,str):    
    r=' '+str
    while(length>len(r)):
        r+=' ' 
    return r

def construct_head_block(length,str):    
    r=' '+str
    head_str_len=len( str.decode("GB2312"))
    while(length>(len(r)-head_str_len)):
        r+=' '
    return r
    
#print "+-----------------------------------------------------------------------------------------------+" 
#print "|"+construct_head_block(10,"代码")+"|"+construct_head_block(20,"名称")+"|"+construct_head_block(10,"购买净值")+"|"+construct_head_block(20,"购买数")+"|"+construct_head_block(10,"今日净值")+"|"+construct_head_block(20,"利润")+"|" 
#print "+-----------------------------------------------------------------------------------------------+"
#get_found_value("161706","2007-06-22",5000.0)
#get_found_value("260110","2007-06-10", 5000.0)
#get_found_value("070011","2007-06-23",5000.0)
get_found_value("240009","2007-07-30",10000.0)
print "+------------------------------------------------------------------------------"
get_found_value("240010","2007-07-30",10000.0)
#print "+-----------------------------------------------------------------------------------------------+"
