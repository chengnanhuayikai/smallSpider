# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import json
from spiders.wt_spider import  WtSpiderSpider




class WtProjectPipeline(object):
    # def process_item(self, item, spider):
    #     print('-------------------> ')
    #
    #     return item




    def upload(self,data):
        # print('*************')
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


    def process_item(self, item, spider):
        print('-------------------> ')
        res = self.upload(item['data'])
        print(res.text)
        print(item)
        print()
        return item