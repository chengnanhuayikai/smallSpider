#encoding=utf8
import json
import random
import string
import time
import requests
import re
from urllib import parse
from get_contentInfo import get_contentId
from pybloom_live import ScalableBloomFilter

sdf = ScalableBloomFilter(initial_capacity=100, error_rate=0.001,
                          mode=ScalableBloomFilter.LARGE_SET_GROWTH)





accountInfo_list = []
contentId_list = []


def stringRandom(n):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, n))
    return ran_str



def pare_tagData(data):
    '''
    解析数据
    :param data:
    :return:
    '''
    if data.get('data') == {}:
        return
    modules = data.get('data').get('modules')
    for temp in modules:
        # print(temp)
        accountInfo_dict = {}
        post = temp.get('data').get('post')
        if post != None:
            accountId = post.get('accountId')
            contentId = post.get('contentId')
            accountInfo_dict['accountId'] = post.get('accountId')
            accountInfo_dict['accountName'] = post.get('accountName')
            if accountId not in sdf:
                contentId_list.append(contentId)


        video = temp.get('data').get('video')
        if video != None:
            accountInfo_dict['accountId'] = video.get('accountId')
            accountInfo_dict['accountName'] = video.get('accountName')

        if accountInfo_dict.get('accountId') not in sdf:
            # print(accountInfo_dict)
            # print()
            accountInfo_list.append(accountInfo_dict)
            sdf.add(accountInfo_dict.get('accountId'))


def get_tags(contentId):
    '''
    根据contentId得到 tags
    :param contentId:
    :return:
    '''
    utdid = stringRandom(24)
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
    return tags


def parse_tags(tags):
    '''
    解析tags
    :param tags:
    :return:
    '''



    if tags == [] or tags == None:
        return  None
    else:
        for tag in tags:
            tag_link = tag.get('link')
            tag_num = re.search('&tag=(.*?)&',tag_link,re.S).group(1)
            tag_contentId = re.search('&contentId=(.*?)&',tag_link,re.S).group(1)
            get_tagPage(tag_contentId,tag_num)




def get_tagPage(contentId,tag_num):
    '''
    取tag页面下所有的page
    :param contentId:
    :param tag_num:
    :return:
    '''
    for toPage in range(1,18):
        t = str(time.time())[:10]
        data = {"contentId":str(contentId),"source":"darenhome","tag":tag_num,"type":"h5","toPage":toPage}
        headers = {
            'x-appkey':'21646297',
            'x-t':t,
            'x-pv':'6.1',
            'x-sign': 'bbc699b829e42fca253c96e1480b456c',
            'x-features': '27',
            'x-location': '119.99023%2C30.275328',
            'x-ttid':'10005934@taobao_android_8.7.0',
            'x-utdid':stringRandom(24),
            'x-devid':'Q8rmBiZW4hbKClMaYgGo0vnNkTXVc3AELqO9d7xp61sH',
            'x-uid':''
        }
        result = requests.get('https://api.m.taobao.com/gw/mtop.taobao.beehive.list.findContentList/1.0/?data='+parse.quote(json.dumps(data)),headers=headers)

        # print(json.dumps(result.json()))
        pare_tagData(result.json())
        # break

if __name__ == '__main__':
    # 根据contentId 得到tags   再取accountId
    # get_tagPage(230014465145)  # 230014465145  231130640992
    # ids = [   200114003706,200114060042,200114096081,200114430910,200114531808,200114615243,200114643142,200116177537,200121395000, 200124226755,200125868186,200130974030,200132697114,200136079822,200136123140,200137472749,200139465639,200140850971,200143332752,200144258360,200144264065,200145758542,200147561048,200154443458,200157418020,200157740087,200159341987,200160031429,200166471761,200179535029,200182149701,200185230195,200186615301,200196583269,200197625560,200200325026,200204262700,200204862751,200206550508,200209373820,200216477763,200218394920,200222598822,200223171265,200229946190 ]

    tags = get_tags(231808262851)
    parse_tags(tags)
    num = 1
    print('len contetnId_list',len(contentId_list))
    for id in contentId_list:

        print(num)
        num += 1
        print()
        tags = get_tags(int(id))
        parse_tags(tags)

    print('len accountInfo_list',len(accountInfo_list))
    for accountInfo_dict in accountInfo_list:
        contentId_obj = get_contentId(accountInfo_dict)
        contentId_obj.main()







