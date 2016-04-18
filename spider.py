import os,sys,time,uuid
import urllib
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import pymysql

download_path = os.path.dirname(os.path.abspath(__file__))
#d_path = download_path+r"\test"
#print(d_path)
#test db

class spider(object):
    def __init__(self,url):
        self.url=url

    def parse(self,content):
        reg = r'src="(.+?\.jpg)"'
        imgre = re.compile(reg)
        #pattern = r'src="(http://.*\.jpg)\s*"'
        matchs = re.findall(imgre,content)
        return matchs

    def downloads(self,urls,title):
        d_path = download_path+r"\test\\"
        d_path = d_path+title
        print(d_path)
        if not os.path.exists(d_path):
            os.mkdir(d_path)
        for url in urls:
            filename = url.split("/")[-1]
            print(url)
            print("Downloads %s" % (filename))
            output = "%s/%s" % (d_path,filename)
            urllib.request.urlretrieve(url,output)

    def getHtml(self,url):
        re = requests.get(url)
        content = re.content.decode('utf-8','ignore')
        return content


    def fanye(self,page_ul,title):
        for page in page_ul:
            if page.text == '末页':
                max_page = page.a['href']
                if max_page:
                    end_page = max_page.split("_")[-1]
                    end_page = end_page.split(".")[0]
                if end_page :
                    for i in range(2,int(end_page)):
                        url_next = max_page.split("/")[-1]
                        url_next = url_next.split("_")[0]
                        url_next = "http://www.aitaotu.com/guonei/"+url_next+"_"+str(i)+".html"
                        print(url_next)
                        next_content = self.getHtml(url_next)
                        next_urls = self.parse(next_content)
                        self.downloads(next_urls,title)

    def getPic(self,url):
        print(url)
        content = self.getHtml(url)
        soup = BeautifulSoup(content,"lxml")
        #取标题
        title = soup.select('#photos')
        title = title[0].h1.text
        title = title.split("(")[0]
        #去掉某些标题结尾的空格
        title = title.rstrip()
        first_urls = self.parse(content)
        self.downloads(first_urls,title)
         #取翻页
        #pages = soup.select('div[class="pages"]')
        pages = soup.find_all('div',{'class':'pages'})
        page_ul = pages[0].ul
        self.fanye(page_ul,title)
        next_page = soup.find_all('div',{'class':'conpndiv'})
        next_page=next_page[0].p
        next_page=next_page.a['href']
        if next_page:
            return next_page

    def run(self):
        d_url = self.url
        next_page = d_url
        while 1:
            next_page = self.getPic(next_page)
            if next_page:
                next_page="http://www.aitaotu.com"+next_page
                continue
            else:
                break


class DBExecute(object):
    def __init__(self,**args):
        self.args = args
        #test
        self.con = pymysql.connect(host='localhost',user='root',db='py_content',port=3306,charset='utf8')

    def insert_db(self,table,col,values):
        con = self.con
        cur = con.cursor()
        sql = "insert into "+table+"("
        for c in col:
            sql = sql+c
        sql += ") values ("
        for v in values:
            v = "'"+v+"'"
            sql = sql+v
        sql += ")"
        try:
            cur.execute(sql)
            cur.close()
        except Exception:
            print("插入数据异常!")

    def __del__(self):
        self.con.close()

if __name__ == "__main__":
    sp = spider("http://www.aitaotu.com/guonei/369.html")
    sp.run()

