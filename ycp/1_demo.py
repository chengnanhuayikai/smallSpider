

# 详情url
# https://www.wehaowu.com/api/java/cms/show/content/v1.2.0
# https://www.wehaowu.com/api/java/cms/show/content/v1.2.0

# {"token":"Cf0Illlv-aQUYTHqkLix2Zzd7NA8Na8woOCQgjUYX6pM_LL3xTRp9H2PUofzgsapj8kuQNTvX-177zlmC_LGh7xilGwmnbQdbpxzpdwXSoPzPLMYh-3cbIdkbqBP_iHnJvCksC3Plr5qkvXtx00SG_hidncGABNS9GzrUqi9yOE=","app_scope":"ycp","platform":"mp","version":"1.4.0","content_id":"15602516829778232"}
# {"token":"Cf0Illlv-aQUYTHqkLix2Zzd7NA8Na8woOCQgjUYX6pM_LL3xTRp9H2PUofzgsapj8kuQNTvX-177zlmC_LGh7xilGwmnbQdbpxzpdwXSoPzPLMYh-3cbIdkbqBP_iHnJvCksC3Plr5qkvXtx00SG_hidncGABNS9GzrUqi9yOE=","app_scope":"ycp","platform":"mp","version":"1.4.0","content_id":"15597343151639824"}
# 图文
# {"token":"iBcjPaEWChzTnYRbaYqMHO0vYVAJlZT7A1e3awPrMHgLCRZ2GsfMtUqVgfuvjJ6PVN11T4osyvLd6fd2B4Xsk7uinRucGM1gFGT38nWvvniWa3iq29cTCe7klT9HwBSUeu2-ecE8vXGLmBUqOt4kWRERpfvyBFeYfpBnq4_RuwI=","app_scope":"ycp","platform":"mp","version":"1.4.0","content_id":"15605711315344813"}


#  瀑布url
# {"token":"Cf0Illlv-aQUYTHqkLix2Zzd7NA8Na8woOCQgjUYX6pM_LL3xTRp9H2PUofzgsapj8kuQNTvX-177zlmC_LGh7xilGwmnbQdbpxzpdwXSoPzPLMYh-3cbIdkbqBP_iHnJvCksC3Plr5qkvXtx00SG_hidncGABNS9GzrUqi9yOE=","app_scope":"ycp","platform":"mp","version":"1.4.0","page":0,"page_size":8,"offset":3}
# {"token":"Cf0Illlv-aQUYTHqkLix2Zzd7NA8Na8woOCQgjUYX6pM_LL3xTRp9H2PUofzgsapj8kuQNTvX-177zlmC_LGh7xilGwmnbQdbpxzpdwXSoPzPLMYh-3cbIdkbqBP_iHnJvCksC3Plr5qkvXtx00SG_hidncGABNS9GzrUqi9yOE=","app_scope":"ycp","platform":"mp","version":"1.4.0","page":0,"page_size":8,"offset":4}


import  requests
import json
import hashlib

content_id_list = []

image_text_num = 1
video_num = 1


headers = {"Host": "www.wehaowu.com",
           "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12F70 MicroMessenger/6.7.4(0x1607042c) NetType/WIFI Language/zh_CN",
           "Referer": "https://servicewechat.com/wx97fb0f2ee9b2413e/28/page-frame.html",
           "Content-Type": "application/json"
           }

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

def get_pageInfo(offset):
    page_url = 'https://www.wehaowu.com/api/java/cms/homepage/list/content/v1.4.1'
    data = {"token":"Cf0Illlv-aQUYTHqkLix2Zzd7NA8Na8woOCQgjUYX6pM_LL3xTRp9H2PUofzgsapj8kuQNTvX-177zlmC_LGh7xilGwmnbQdbpxzpdwXSoPzPLMYh-3cbIdkbqBP_iHnJvCksC3Plr5qkvXtx00SG_hidncGABNS9GzrUqi9yOE=",
            "app_scope":"ycp",
            "platform":"mp",
            "version":"1.4.0",
            "page":0,
            "page_size":8,
            "offset":offset}

    res = requests.post(url=page_url,headers=headers,data=json.dumps(data))
    # print(res.text)
    return  json.loads(res.text)

