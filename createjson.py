import elasticsearch
import os
import json
import pprint
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf8')
es = elasticsearch.Elasticsearch()

def make_json():
    with open('datamap.json') as input_file:
        linkmap = json.loads(input_file.read().decode("utf-8"))

    for base, subdirs, files in os.walk('./pdfs/fetched'):
        for name in files:
            if name.endswith('.txt'):
                name_split = name.split('_')
                body = dict()
                body['date'] = name_split[0]
                body['tag'] = name_split[1]
                key = name.split('.')[0][:-4]+ '.pdf'
                body['link'] = linkmap[key]
                body['group'] = 'city-council'
                page_str = name_split[2].split('.')[0]
                body['page_num'] = int(page_str)
                # with open(os.path.join(base, name), 'r') as fp:
                file_name = os.path.join(base, name)
                with codecs.open(file_name, "r",encoding='utf-8', errors='ignore') as fp:
                    body['text'] = str(fp.read()).encode('utf-8').strip()
                jsonbody = json.dumps(body)
                es.index(index='notes', doc_type='page', id=name, body = jsonbody)

if __name__ == '__main__':
    make_json()
