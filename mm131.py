import os,sys,time,uuid
import urllib
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import pymysql

download_path = os.path.dirname(os.path.abspath(__file__))

class mm131spider(object):
    def __init__(self,url):
        self.url=url

    def parse(self,content):
        reg = r'src="(.+?\.jpg)"'
        imgre = re.compile(reg)
        matchs = re.findall(imgre,content)
        return matchs

    def downloads(self,urls,title):
        d_path = download_path+"\mm131\\"
        d_path = d_path+title
        print(d_path)
        if not os.path.exists(d_path):
            os.mkdir(d_path)
        for url in urls:
            filename = url.split("/")[-1]
            print(url)
            print("Downloads %s" % (filename))
            output = "%s\\%s" % (d_path,filename)
            #urllib.request.urlretrieve(url,output)   #会有假死状态，如果阻塞就不会一直抓下去
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
            re = requests.get(url,headers=headers)
            binfile = open(output,'wb')
            binfile.write(re.content)
            binfile.close()

    def getHtml(self,url):
        re = requests.get(url)
        content = re.content.decode('gb2312','ignore')
        return content


    def fanye(self,page_total,baseurl,title):
        for i in range(2,int(page_total)):
            url_next = "http://www.mm131.com/xinggan/"+baseurl+"_"+str(i)+".html"
            print(url_next)
            next_content = self.getHtml(url_next)
            soup_next = BeautifulSoup(next_content,"lxml")
            next_content_pic = soup_next.find_all('div',{'class':'content-pic'})
            next_urls = self.parse(str(next_content_pic[0]))
            self.downloads(next_urls,title)

    def getPic(self,url):
        print(url)
        content = self.getHtml(url)
        soup = BeautifulSoup(content,"lxml")
        #取标题
        #截取页面内容
        content = soup.find_all('div',{'class':'content'})
        title = content[0].h5.text
        content_pic = soup.find_all('div',{'class':'content-pic'})
        first_urls = self.parse(str(content_pic[0]))
        self.downloads(first_urls,title)
         #取翻页
        pages = soup.find_all('div',{'class':'content-page'})
        page_total = pages[0].span.text
        page_total = re.findall("\d+",page_total)
        baseurl = url.split('/')[-1]
        baseurl = baseurl.split('.')[0]
        self.fanye(page_total[0],baseurl,title)
        #取下一页
        next_page = soup.find_all('div',{'class':'updown'})
        next_page=next_page[0].a
        next_page=next_page['href']
        if next_page:
            return next_page

    def run(self):
        d_url = self.url
        next_page = d_url
        while 1:
            next_page=self.getPic(next_page)
            if next_page:
                continue
            else:
                break



if __name__ == "__main__":
    sp = mm131spider("http://www.mm131.com/xinggan/1999.html")
    sp.run()