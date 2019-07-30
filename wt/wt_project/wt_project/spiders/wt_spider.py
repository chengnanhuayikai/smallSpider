# -*- coding: utf-8 -*-
import scrapy
import hashlib
import json
import time
import requests
import random
import re
import string
from urllib import parse
from wt_project.items import  WtProjectItem


class WtSpiderSpider(scrapy.Spider):

    name = 'wt_spider'
    allowed_domains = ['h5api.m.taobao.com','acs.m.taobao.com','api.m.taobao.com']
    # start_urls = ['http://h5api.m.taobao.com/']
    headers = {}
    # 获取当前时间戳
    t = str(int(time.time() * 1000))
    appKey = '12574478'
    contentId_list = []


    wt_p_1 = 0  # 无外链聚合内容
    wt_w_1 = 0  # 无外链混排内容
    wt_p_2 = 0  # 有外链聚合内容
    wt_w_2 = 0  # 有外链混排内容
    wt_v_1 = 0  # 无外链视频内容
    wt_v_2 = 0  # 有外链视频内容

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

    def get_parseAccountIdPage(self,info):
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
                    content_dict['contentType'] = 'Text'
                    self.contentId_list.append(content_dict)


                if content.get("feedType") == '506':
                    content_dict = {}
                    content_dict['image'] = content.get('images')
                    content_dict['contentId'] = content.get('feedId')
                    content_dict['feedCount'] = content.get('feedCount')
                    content_dict['duration'] = content.get('duration')
                    content_dict['contentType'] = 'Video'
                    # print(content_dict)
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
            self.get_accountIdPage(accountId,page)


        return json.loads(response.text)

    def get_allPage(self,accountId):
        '''
        得到所有页数据
        :param accountId:
        :param page:
        :return:
        '''
        flag = True
        page = 1
        while flag:
            if page > 100:
                break
            info = self.get_accountIdPage(accountId,page)
            flag = self.get_parseAccountIdPage(info)
            page += 1
            # break


    def get_detailsSign(self,contentId):
        '''
        根据contentId生成sign
        调用请求、解析
        :param contentId:
        :return:
        '''
        # cookie = ""
        # tk = re.search('_m_h5_tk=(.*?);', cookie, re.S).group(1).split('_')[0]
        tk = '4205e22472369c77955bcacbc0a5fada'
        data = '{"contentId":"' + str(contentId) + r'","source":"darenhome","type":"h5","params":"{\"sourcePageName\":\"darenhome\"}","business_spm":"a2114l.11283723","track_params":""}'
        t = int(time.time() * 1000)
        strs = tk + "&" + str(t) + "&" + "12574478" + "&" + data
        details_sign = hashlib.md5(strs.encode(encoding='utf8')).hexdigest()
        # print(details_sign)

        return  details_sign


    def get_contentIdUrl(self,contentId,contentType):
        '''
        根据contentId 生成url
        :param contentId:
        :param content_dict:
        :return:
        '''
        data = {"contentId": str(contentId), "source": "darenhome", "type": "h5",
                "params": "{\"sourcePageName\":\"darenhome\"}", "business_spm": "", "track_params": ""}
        utdid = ''.join(random.sample(string.ascii_letters + string.digits, 24))
        headers = {
            'x-appkey': '21646297',
            'x-t': str(time.time())[:10],
            'x-pv': '6.1',
            # 'x-sign': 'bbc699b829e42fca253c96e1480b456c',
            'x-sign':self.get_detailsSign(contentId),
            'x-features': '27',
            'x-location': '119.99023%2C30.275328',
            'x-ttid': '10005934@taobao_android_8.7.0',
            'x-utdid': utdid,
            'x-devid': 'Q8rmBiZW4hbKClMaYgGo0vnNkTXVc3AELqO9d7xp61sH',
            'x-uid': ''
        }

        url = 'https://api.m.taobao.com/gw/mtop.taobao.beehive.detail.contentservicenewv2/1.0/?data=' + parse.quote(
                json.dumps(data))

        return url,headers


    def data_md5(self,data):
        return hashlib.md5(data.encode()).hexdigest()

    def change_resourceContent(self,resourceContent):
        '''
        resourceContent 转  cellType 格式
        :param resourceContent:
        :return:
        '''

        new_resourceContent = []

        for item in resourceContent:
            temp = {}
            cellType = item.get('resource')[0].get('entityType')
            if cellType == 'ResourceText':
                temp['cellType'] = 1
                temp['text'] = item.get('resource')[0].get('text')
                new_resourceContent.append(temp)
            if cellType == 'ResourcePic':
                temp['cellType'] = 2
                temp['imageUrl'] = 'http:' + item.get('resource')[0].get('picture').get('picUrl')
                new_resourceContent.append(temp)
            if cellType == 'ResourceItem':
                temp['cellType'] = 3
                temp['goods_name'] = item.get('resource')[0].get('item').get('itemTitle')
                temp['goods_url'] = 'http:' + item.get('resource')[0].get('item').get('itemUrl')
                if item.get('resource')[0].get('item').get('item_pic') == None:
                    temp['goods_pic'] = ''
                else:
                    temp['goods_pic'] = 'http:' + item.get('resource')[0].get('item').get('item_pic')

                temp['goods_id'] = item.get('resource')[0].get('item').get('itemId')
                if  item.get('resource')[0].get('item').get('itemPriceDTO') == None :
                    temp['goods_price'] = ''
                else:
                    temp['goods_price'] = item.get('resource')[0].get('item').get('itemPriceDTO').get('price').get(
                        'item_current_price')
                new_resourceContent.append(temp)

        # for temp in new_resourceContent:
        #     print(temp)

        return new_resourceContent


    def start_requests(self):
        '''
        读取 accountId
        :return:
        '''
        f = open('/Users/songhuan/project/红桃k内容/微淘达人/new_details_content/wt_project/wt_project/spiders/accountId.txt','r')
        lines = f.readlines()
        f.close()

        for line in lines:
            accountId = line.strip()
            self.get_allPage(accountId)

        for content_dict in self.contentId_list :

            if content_dict.get('contentType') == 'Text':
                url,headers = self.get_contentIdUrl(content_dict.get('contentId'),'Text')
            if content_dict.get('contentType') == 'Video':
                url, headers = self.get_contentIdUrl(content_dict.get('contentId'), 'Video')
            yield scrapy.Request(url=url, meta={'content_dict': content_dict}, callback=self.parse_deatilsInfo,
                                 headers=headers)

            # break



    def parse_deatilsInfo(self, response):
        '''
        解析 and 清洗
        :param response:
        :return:
        '''
        contentInfo_dict = response.request.meta.get('content_dict')
        info = json.loads(response.text)
        content = info.get('data').get('models').get('content')
        tags = info.get('data').get('models').get('tags')
        if tags == None:
            tags = []
        else:
            tags = [tag.get('name') for tag in tags]

        drawerList = content.get('drawerList')
        gmtCreate = content.get('gmtCreate')
        resourceTitle = content.get('title')
        resourceLink = content.get('detailUrl')
        resourceTag = '微淘内容'
        resourceId = 'wtlm_' + self.data_md5(resourceTitle)
        goods_info_list = []
        account = info.get('data').get('models').get('account')
        accountTag = account.get('accountTag')
        if accountTag == None:
            userTag = ''
        else:
            userTag = accountTag[0].get('tagName')

        userPic = account.get('accountPic').get('picUrl')
        if 'http:' not in userPic:
            userPic = 'http:' + userPic

        userInfo = {
            "userName": account.get('name'),  # 名字
            "userTag": userTag,  # 标签
            "userDesc": account.get('accountDesc'),  # 描述
            "userFans": account.get('fansCount'),  # 粉丝
            "userPic": userPic
        }


        # 解析图文内容
        if contentInfo_dict.get('contentType') == 'Text':
            richText = content.get('richText')
            # 无商品外链内容
            if drawerList == [] or drawerList == None:
                # 聚合内容
                if richText == [] or richText == None:
                    resourceContent = content.get('summary')
                    resourcePlatform = 'wt$polymerization'

                    self.wt_p_1 += 1

                # 混排内容
                else:
                    summary = content.get('summary')
                    summary_temp = {
                        'resource': [
                            {
                                'entityType': 'ResourceText',
                                'text': summary
                            }
                        ]
                    }

                    richText.insert(0, summary_temp)
                    resourceContent = self.change_resourceContent(richText)
                    resourcePlatform = 'wt$mixrow'

                    self.wt_w_1 += 1




            # 有商品外链内容
            else:
                for temp in drawerList:
                    goods_info_dict = {}
                    goods_info_dict['goods_name'] = temp.get('itemTitle')
                    goods_info_dict['goods_url'] = 'http:' + temp.get('itemUrl')
                    if temp.get('item_pic') == None:
                        goods_info_dict['goods_pic'] = ''
                    else:
                        goods_info_dict['goods_pic'] = 'http:' + temp.get('item_pic')

                    if temp.get('itemPriceDTO') == None:
                        goods_info_dict['goods_price'] = ''
                    else:
                        goods_info_dict['goods_price'] = temp.get('itemPriceDTO').get('price').get('item_current_price')
                    goods_info_dict['goods_id'] = temp.get('itemId')
                    goods_info_list.append(goods_info_dict)
                # 聚合内容
                if richText == [] or richText == None:
                    resourceContent = content.get('summary')
                    resourcePlatform = 'wt#polymerization'

                    self.wt_p_2 += 1

                else:
                    summary = content.get("summary")
                    summary_temp = {
                        "resource": [
                            {
                                "entityType": "ResourceText",
                                "text": summary
                            }
                        ]
                    }

                    richText.insert(0, summary_temp)
                    resourceContent = self.change_resourceContent(richText)
                    resourcePlatform = 'wt#mixrow'

                    self.wt_w_2 += 1


            data = {
                    "dataType": 1,
                    "resources": [
                        {

                            "resourceId": resourceId,  # 资源唯一ID
                            "resourceTitle": resourceTitle,  # 文章标题
                            "resourceContent": resourceContent,  # 文章内容
                            "userInfo": userInfo,
                            "gmtCreate": gmtCreate,
                            "tags": tags,
                            "resourceLink": resourceLink,  # 文章链接
                            "resourcePlatform": resourcePlatform,  # 来源
                            "resourceTag": resourceTag,
                            "resourceInfo": {
                                # 图片
                                "image": '',
                                # 视频
                                "video": []
                            },
                            "goods_info": goods_info_list
                        }
                    ]
                }


            image = ['http:' + image_url for image_url in contentInfo_dict.get('image')]
            data.get('resources')[0].get('resourceInfo')['image'] = image
            data.get('resources')[0]['praiseCount'] = contentInfo_dict.get('feedCount').get('praiseCount')
            data.get('resources')[0]['viewCount'] = contentInfo_dict.get('feedCount').get('viewCount')

            # print(json.dumps(data))
            item = WtProjectItem()
            item['data'] = data

            yield  item


        # 解析视频内容
        if contentInfo_dict.get('contentType') == 'Video':
            resourceContent = content.get('summary')
            videoUrl = content.get('video').get('videoUrl')
            videoInfo = {
                "videoHeight": content.get('video').get('height'),
                "videoWidth": content.get('video').get('width'),
                "videoUrl": videoUrl
            }
            if drawerList == [] or drawerList == None:
                resourcePlatform = 'wt$video'
                self.wt_v_1 += 1
            else:
                for temp in drawerList:
                    goods_info_dict = {}
                    goods_info_dict['goods_name'] = temp.get('itemTitle')
                    goods_info_dict['goods_url'] = 'http:' + temp.get('itemUrl')
                    if temp.get('item_pic') == None:
                        goods_info_dict['goods_pic'] = ''
                    else:
                        goods_info_dict['goods_pic'] = 'http:' + temp.get('item_pic')

                    if temp.get('itemPriceDTO') == None:
                        goods_info_dict['goods_price'] = ''
                    else:
                        goods_info_dict['goods_price'] = temp.get('itemPriceDTO').get('price').get('item_current_price')
                    goods_info_dict['goods_id'] = temp.get('itemId')
                    goods_info_list.append(goods_info_dict)
                resourcePlatform = 'wt#video'
                self.wt_v_2 += 1

            data = {
                "dataType": 1,
                "resources": [
                    {

                        "resourceId": resourceId,  # 资源唯一ID
                        "resourceTitle": resourceTitle,  # 文章标题
                        "resourceContent": resourceContent,  # 文章内容
                        "userInfo": userInfo,
                        "gmtCreate": gmtCreate,
                        "tags": tags,
                        "resourceLink": resourceLink,  # 文章链接
                        "resourcePlatform": resourcePlatform,  # 来源
                        "resourceTag": resourceTag,
                        "videoInfo": videoInfo,
                        "resourceInfo": {
                            # 图片
                            "image": '',
                            # 视频
                            "video": [videoUrl]
                        },
                        "goods_info": goods_info_list
                    }
                ]
            }

            data.get('resources')[0].get('resourceInfo')['image'] = image = ['http:' + image_url for image_url in contentInfo_dict.get('image')]
            data.get('resources')[0]['commentCount'] = contentInfo_dict.get('feedCount').get('commentCount')
            data.get('resources')[0]['praiseCount'] = contentInfo_dict.get('feedCount').get('praiseCount')
            data.get('resources')[0]['viewCount'] = contentInfo_dict.get('feedCount').get('viewCount')
            data.get('resources')[0]['duration'] = contentInfo_dict.get('duration')

            item = WtProjectItem()
            item['data'] = data
            item['num'] = {'wt_p_1':self.wt_p_1,'wt_w_1':self.wt_w_1,'wt_p_2':self.wt_p_2,'wt_w_2':self.wt_w_2,'wt_v_1':self.wt_v_1,'wt_v_2':self.wt_v_2}

            yield item




