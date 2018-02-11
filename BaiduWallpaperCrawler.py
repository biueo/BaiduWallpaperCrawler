# -*- coding: utf-8 -*-

__author__="ddc"

import urllib.request as ur
import urllib.parse
import re
import os
import time
import socket

class Wallpaperspider(object):
    def __init__(self,path='C://壁纸/',classname=None,subclassname=None,pn=4,keyword='壁纸'):
        self.classname=classname
        self.subclassname=subclassname
        self.keyword=keyword
        self.path=path
        self.pn=pn

    def geturl(self,pn):
        if type(pn)!=int:
            print('Error:pn is not an int')
            return none
        if not self.classname:
            key_code=ur.quote(self.keyword)
            url="http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%s&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&pn=%s&rn=30&itg=1&gsm=1e&1516354255134="%(key_code,key_code,pn)
        elif not self.subclassname:
            class_code=ur.quote(self.classname)
            key_code=ur.quote(self.keyword)
            url="http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s+%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%s+%s&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&pn=%s&rn=30&itg=1&gsm=1e&1516354255134="%(key_code,class_code,key_code,class_code,pn)
        else:
            class_code=ur.quote(self.classname)
            key_code=ur.quote(self.keyword)
            sub_code=ur.quote(self.subclassname)
            url="http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s+%s+%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&word=%s+%s+%s&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&pn=%s&rn=30&itg=1&gsm=1e&1516354255134="%(key_code,class_code,sub_code,key_code,class_code,sub_code,pn)
        return url

    def getimgurls(self,data):
        reg='\[\{"ObjURL":"(.*?)"'
        imglist= re.compile(reg).findall(data.decode('utf-8'),re.I)  
        imglist=[i.replace('\\','') for i in imglist]
        return imglist

    def moreimgurls(self):
        imgurls=[]
        for i in range(1,self.pn):
            pn=i*30
            htmlurl=self.geturl(pn)
            headers=('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
            opener=ur.build_opener()
            opener.addheaders=[headers]
            ur.install_opener(opener)
            data=opener.open(htmlurl).read()
            imgurls+=self.getimgurls(data)
        self.imgurls=imgurls
        return self.imgurls

    def downpic(self):
        self.moreimgurls()
        pici=1
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        headers=('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        opener=ur.build_opener()
        opener.addheaders=[headers]
        ur.install_opener(opener)
        for imgurl in self.imgurls:
            pathname=self.path+imgurl[-38:-16]+'.jpg'
            print('你正在下载第%s张图片...'%pici)
            try:
                socket.setdefaulttimeout(15)  #超时设定15秒
                ur.urlretrieve(imgurl,pathname)
                pici+=1
            except socket.error: 
                print("下载超时")
            except Exception as e:
                print("未成功下载",imgurl)
                continue
            time.sleep(1)
        allnum=pici-1
        print('总共下载了%s张图片'%allnum)
        return allnum


down=Wallpaperspider(classname='不同风格',subclassname='风景',pn=3)
down.downpic()