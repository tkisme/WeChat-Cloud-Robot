#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: hkk
# @Date:   2015-11-20 11:51:48
# @Last Modified by:   anchen
# @Last Modified time: 2015-12-09 12:39:44
import ssl
import urllib2
import httplib,socket
ssl._create_default_https_context = ssl._create_unverified_context

class WeChat(object):
    """docstring for ClassName"""

    def genQrcodeUuid(self):

        url = "https://login.weixin.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN"
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
            
        return res[50:62]
    def ScanStauts(self,uuid):
        #返回200：手机已确认登入；返回201：等待手机确认；返回408：还未确认或者还未扫码；返回400：二维码失效
        #https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=QelLRKlwVA==&tip=1
        try:
            url = "https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid="+uuid+"&tip=1"
            req = urllib2.Request(url)
            res_data = urllib2.urlopen(req)
            res = res_data.read()
            return res           
        except ssl.SSLError as e:
            return 'window.code=408;'
    def GetWeChatCookies(self,url):
        if 'wx2.qq.com' in url:
            HOSTNAME = 'wx2.qq.com'
        else:
            HOSTNAME = 'wx.qq.com'
        parm = url[18:]
        conn = httplib.HTTPSConnection(HOSTNAME)
        conn.putrequest('GET', parm)
        conn.endheaders()
        response = conn.getresponse()
        cookies = response.getheader('set-cookie')
        body = response.read()
        msg = dict()
        # req = urllib2.Request(url)
        # res_data = urllib2.urlopen(req)
        # res = res_data.read()
        #print res
        if 'OK' in body:
            msg['COOKIES']= cookies
            msg['MSG'] = body
            return msg
        else:
            return None


    
       
# a =  WeChat().GetWeChatCookies('https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=A2j-JSAujsdhX74L_hbojbqH@qrticket_0&uuid=QYHhlI68dg==&lang=zh_CN&scan=1448935970&vcdataticket=AQbbnFwLqqgifEfbcQQ2ro9t&vccdtstr=N-SvpfgDKjk_LbK9VEEllhof1w6Z8gIaqOC2_G2ocdCzD_1kFvHtgoZgpKg5fnrw')
# print a