def parse_pageInfo(data):
    for item in data.get('data').get('home_page_contents'):
        content_id_list.append(item.get('content_id'))
    # print(content_id_list)



def get_contentInfo(content_id):
    content_url = 'https://www.wehaowu.com/api/java/cms/show/content/v1.2.0'
    data = {
        "token":"Cf0Illlv-aQUYTHqkLix2Zzd7NA8Na8woOCQgjUYX6pM_LL3xTRp9H2PUofzgsapj8kuQNTvX-177zlmC_LGh7xilGwmnbQdbpxzpdwXSoPzPLMYh-3cbIdkbqBP_iHnJvCksC3Plr5qkvXtx00SG_hidncGABNS9GzrUqi9yOE=",
        "app_scope":"ycp",
        "platform":"mp",
        "version":"1.4.0",
        "content_id":content_id
    }
    res = requests.post(url=content_url,headers=headers,data=json.dumps(data))
    # print(res.text)
    content_info = json.loads(res.text).get('data').get('content')
    # 视频内容
    if content_info.get('content_type') ==  "VDO":
        resourceTitle = content_info.get('title')
        resourcePlatform = 'ycp#video'
        resourceId = 'ycp_' +  data_md5(resourceTitle)
        video_url = json.loads(content_info.get('content')).get('video_url')
        goods_dict = {}
        goods_dict['goods_name'] = content_info.get('linked_series')[0].get('series_name')
        goods_dict['goods_price'] = [ content_info.get('linked_series')[0].get('first_pic') ]
        # print(goods_dict['goods_name'])

        info = {
            "dataType": 1,
            "resources": [
                {

                    "resourceId": resourceId,  # 资源唯一ID
                    "resourceTitle": resourceTitle,  # 文章标题
                    "resourcePlatform": resourcePlatform,  # 来源
                    "resourceTag": "推广资源",
                    "resourceInfo": {
                        # 图片
                        "image": [],
                        # 视频
                        "video": [ video_url ]
                    },
                    "goods_info": [
                        goods_dict
                    ]
                }
            ]
        }


        print(info)
        res = upload(info)
        print(res)
        return 1

    # 图文混排内容
    if content_info.get('content_type') == "IMG":
        resourceTitle = content_info.get('title')
        resourcePlatform = 'ycp#mixrow'
        resourceId = 'ycp_' +  data_md5(resourceTitle)
        resourceContent = json.loads(content_info.get('content')).get('ops')
        # print(resourceContent)
        # for  item in resourceContent:
        #     print(item)
        image = content_info.get('first_pic')
        goods_dict = {}
        goods_dict['goods_name'] = content_info.get('linked_series')[0].get('series_name')
        goods_dict['goods_price'] = [ content_info.get('linked_series')[0].get('first_pic') ]

        info = {
            "dataType": 1,
            "resources": [
                {

                    "resourceId": resourceId,  # 资源唯一ID
                    "resourceTitle": resourceTitle,  # 文章标题
                    "resourceContent":resourceContent, # 图文混排数组
                    "resourcePlatform": resourcePlatform,  # 来源
                    "resourceTag": "推广资源",
                    "resourceInfo": {
                        # 图片
                        "image": [image],
                        # 视频
                        "video": [ ]
                    },
                    "goods_info": [
                        goods_dict
                    ]
                }
            ]
        }

        print(info)
        res = upload(info)
        print(res)
        return 2




def main():
    global  image_text_num
    global  video_num
    for offset in range(1,21):
        data = get_pageInfo(offset)
        parse_pageInfo(data)
    for id in content_id_list :
        num = get_contentInfo(id)
        if num == 1:
            print('---------- >>> video_num:', video_num)
            video_num += 1
            print()
        if num == 2:
            print('---------- >>> image_text_num:', image_text_num)
            image_text_num += 1
            print()







if __name__ == "__main__":
    # data = get_pageInfo(1)
    # parse_pageInfo(data)
    # for id in ['15602516829778232', '15487615509035427', '15451995143072066', '15451997944805642', '15600965315474419', '15525417041888503', '15541966555930281', '15451990479642824']:
    #
    #     get_contentInfo(id)

    # get_contentInfo(15605711315344813)
    main()