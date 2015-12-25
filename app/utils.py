# -*- coding: utf-8 -*-
import json
from bson import json_util


def fix_dot_keys(data):
    """
    >>> d = {'1.1': 1, '2': {'2.1': 1}}
    >>> fix_dot_keys(d)
    >>> sorted(d)
    ['1_1', '2']
    >>> sorted(d['2'])
    ['2_1']
    """
    for key in data.keys():
        if type(data[key]) == dict:
            fix_dot_keys(data[key])
        if '.' in key:
            _key = key.replace('.', '_')
            data[_key] = data[key]
            del data[key]


def export_collection(collection, fw, keys=None, query=None):
    if keys is None:
        keys = ['_id']
    if query is None:
        query = {}
    fw.write('[\n')
    is_first = True
    for item in collection.find(query, no_cursor_timeout=True):
        for key in keys:
            del item[key]
        if not is_first:
            fw.write(',\n')
        fw.write(json.dumps(item, ensure_ascii=False, default=json_util.default))
        is_first = False
    fw.write('\n]')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
