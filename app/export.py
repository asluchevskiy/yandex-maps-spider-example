# -*- coding: utf-8 -*-
import json
import pymongo
import string
import urlparse
from utils import export_collection
from settings import *


class Exporter(object):
    def __init__(self):
        self.db = pymongo.MongoClient()[MONGO_DB]
        self.db.result.create_index('yandex_id')

    def _process_item(self, item, query_meta):
        if 'CompanyMetaData' not in item['properties']:
            return
        properties = item['properties']
        yandex_id = properties['CompanyMetaData']['id']
        name = properties['CompanyMetaData']['name']
        urls = properties['CompanyMetaData'].get('urls', [])
        coordinates = item['geometry']['coordinates']
        phones = [ph['formatted'] for ph in properties['CompanyMetaData'].get('Phones', [])]
        address = properties['CompanyMetaData']['AddressDetails']['Country']['AddressLine']
        yandex_address_details = properties['CompanyMetaData']['AddressDetails']
        categories = [c['name'] for c in properties['CompanyMetaData']['Categories']]
        hours = properties['CompanyMetaData'].get('Hours', {}).get('text')
        br = properties.get('BusinessRating', {})
        score = br.get('score')
        meta = {
            'reviews_count': br.get('reviews', 0),
            'source': 'yandex'
        }
        result = dict(yandex_id=yandex_id, name=name, urls=urls, coordinates=coordinates, phones=phones,
                   address=address, yandex_address_details=yandex_address_details, categories=categories,
                   hours=hours, score=score, _meta=meta, _query_meta=[query_meta])
        if not self.db.result.find_one({'yandex_id': yandex_id}, {'yandex_id': 1}):
            self.db.result.save(result)
        else:
            self.db.result.update({'yandex_id': yandex_id}, {'$push': {'_query_meta': query_meta}})

    def _process_data(self):
        for data in self.db.search_result.find({}, no_cursor_timeout=True):
            for item in data['data']['features']:
                # data fix:
                for key in ('city_id', 'category_id'):
                    data['_meta'][key] = int(data['_meta'][key])
                self._process_item(item, data['_meta'])
                
    def export_json(self):
        with open(RESULT_FILE, 'w') as fw:
            export_collection(self.db.result, fw)

    def run(self):
        self._process_data()
