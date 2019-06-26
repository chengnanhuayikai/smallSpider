

import requests
import re
import json
from fake_useragent import  UserAgent
import hashlib

ua = UserAgent(path='/Users/songhuan/path/fake_useragent.json')

def upload(data):
    dataList = {
        "dataList": [
            {
                "isUse": 0,
                "data": json.dumps(data)

            }
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        'Postman-Token': '665e9f6b-39f0-4304-b944-5bacbf787a02',
        'cache-control': 'no-cache'
    }

    res = requests.post(url='http://172.17.123.234:8166/service/duoduojinbao/resource/add', headers=headers,
                        data=json.dumps(dataList)).text
    # print(res)
    # print()
    # print(dataList)
    return res



def data_md5(data):
    return hashlib.md5(data.encode()).hexdigest()


def get_info(url):
    headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': ua.random
    }
    response = requests.get(url=url, headers=headers).text
    html = response.replace('\\\\\\','')

    items = re.search(r'window.__INITIAL_STATE__ = JSON.parse\("(.*?)"\);', html,re.S).group(1)
    items = items.replace('\\', '')
    temp = re.search('"content":"(.*)","coverImg"',items,re.S)

    if temp == None:
        print('----------   pass --------------')
        return  None

    # temp = re.search('"content":"(.*)","coverImg"',items,re.S).group(1)
    temp = temp.group(1)
    items = items.replace(temp,'')

    items = json.loads(items)
    resourceContent = json.loads(temp)
    cellType_list = [cell_type.get('cellType') for cell_type in  resourceContent]
    # print(cellType_list)
    if 8 in cellType_list or 9 in cellType_list:
        print('----------   pass --------------')
        return  None
    print(items)
    print(resourceContent)

    resourceTitle = items.get('novelDetail').get('title')

    if resourceTitle == '' or resourceTitle == None:
        print('------- pass -----------')
        return None

    image = items.get('novelDetail').get('coverImg')
    resourceLink = url
    resourcePlatform = '网易考拉'
    resourceId = 'wykl_' + data_md5(resourceTitle)

    goods_info = []
    matchedGoods = items.get('matchedGoods')
    if matchedGoods != []:
        for matched_good in matchedGoods:
            goods_info_dict = {}
            goods_info_dict['goods_name'] = matched_good.get('title')
            goods_info_dict['goods_url'] = 'https://m-goods.kaola.com/product/{}.html'.format(matched_good.get('id'))
            goods_info_dict['goods_price'] = [ matched_good.get('imgUrl') ]
            goods_info.append(goods_info_dict)



    info = {
        "dataType": 1,
        "resources": [
            {

                "resourceId": resourceId,  # 资源唯一ID
                "resourceTitle": resourceTitle,  # 文章标题
                "resourceContent": resourceContent,  # 文章内容

                "resourceLink": resourceLink,  # 文章链接
                "resourcePlatform": resourcePlatform,  # 来源
                "resourceTag": "推广资源",
                "resourceInfo": {
                    # 图片
                    "image": [ image ],
                    # 视频
                    "video": []
                },
                "goods_info": goods_info
            }
        ]
    }

    print(info)
    res = upload(info)
    print(res)
    print()
    return 1


def mian():
    num = 1
    for page_id in range(11402028, 11402128):

        url = 'https://zone.kaola.com/novels/{}.html'.format(page_id)
        try:

            data = get_info(url)
        except:
            continue

        if data != None:
            print('------------------------->', num)
            num += 1
            print()

        # break

    print('--------------- end ------------------')

if __name__ == '__main__':
    get_info('https://zone.kaola.com/novels/11923641.html')
    # main()

# 11405000
# 11410000
# 11415000
