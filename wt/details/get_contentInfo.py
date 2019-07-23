
import time
import hashlib
import requests
import re
import json
from urllib import parse
from details_content import details_content


class get_contentId:
    contentId_list = []
    headers  = {}
    t = str(int(time.time() * 1000))
    appKey = '12574478'

    def __init__(self,accountId):
        self.accountId = accountId


    def setHeaders(self,html=None):
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
            # print('秘钥：' + sign)
            # 设置第二次请求的cookie
            headers = {
                'cookie': '_m_h5_tk=' + _m_h5_tk + '; _m_h5_tk_enc=' + _m_h5_tk_enc,
            }

            self.headers = headers

    def hex_md5(self,string):
        '''
        MD5 加密
        :param string:
        :return:
        '''
        m = hashlib.md5()
        m.update(string.encode('UTF-8'))
        return m.hexdigest()

    def parse_accountIdPage(self,info):
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
                    content_dict = {}
                    content_dict['image'] = content.get('images')
                    content_dict['contentId'] = content.get('feedId')
                    content_dict['feedCount'] = content.get('feedCount')
                    self.contentId_list.append(content_dict)



            return True


    def get_accountIdPage(self,accountId,page):
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
            self.parse_accountIdPage(accountId,page)


        return json.loads(response.text)



    def main(self):
        '''
        取所有的page数
        :return:
        '''


        flag = True
        page = 1
        while flag:
            # print(page)
            print(page)
            if page > 300 :
                break
            info = self.get_accountIdPage(self.accountId,page)
            flag = self.parse_accountIdPage(info)
            page += 1



        temp = details_content(self.contentId_list)
        num_tuple = temp.main()
        return num_tuple









if __name__ == '__main__':
    # 3020335190 2315200564
    contentId_obj = get_contentId(2223976488)
    contentId_obj.main()

    # number = contentId_obj.main()
    # print(number)



