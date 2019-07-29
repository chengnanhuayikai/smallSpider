
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
    contentId = ''
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
        print('-------')
        feeds = info.get('data').get('result').get('data')[-1].get('co').get('result').get('data').get('feeds')
        # print(feeds)
        if feeds == []:
            return False
        else:
            for content in feeds:
                if content.get('feedType') == '500' or content.get('feedType') == '504':
                    contentId = content.get('feedId')
                    temp = self.get_tags(contentId)
                    if temp == True:
                        self.contentId = contentId
                        return False

                    return  True

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



    def get_tags(self,contentId):
        '''
        根据contentId得到 tags
        :param contentId:
        :return:
        '''
        utdid = ''.join(random.sample(string.ascii_letters + string.digits, 24))
        v = '1.0'
        api = "mtop.taobao.beehive.detail.contentservicenewv2"
        data = {"contentId": str(contentId), "source": "darenhome", "type": "h5",
                "params": "{\"sourcePageName\":\"darenhome\"}", "business_spm": "", "track_params": ""}
        headers = {
            'x-appkey': '21646297',
            'x-t': str(time.time())[:10],
            'x-pv': '6.1',
            'x-sign': 'bbc699b829e42fca253c96e1480b456c',
            'x-features': '27',
            'x-location': "119.99023%2C30.275328",
            'x-ttid': '10005934@taobao_android_8.7.0',
            'x-utdid': utdid,
            'x-devid': 'Q8rmBiZW4hbKClMaYgGo0vnNkTXVc3AELqO9d7xp61sH',
            'x-uid': ''
        }
        result = requests.get(
            'https://api.m.taobao.com/gw/' + api + '/' + v + '/?data=' + parse.quote(json.dumps(data)), headers=headers)
        # print(result.text)
        tags = result.json().get('data').get('models').get('tags')
        if tags == [] or tags == None:
            return False
        else:
            return True





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
            info = self.get_accountIdPage(accountId ,page)
            flag = self.get_parseAccountIdPage(info)
            print(flag)
            page += 1
            # break


        return self.contentId











if __name__ == '__main__':
    getAccountPage_obj = getAccountPage(105993661)
    contentId = getAccountPage_obj.get_allPage()
    print(contentId)
