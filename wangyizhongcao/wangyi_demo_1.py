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
    # print(response)
    title = re.search('<title>(.*?)</title>',response,re.S).group(1)
    if '心得详情' in title:
        print('------- pass -----------')
        return None

    items = re.search(r'JSON.parse\("(.*)"\)', response).group(1)
    items = items.replace(r'\n', '')
    items = items.replace('\\', '')
    # print(info)
    items = json.loads(items)
    resourceTitle = items.get('ideaDetail').get('title')

    if resourceTitle == '' or resourceTitle == None:
        print('------- pass -----------')
        return None

    matchedGoods = items.get('matchedGoods')
    relatedGoods = items.get('relatedGoods')


    if matchedGoods == [] and relatedGoods == []:
        return None

    image = items.get('ideaDetail').get('imgList')
    resourceContent = re.search(r'."desc.":."(.*?)."', response).group(1)
    resourceContent = resourceContent.replace('\\\\n', '\n')
    resourceLink = url
    resourcePlatform = '网易考拉'
    resourceId = 'wykl_' + data_md5(resourceTitle)





    goods_info = []
    goods_name_list = []

    if matchedGoods != []:
        for matched_good in matchedGoods:
            goods_info_dict = {}
            goods_info_dict['goods_name'] = matched_good.get('title')
            goods_info_dict['goods_url'] = 'https://m-goods.kaola.com/product/{}.html'.format(matched_good.get('id'))
            goods_info_dict['goods_price'] = [ matched_good.get('imgUrl') ]
            if goods_info_dict['goods_name'] not in goods_name_list:
                goods_name_list.append(goods_info_dict['goods_name'])
                goods_info.append(goods_info_dict)

    if relatedGoods != []:
        for related_good in relatedGoods:
            goods_info_dict = {}
            goods_info_dict['goods_name'] = related_good.get('title')
            goods_info_dict['goods_url'] = 'https://m-goods.kaola.com/product/{}.html'.format(related_good.get('id'))
            goods_info_dict['goods_price'] = [ related_good.get('imgUrl') ]
            if goods_info_dict['goods_name'] not in goods_name_list:
                goods_name_list.append(goods_info_dict['goods_name'])
                goods_info.append(goods_info_dict)

    #
    # print(relatedGoods)
    # print(matchedGoods)
    # print(image)



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
                    "image": image,
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



def main():
    num = 1
    for page_id in range(11402028, 11402128):

        url = 'https://zone.kaola.com/idea/{}.html'.format(page_id)
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
    # get_info('https://zone.kaola.com/idea/11900146.html') # 11900146  11900143
    main()

