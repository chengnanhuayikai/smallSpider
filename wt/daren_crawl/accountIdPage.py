
import hashlib
import json
import time
import requests
import random
import re
import string
from urllib import parse






class getAccountPage():

    headers = {}
    contentId_list = []
    t = str(int(time.time() * 1000))
    appKey = '12574478'


    def __init__(self,accountId):
        self.accountId = accountId


    def hex_md5(self,string):
        '''
        MD5 加密
        :param string:
        :return:
        '''
        m = hashlib.md5()
        m.update(string.encode('UTF-8'))
        return m.hexdigest()


    def setHeaders(self ,html=None):
        '''
        设置headers
        :return:
        '''
        if html == None:
            url = 'https://acs.m.taobao.com/h5/mtop.taobao.maserati.xplan.render/1.0/'
            data = '{"accountId":"2953887409","siteId":41,"pageId":"6273","fansId":"3020335190","status":0,"currentPage":1,"currentModuleIds":"","contentId":"","tabString":"homepage","subTabString":"new_feeds"}'
            params = {
                'appKey': self.appKey,
                'data': data
            }
            # 请求空获取cookies
            html = requests.get(url, params=params)
            _m_h5_tk = html.cookies['_m_h5_tk']
            _m_h5_tk_enc = html.cookies['_m_h5_tk_enc']
            token = _m_h5_tk.split('_')[0]
            cookie_t = html.cookies['t']
            u = token + '&' + self.t + '&' + self.appKey + '&' + data
            # MD5加密
            sign = self.hex_md5(u)
            headers = {
                'cookie': '_m_h5_tk=' + _m_h5_tk + '; _m_h5_tk_enc=' + _m_h5_tk_enc,
            }

            self.headers = headers


    def get_parseAccountIdPage(self ,info):
        '''
        解析page数据
        :return:
        '''
        feeds = info.get('data').get('result').get('data')[-1].get('co').get('result').get('data').get('feeds')
        # print(feeds)
        if feeds == []:
            return False
        else:
            for content in feeds:
                if content.get('feedType') == '500' or content.get('feedType') == '504':
                    contentId = content.get('feedId')
                    self.contentId_list.append(contentId)


            return True







    def get_accountIdPage(self ,accountId ,page):
        '''
        请求page页面
        :param accountId:
        :param page:
        :return:
        '''

        if self.headers == {}:
            self.setHeaders()


        url = 'https://acs.m.taobao.com/h5/mtop.taobao.maserati.xplan.render/1.0/'

        data = '{"accountId":"' + str(accountId) + '","siteId":41,"pageId":6273,"fansId":"' + str(
            accountId) + '","status":0,"currentPage":' + str(
            page) + ',"currentModuleIds":"","contentId":"","tabString":"homepage","subTabString":"new_feeds"}'


        token = self.headers.get('cookie').split(';')[0].split('=')[-1].split('_')[0]
        t = self.t
        u = token + '&' + t + '&' + self.appKey + '&' + data
        # MD5加密
        sign = self.hex_md5(u)

        params = {
            'appKey': self.appKey,
            't': t,
            'sign': sign,
            'data': data
        }
        response = requests.get(url, headers=self.headers, params=params)
        if "令牌过期" in response.text:
            self.setHeaders()
            self.get_accountIdPage(accountId ,page)


        return json.loads(response.text)

    def get_allPage(self ):
        '''
        得到所有页数据
        :param accountId:
        :param page:
        :return:
        '''
        accountId = self.accountId
        flag = True
        page = 1
        while flag:
            if page > 20:
                break
            info = self.get_accountIdPage(accountId ,page)
            flag = self.get_parseAccountIdPage(info)
            page += 1
            # break


        return self.contentId_list











if __name__ == '__main__':
    getAccountPage_obj = getAccountPage(105993661)
    contentId_list = getAccountPage_obj.get_allPage()
    print(contentId_list)
