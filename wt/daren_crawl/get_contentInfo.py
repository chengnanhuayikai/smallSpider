
import time
import hashlib
import requests
import re
import random
import json
import string
from urllib import parse
from itemDetails import get_rootCategoryId
from collections import Counter



class get_contentId:
    contentId_list = []
    headers  = {}
    t = str(int(time.time() * 1000))
    appKey = '12574478'

    def __init__(self,accountId_dict):
        self.accountId_dict = accountId_dict


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

    def get_drawerList(self,contentId):
        '''
        contentID page 数据
        :param contentId:
        :return:
        '''

        data = {"contentId": str(contentId), "source": "darenhome", "type": "h5",
                "params": "{\"sourcePageName\":\"darenhome\"}", "business_spm": "", "track_params": ""}
        utdid = ''.join(random.sample(string.ascii_letters + string.digits, 24))
        headers = {
            'x-appkey': '21646297',
            'x-t': str(time.time())[:10],
            'x-pv': '6.1',
            'x-sign': 'bbc699b829e42fca253c96e1480b456c',
            'x-features': '27',
            'x-location': '119.99023%2C30.275328',
            'x-ttid': '10005934@taobao_android_8.7.0',
            'x-utdid': utdid,
            'x-devid': 'Q8rmBiZW4hbKClMaYgGo0vnNkTXVc3AELqO9d7xp61sH',
            'x-uid': 'Q8rmBiZW4hbKClMaYgGo0vnNkTXVc3AELqO9d7xp61sH'
        }
        result = requests.get(
            'https://api.m.taobao.com/gw/mtop.taobao.beehive.detail.contentservicenewv2/1.0/?data=' + parse.quote(
                json.dumps(data)), headers=headers)

        drawerList = result.json().get('data').get('models').get('content').get('drawerList')
        return drawerList



    def parse_accountIdPage(self,info):
        '''
        解析内容
        :param info:
        :return:
        '''
        # print(json.dumps(info))
        # 粉丝
        fans = info.get('data').get('result').get('data')[2].get('co').get('result').get('data').get('fans')
        # 粉丝数单位
        unit = info.get('data').get('result').get('data')[2].get('co').get('result').get('data').get('unit')

        if unit != None:
            fans = fans + unit




        if '万' in fans:
            # print(''.join(re.findall(r'\d+', fans)) + '0000')
            fans = ''.join(re.findall(r'\d+', fans)) + '0000'



        if int(fans) < 1000 :
            return None




        # 认证标题
        title = info.get('data').get('result').get('data')[2].get('co').get('result').get('data').get('title')

        # 类型
        typeName = info.get('data').get('result').get('data')[2].get('co').get('result').get('data').get('typeName')

        # 描述
        desc = info.get('data').get('result').get('data')[2].get('co').get('result').get('data').get('desc')

        unit = ''   if unit == None else unit
        title = '' if title == None else title
        typeName = '' if typeName == None else typeName
        desc = '' if desc == None else desc

        feeds =  info.get('data').get('result').get('data')[-1].get('co').get('result').get('data').get('feeds')
        items = []
        for temp in feeds:
                if temp.get('items') != None:
                    for item in temp.get('items'):
                        items.append(item.get('itemId'))


        if items == [] and feeds != []:
            contentId = feeds[0].get('feedId')
            drawerList = self.get_drawerList(contentId)
            if drawerList != [] and drawerList != None:
                for temp in drawerList:
                    items.append(temp.get('itemId'))



        try:
            publishTime = info.get('data').get('result').get('data')[-1].get('co').get('result').get('data').get('feeds')[0].get('publishTime')
            ti = str(publishTime)[:-3]
            publishTime = time.strftime('%Y--%m--%d %H:%M:%S', time.localtime(int(ti)))
        except:
            publishTime = ''

        if len(items) > 5:
            items = items[:5]

        # print(items)
        return (fans,publishTime,title,typeName,desc,items)


    def get_accountIdPage(self,accountId):
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
            1) + ',"currentModuleIds":"","contentId":"","tabString":"homepage","subTabString":"new_feeds"}'


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
        循环accountId_list
        取出数据
        写入文件
        :return:
        '''


        info = self.get_accountIdPage(self.accountId_dict.get('accountId'))
        try:
            info_tuple = self.parse_accountIdPage(info)
        except Exception as e:
            print(e)
            print(json.dumps(info))
            return None


        if info_tuple == None:
            return  None


        accountId = self.accountId_dict.get('accountId')
        accountName = self.accountId_dict.get('accountName')
        fans = info_tuple[0]
        title = info_tuple[2]
        typeName = info_tuple[3]
        desc = info_tuple[4]
        publishTime = info_tuple[1]

        category_list = []
        for item in info_tuple[5]:
            category = get_rootCategoryId(item)

            category_list.append(category)

        if category_list == []:
            category = ''
        else:
            category_counts = Counter(category_list)
            category = category_counts.most_common(1)[0][0]

        if category == None:
            category = ''

        try:
            userInfo = str(
                accountId) + ',' + accountName + ',' + fans + ',' + publishTime + ',' + title + ',' + typeName + ',' + desc +  ',' +  category + '\n'
            print(userInfo)


            with open('wtDarenId_01.csv', 'a', encoding='Utf8') as f:
                f.write(userInfo)
        except Exception as e:
            print('-----------------> ')
            print(e)













if __name__ == '__main__':
    # 3020335190 2315200564
    accountId_list = {'accountId':41358922,'accountName':'kdjskj'}

    contentId_obj = get_contentId(accountId_list)
    contentId_obj.main()







