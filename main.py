from multiprocessing import Pool
from get_channel import channel_list
from page_info import get_urls_from,get_item_info
import pymongo
# 多线程

client = pymongo.MongoClient('localhost',27017)
tongcheng = client['tongcheng']
url_list = tongcheng['url_list']


def get_all_urls_from(channel):
    for i in range(1,2):
        get_urls_from(channel,i)






if __name__ == '__main__':
    pool = Pool()

    pool.map(get_all_urls_from,channel_list.split())

    for url in url_list.find():
    print(url['url'])
    get_item_info(url['url'])

