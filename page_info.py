from bs4 import BeautifulSoup
import requests
import time
import pymongo

# spider 1
client = pymongo.MongoClient('localhost',27017)
tongcheng = client['tongcheng']
url_list = tongcheng['url_list']
item_list = tongcheng['item_list']

def get_urls_from(channel, pages, who_sells=0):
    # http://bj.58.com/shouji/0/pn1/?PGTID=0d3001e7-0000-145b-1954-1d8fb2388e0f&ClickID=1
    #channel 抓取的品类链接
    # who_sells  0代表个人  1代表商家
    #pages  页码
    list_view = '{}{}/pn{}/'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #没有td.t 就结束
    if soup.find('td', 't'):
        for link in soup.select('td.t a.t'):
            # http://zhuanzhuan.58.com/detail/901663460499685385z.shtml?fullCate=5%2C36&fullLocal=1&from=pc&PGTID=0d300024-0000-1ddd-6879-e4bca4374cc3&ClickID=1
            # 通过?分割去除地址后的参数
            item_url = link.get('href').split('?')[0]
            url_list.insert_one({'url': item_url})
            print(item_url)
            # return urls
    else:
        # 页面不存在，也就是相当于最后一页
        #pass
        print('爬取完成！')



# spider 2
def get_item_info(url):
    if url.split('/')[-1] == 'jump':
        pass
    else:

        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        #判断商品页面存在与否，也就是是否卖出
        # 通过js链接中是否存在404判断
        no_longer_exist = '404' in soup.find('script', type="text/javascript").get('src').split('/')
        if no_longer_exist:
            item_info.insert_one({'title': '已卖出', 'price': '已卖出', 'date': '已卖出', 'area': '已卖出', 'url': '已卖出'})
        else:
            title = soup.title.text
            price = soup.select('span.price.c_f50')[0].text
            date = soup.select('.time')[0].text
            # 判断地区信息是否存在
            area = list(soup.select('c_25d  a')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None
            item_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})
            print({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})

