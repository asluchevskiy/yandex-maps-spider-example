# -*- coding: utf-8 -*-
import pymongo
import csv
import re
import json
from grab.spider import Spider, Task
from settings import *
from urllib import quote
from utils import fix_dot_keys


class YandexMapsSpider(Spider):
    initial_urls = ['https://maps.yandex.ru']

    def prepare(self):
        self.db = pymongo.MongoClient()[MONGO_DB]
        self.db.search_result.create_index([('_meta.category_id', pymongo.ASCENDING),
                                            ('_meta.city_id', pymongo.ASCENDING)])

    # def update_grab_instance(self, grab):
    #     grab.setup(log_dir='./logs', debug=True)

    def task_initial(self, grab, task):
        self._crsf_token = re.search('csrfToken\":\"(.+?)\"', grab.response.body).group(1)
        self._grab = grab
        self.task_generator_object = self._task_generator()
        self.task_generator_enabled = True

    def _task_generator(self):
        with open(TASK_FILE) as f:
            reader = csv.reader(f, delimiter=';')
            for line in reader:
                if len(line) != 3:
                    continue
                category_id, city_id, query = line
                if self.db.search_result.find_one({'_meta.category_id': category_id, '_meta.city_id': city_id},
                                                  {'_meta': 1}):
                    continue
                url = r'https://maps.yandex.ru/api/search?text=' + quote(query) + \
                      r'&chain=&lang=ru_RU&origin=maps-form&results=1000&snippets=' + \
                      r'business%2F1.x%2Cmasstransit%2F1.x%2Cpanoramas%2F1.x%2Cbusinessrating' + \
                      r'%2F2.x%2Cphotos%2F1.x%2Cbusinessreviews%2F1.x&' + \
                      r'ask_direct=0&csrfToken=' + self._crsf_token
                grab = self._grab.clone(url=url)
                yield Task('search', grab=grab, _meta=dict(category_id=category_id, city_id=city_id, query=query))

    def task_search(self, grab, task):
        data = json.loads(grab.response.body)
        if not len(data['data']['features']):
            return
        fix_dot_keys(data)
        data['_meta'] = task._meta
        self.db.search_result.insert(data)
