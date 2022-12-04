import json
import os
import random
import sqlite3
import threading
import time

import brotli
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from seleniumwire.request import Response
from seleniumwire.webdriver import Chrome

insert_keys = ['id', 'contractAddress', 'creator', 'description', 'assetImageUrl', 'name', 'tokenId', 'tokenStandard', 'isCollect', 'collectCount', 'clickCount', 'nftPrice', 'owner', 'status', 'createTime', 'startTime', 'endTime', 'metadata', 'chainConfigName', 'coinConfigName', 'assetTypeId', 'createUserNickName', 'createUserImgLogo', 'ownerUserNickName', 'ownerUserImgLogo', 'auctionNumber', 'categoryId']
integer_keys = ['isCollect', 'collectCount', 'clickCount', 'nftPrice', 'status', 'createTime', 'startTime', 'endTime','assetTypeId', 'auctionNumber', 'categoryId']
def sqlite_insert(sql):
    try:
        s = cur.execute(sql)
        con.commit()
    except Exception as e:
        print(e)

def sqlite_create_table():

    sql_create = '''
       CREATE TABLE if not exists `t_nft` (
        `id`  CHAR(64) NOT NULL UNIQUE,
        `contractAddress`  VARCHAR(255) NOT NULL,                                                                                                                    
        `creator`  VARCHAR(255) NOT NULL,                                                                                               
        `description`  TEXT NULL,
        `assetImageUrl`  TEXT NOT NULL,
        `name`  VARCHAR(255) NOT NULL,
        `tokenId`  VARCHAR(255) NOT NULL,
        `tokenStandard`  VARCHAR(255) NOT NULL,
        `isCollect`  INT NOT NULL,
        `collectCount`  INT NOT NULL,
        `clickCount`  INT NOT NULL,
        `nftPrice`  BIGINT NOT NULL,
        `owner`  VARCHAR(255) NOT NULL,
        `status`  INT NOT NULL,
        `createTime`  DATETIME NOT NULL,
        `startTime`  DATETIME NOT NULL,
        `endTime`  DATETIME NOT NULL,
        `metadata`  TEXT NOT NULL,
        `chainConfigName`  VARCHAR(255) NOT NULL,
        `coinConfigName`  VARCHAR(255) NOT NULL,
        `assetTypeId`  INT NOT NULL,
        `createUserNickName`  VARCHAR(255) NOT NULL,
        `createUserImgLogo`  TEXT NOT NULL,
        `ownerUserNickName`  VARCHAR(255) NOT NULL,
        `ownerUserImgLogo`  TEXT NOT NULL,
        `auctionNumber`  BIGINT NOT NULL,
        `categoryId`  INT NOT NULL
       )
       '''

    # 用 execute 执行一条 sql 语句
    con.execute(sql_create)
    print('创建成功')
class Common:
    """driver的单例模式"""
    driver = None  # 将driver定义为类级变量，不随实例化而被重新赋值为None

    mutex = threading.Lock()
    user_agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]

    @classmethod
    def get_user_agent(cls):
        return random.choice(cls.user_agent)

    @classmethod
    def get_driver(cls):
        if cls.driver is None:
            # Chrome 参数选项
            opt = Options()
            opt.add_argument('--disable-gpu')  # 禁用浏览器正在被自动化程序控制的提示
            opt.add_argument('--blink-settings=imagesEnabled=false')  # 禁止图片加载
            opt.add_experimental_option('excludeSwitches', ['enable-automation'])  # 防止被发现
            opt.add_argument(f"--user-data-dir={chromedriver_datadir}")
            opt.add_argument("--start-maximized")
            opt.add_argument("allow-running-insecure-content")
            opt.add_argument("--test-type")
            if chromedriver_debug:
                opt.add_argument('--headless')
            # opt.add_argument('user-age=M    ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')
            opt.add_argument(f'user-agent={cls.get_user_agent()}')

            web = Chrome(options=opt,
                         service=Service(chromedriver_path))

            cls.driver = web
        return cls.driver
global_page_count = -1
def interceptor(request, response:Response):

    if interface_full in request.url and response.status_code == 200:
        body = response.body
        body = brotli.decompress(body)
        body = body.decode('utf-8')
        json_body = json.loads(body)
        data = json_body['data']
        page, pageSize, total, pageCount, true_data = \
            data['page'], data['pageSize'], data['total'], \
                data['pageCount'], data['data']
        global global_page_count
        global_page_count = pageCount
        print(f'第 {page} 页的数据 （pageSize={pageSize}）爬取成功！')
        for item in true_data:
            try:
                insert_values = [item[_] if _ in item.keys() else "null" for _ in insert_keys]
            except KeyError:
                print("debug", item)
                input()
            per_sql = f"""
            insert into `t_nft`({",".join([f'`{_}`'for _ in insert_keys])})
            values({",".join(map(lambda x: f"'{x}'" if x not in integer_keys else x, insert_values))})
            """
            sqlite_insert(per_sql)

class NFTCrawler:
    web: Chrome

    def __init__(self):
        self.web = Common.get_driver()
        self.web.response_interceptor = interceptor
    def download_img_by_url(self, url, filename):
        # 下载图片
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            open(filename, 'wb').write(r.content)  # 将内容写入图片
        del r

    def change_page_size_to_max(self):
        time.sleep(10)
        page_size_ele = self.web.find_element(By.XPATH, '//*[@id="antd"]/ul/li[11]/div[1]/div[1]/span[2]')
        time.sleep(5)
        page_size_ele.click()
        time.sleep(5)
        btn_108_ele = self.web.find_element(By.XPATH,
                                            '//*[@id="antd"]/ul/li[11]/div[1]/div[2]/div/div/div/div[2]/div/div/div/div[4]')
        time.sleep(5)
        btn_108_ele.click()



    def close(self):
        cur.close()
        con.close()
        self.web.quit()
    def main2(self):
        Common.mutex.acquire()
        # 首先打开浏览器，跳转到 知网高级检索的页面
        nft_url = 'https://www.7seasweb.com/explore'
        self.web.get(nft_url)
        self.change_page_size_to_max()

        count = 1
        next_btn_ele = self.web.find_element(By.XPATH, '//*[@id="antd"]/ul/li[10]/button')
        while True:
            try:
                time.sleep(10) # 每隔几秒翻一次页
                next_btn_ele.click()
            except Exception as e:
                time.sleep(10)

        Common.mutex.release()



current_dir = os.path.abspath(os.curdir)
chromedriver_path = os.path.join(current_dir, "bin", "chromedriver.exe")
chromedriver_datadir = os.path.join(current_dir, "tmp")
chromedriver_debug = False # 是否后台运行
interface_full = 'https://api.7seasweb.com/api/asset/findNftPageList'
max_page_size = 108
db_path = r'db.sqlite3'
con = sqlite3.connect(db_path, check_same_thread = False)
cur = con.cursor()

# 创建工作目录
if not os.path.exists(chromedriver_datadir):
    os.mkdir(chromedriver_datadir)

if __name__ == "__main__":
    sqlite_create_table()
    nft_crawler = NFTCrawler()
    nft_crawler.main2()
    nft_crawler.close()




