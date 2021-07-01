from elasticsearch import Elasticsearch
from SearchAPI import *
from GenerateDataset import *
from CONFIG import configFile


CONFIG = configFile()
es_client = Elasticsearch([CONFIG['elasticsearchIP']],http_compress=True)


def themedf(index,keyword,start_time,end_time):
    apisearch = APISearch()
    items=[]

    if index == 'news':
        query = (APISearch.search_news(apisearch, search_string=keyword, timestamp_from=start_time, timestamp_to=end_time))
        res = es_client.search(index=index, body=query, size=10000,scroll='2m')
        scroll_id = res['_scroll_id']
        while True:

            if len(res['hits']['hits']) > 0:
                items.extend(res['hits']['hits'])
            else:
                break

            res = es_client.scroll(scroll_id=scroll_id, scroll='2m')
            print("Number of items:", len(items))

        df = GenerateDataset(index)


        dfTicker = GenerateDataset.createDataStructure(df, items)
        dfTicker.drop_duplicates(subset=['title'],inplace=True,ignore_index=True)
        dfTicker = dfTicker.loc[:, ['published_datetime', 'title']]

    elif index == 'tweets':
        query = (APISearch.search_tweets(apisearch, search_string=keyword, timestamp_from=start_time, timestamp_to=end_time))
        res = es_client.search(index=index, body=query, size=10000,scroll='2m')
        scroll_id = res['_scroll_id']
        while True:

            if len(res['hits']['hits']) > 0:
                items.extend(res['hits']['hits'])
            else:
                break

            res = es_client.scroll(scroll_id=scroll_id, scroll='2m')

        df = GenerateDataset(index)

        dfTicker = GenerateDataset.createDataStructure(df, items)
        dfTicker.drop_duplicates(subset=['tweet'],inplace=True,ignore_index=True)
        dfTicker = dfTicker.loc[:, ['timestamp', 'tweet']]

    return dfTicker
