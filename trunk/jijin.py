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
�����Զ�ץȡ�����ֵ����ȡ��Ӧ���������.
author:jun tsai
revision:$Revision: 3191 $
since:0.1
""" 
def get_found_value(fund_code,sale_date,sale_money):
    """�Զ�ץȡ����ֵ�Ľű�����,ͨ�������Ļ�����룬���������ڣ��Լ�Ͷ��ʹ�õ�Ǯ,
    ���Զ�ץȡ����ľ�ֵ���Լ�����
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
    print "������룺"+construct_block(10,fund_code)+"���ƣ�"+construct_head_block(20,fund_name)+"����ֵ��" +construct_block(10,sale_value.__str__())+"��������" +construct_block(20,sale_count.__str__())+"���վ�ֵ��" +construct_block(10,today_value.__str__())+"����" +construct_block(20,value.__str__())+"|" 
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
#print "|"+construct_head_block(10,"����")+"|"+construct_head_block(20,"����")+"|"+construct_head_block(10,"����ֵ")+"|"+construct_head_block(20,"������")+"|"+construct_head_block(10,"���վ�ֵ")+"|"+construct_head_block(20,"����")+"|" 
#print "+-----------------------------------------------------------------------------------------------+"
#get_found_value("161706","2007-06-22",5000.0)
#get_found_value("260110","2007-06-10", 5000.0)
#get_found_value("070011","2007-06-23",5000.0)
get_found_value("240009","2007-07-30",10000.0)
print "+------------------------------------------------------------------------------"
get_found_value("240010","2007-07-30",10000.0)
#print "+-----------------------------------------------------------------------------------------------+"
