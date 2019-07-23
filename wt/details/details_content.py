import time
import hashlib
import requests
import re
import json
import pymysql
import string
import random
from urllib import parse



class  details_content:


    wtdr_mixrow_num = 0
    wtdr_polymerization_num = 0
    wtdr_noLink_mixrow_num = 0
    wtdr_noLink_polymerization_num = 0

    num = 1


    def __init__(self,contentId_list):
        self.contentId_list = contentId_list

    def upload(self,data):

        api_url = 'http://172.17.122.112/event/hashtag/resource/add' # prd
        # api_url = 'http://172.18.0.75/event/hashtag/resource/add'     # stag


        api_headers = {
            'Content-Type': 'application/json',
            'Postman-Token': '5922f1d1-cfa9-4ef1-bdfb-829396d70683',
            'cache-control': 'no-cache'
        }

        res = requests.post(url=api_url, data=json.dumps(
            data), headers=api_headers)

        # print('================= >', res.text)
        return res

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


    def parse_info(self,info):
        content = info.get('data').get('models').get('content')
        tags = info.get('data').get('models').get('tags')
        if tags == None:
            tags = []
        else:
            tags = [tag.get('name') for tag in tags]
        drawerList = content.get('drawerList')
        richText = content.get('richText')
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

        # 无商品外链内容
        if drawerList == [] or drawerList == None:
            # 聚合内容
            if richText == [] or richText == None:
                resourceContent = content.get('summary')
                resourcePlatform = 'wt$polymerization'
                self.wtdr_noLink_polymerization_num += 1
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
                self.wtdr_noLink_mixrow_num += 1



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
                self.wtdr_polymerization_num += 1
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
                self.wtdr_mixrow_num += 1

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

        return  data

    def stringRandom(self,n):
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, n))
        return ran_str

    def get_detailsSign(self,contentId):
        '''
        根据contentId生成sign
        调用请求、解析
        :param contentId:
        :return:
        '''
        cookie = "t=ce9c2d81840f516b90065693d3c1bced;cna=VaGnFRJC5HQCAXPBLh6Y0/1c;cookie2=1c25f6cda62c32ef779da13460131a0f;_tb_token_=5bd1458e33506;munb=2204107709941;WAPFDFDTGFG=+4cMKKP+8PI+KK8Wni0Vgjhqw0RFAA==;_w_app_lg=0;thw=cn;tg=0;hng=CN|zh-cn|CNY;v=0;existShop=MTU2Mjg0NzM1OQ==;tracknick=tb891903328;lgc=tb891903328;dnk=tb891903328;mt=ci=0_1;_m_h5_tk=a8e73dd2bea9653e0fab791cf9c8206c_1562907734678;_m_h5_tk_enc=37cea89dd28fd4ad745193172e5cd9b2;ockeqeudmj=v3iR+tc=;unb=2204107709941;sg=810;_l_g_=Ug==;skt=0a0ee123ba345df4;uc1=cookie16=V32FPkk/xXMk5UvIbNtImtMfJQ==&cookie21=WqG3DMC9Eman&cookie15=V32FPkk/w0dUvg==&existShop=false&pas=0&cookie14=UoTaGqVgiSa58Q==&tag=8&lng=zh_CN;cookie1=BxVWjsb3y3W4pMwjttpdqB8Ohc1mlPpUCgSSARFgsR4=;csg=465d32d8;uc3=vt3=F8dBy3/8YGZEwvNNtn0=&id2=UUphzpYoK748IBvz2A==&nk2=F5RNbBmXSVJe3I0=&lg2=UtASsssmOIJ0bQ==;_cc_=U+GCWk/7og==;_nk_=tb891903328;cookie17=UUphzpYoK748IBvz2A==;ntm=1;l=cBTCZm3lqa8EKJcLBOCi5uIRZf7TSIRAguPRw4mvi_5IL6Ls0gbOk0AZfFp6cjWd92TB4J_NPtw9-etfs7SDmghzaiUc.;isg=BMzMmjW9_TjPPenE_hdrV1pqnSw-rbjYUk4mDSaN1HcasWy7ThcePyJLUfks-agH"
        tk = re.search('_m_h5_tk=(.*?);', cookie, re.S).group(1).split('_')[0]
        data = '{"contentId":"' + str(contentId) + r'","source":"darenhome","type":"h5","params":"{\"sourcePageName\":\"darenhome\"}","business_spm":"a2114l.11283723","track_params":""}'
        t = int(time.time() * 1000)
        strs = tk + "&" + str(t) + "&" + "12574478" + "&" + data
        details_sign = hashlib.md5(strs.encode(encoding='utf8')).hexdigest()
        # print(details_sign)

        return  details_sign


    def get_pageInfo(self,contentId):
        utdid = self.stringRandom(24)
        v = '1.0'
        api = "mtop.taobao.beehive.detail.contentservicenewv2"
        # api='mtop.mediaplatform.live.searchv2'
        # api='mtop.tmall.search.searchproduct'
        # api = 'taobao.wireless.share.tpwd.query'

        data = {"contentId": str(contentId), "source": "darenhome", "type": "h5",
                "params": "{\"sourcePageName\":\"darenhome\"}", "business_spm": "", "track_params": ""}
        headers = {
            'x-appkey': '21646297',
            'x-t': str(time.time())[:10],
            'x-pv': '6.1',
            'x-sign': self.get_detailsSign(contentId),
            'x-features': '27',
            'x-location': "119.99023%2C30.275328",
            'x-ttid': '10005934@taobao_android_8.7.0',
            'x-utdid': utdid,
            'x-devid': 'Q8rmBiZW4hbKClMaYgGo0vnNkTXVc3AELqO9d7xp61sH',
            'x-uid': ''
        }
        result = requests.get(
            'https://api.m.taobao.com/gw/' + api + '/' + v + '/?data=' + parse.quote(json.dumps(data)), headers=headers)
        # print(result.json())
        info = self.parse_info(result.json())
        return info



    def main(self):
        for contentInfo_dict in self.contentId_list:
            contentId =  contentInfo_dict.get('contentId')
            try:
                data = self.get_pageInfo(contentId)
                image = ['http:' + image_url for image_url in contentInfo_dict.get('image')]
            except:
                continue
            if data != None:
                data.get('resources')[0].get('resourceInfo')['image'] = image
                data.get('resources')[0]['praiseCount'] = contentInfo_dict.get('feedCount').get('praiseCount')
                data.get('resources')[0]['viewCount'] = contentInfo_dict.get('feedCount').get('viewCount')
                res = self.upload(data)
                print('-------------- >',self.num)
                print(res.text)
                # print(json.dumps(data))
                print()
                self.num += 1

        # print('wt$polymerization:', self.wtdr_noLink_polymerization_num)
        # print('wt$mixrow:', self.wtdr_noLink_mixrow_num)
        # print('wt#polymerization:', self.wtdr_polymerization_num)
        # print('wt#mixrow:', self.wtdr_mixrow_num)


        return ( self.wtdr_mixrow_num ,self.wtdr_polymerization_num,self.wtdr_noLink_mixrow_num,self.wtdr_noLink_polymerization_num )








if __name__ == '__main__':
    contentId_list = [{  "image": ["//img.alicdn.com/imgextra/i4/2200736526912/O1CN01jUL2FF20vk8sDyBDr_!!2200736526912.jpg", "//img.alicdn.com/imgextra/i3/2200736526912/O1CN01otC6gl20vk8o5reRH_!!2200736526912.jpg", "//img.alicdn.com/imgextra/i4/2200736526912/O1CN01kFeBXW20vk8o5nHhA_!!2200736526912.jpg"], "contentId": 229630290483}]
    temp = details_content(contentId_list)
    print(temp.main())

