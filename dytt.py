import os,sys,time,uuid
import urllib
import requests
import re
import jieba
import time
import random
import string
from bs4 import BeautifulSoup
from lxml import etree
import pymysql
from PIL import Image

download_path = os.path.dirname(os.path.abspath(__file__))

class dyttSpider(object):
    def __init__(self,url):
        self.url = url

    def getHtml(self,url,charset='utf-8'):
        re = requests.get(url)
        content = re.content.decode('gb2312','ignore')
        return content

    def downloadPic(self,pic_url,pic_name):
        #download the cover picture and return the picture path
        d_path = download_path+'\zxdytt\\'
        if not os.path.exists(d_path):
            os.mkdir(d_path)
        print("Downloads %s" % (pic_url))
        output = "%s\\%s" % (d_path,pic_name+'.jpg')
        #urllib.request.urlretrieve(url,output)   #会有假死状态，如果阻塞就不会一直抓下去
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
        re = requests.get(pic_url,headers=headers)
        binfile = open(output,'wb')
        binfile.write(re.content)
        binfile.close()
        #covert the resize image

        local_url = ''
        return local_url

    def compress_img(self,path,size,pic_name):
        #thumb size
        size = (120,120)
        img = Image.open(path)
        img.thumbnail(size)
        img.save(pic_name+'-lp','jpeg')

    def fanye(self,page_url,title):
        return
        #get the content of movie list source

    #parse the sigle movie page
    def parseMovieContent(self,m_content):
        m_soup = BeautifulSoup(m_content,'lxml')
        m_desc = m_soup.find('div',{'class','co_area2'})
        title = m_desc.find('div',{'class':'title_all'})
        title = title.h1.string
        #cut the title to keywords list
        key_words = jieba.cut(title)
        s_title = title
        key_words = ','.join(key_words)
        #time
        post_time = time.time()
        temp_time = time.localtime(post_time)
        short_time = time.strftime('%y%m%d',temp_time)
        #download the pagecoverimg

        #description and content
        desc = m_desc.select('#Zoom')
        desc = desc[0].find_all('p')

        type_id = 5
        type_id2 = 0
        sortrank = post_time
        flag = 'p'
        ismake = 1
        channel = 17
        arcrank = 0
        click = random.randint(0,100)
        money = 0
        m_title = title
        short_title = s_title
        color = ''
        writer = 2016
        source = '全集'
        litpic = '/uploads/allimg/'+short_time+'/'+''.join(random.sample(string.ascii_letters+string.digits, 15))
        pubdate = post_time
        senddate = post_time
        mid = 1
        keywords = key_words
        lastpost = 0
        scores = 0
        goodpost = 0
        badpost = 0
        voteid = 0
        notpost = 0
        description = desc

        m_values = []

        print(desc)

        #return

    #test
    def runTest(self):
        content = self.getHtml('http://www.dy2018.com/i/96467.html')
        self.parseMovieContent(content)

    def run(self,baseurl):
        #connect to db
        db = DBExecute()
        content = self.getHtml(self.url,'gb2312')
        soup = BeautifulSoup(content,'lxml')
        #get movie list data on the first page
        m_list = soup.find_all('div',{'class':'co_content8'})
        m_list = m_list[0].find_all('table')
        for x in m_list:  #index the movie title and content
            a_b = x.b.select('a')
            m_url = a_b[1]['href']
            m_title = a_b[1]['title']
            m_content = self.getHtml(baseurl+m_url,'gb2312')
            m_values = self.parseMovieContent(m_content)
            db.insert_content_db(m_values)





#db executor
class DBExecute(object):
    def __init__(self):
        self.con = pymysql.connect(host='localhost',user='root',passwd='root',db='dedecaiji',port=3306,charset='utf8')

    def insert_content_db(self,values):
        con = self.con
        cur = con.cursor()
        sql = "insert into gope_cn_archives values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"   # 31total
        try:
            cur.execute(sql,values)
            mid=int(cur.lastrowid)  #get the movie id
            #construct movie values array
            m_values = []
            m_values.append(mid)

            m_insert_sql="insert into gope_cn_addonmovie values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # 9 total
            cur.execute(m_insert_sql,m_values)
            cur.connection.commit()
        except:
            print("insert Error!")

    def __del__(self):
        self.con.close()

if __name__ == '__main__':
    base_url = 'http://www.dy2018.com'
    dy = dyttSpider('http://www.dy2018.com/2/')
    dy.runTest()
    #dy.run(base_url)