import os
import random
import threading
import time
from logging import exception

import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from seleniumwire.webdriver import Chrome
from tqdm import tqdm

caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {
    'browser': 'ALL',
    'performance': 'ALL',
}
caps['perfLoggingPrefs'] = {
    'enableNetwork': True,
    'enablePage': False,
    'enableTimeline': False
}


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
            opt.add_argument("--user-data-dir=D:/tmp/chromedriver")
            opt.add_argument("--start-maximized")
            opt.add_argument("allow-running-insecure-content")
            opt.add_argument("--test-type")
            # opt.add_argument('--headless')
            # opt.add_argument('user-age=M    ozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36')
            opt.add_argument(f'user-agent={cls.get_user_agent()}')
            # opt.add_experimental_option('w3c', False)  # 重要参数，不添加在无头模式无法获取日志！！
            #
            # opt.add_experimental_option('perfLoggingPrefs', {
            #     'enableNetwork': True,
            #     'enablePage': False,
            # })
            # 目标URL

            web = Chrome(options=opt,
                         desired_capabilities=caps,
                         service=Service(r".\bin\chromedriver.exe"))
            cls.driver = web
            # cls.driver.get('http://www.baidu.com')
            # cls.driver.implicitly_wait(10)
            # cls.driver.minimize_window()
            # cls.driver.maximize_window()

        return cls.driver


class NFTCrawler:
    web: Chrome

    def __init__(self):
        self.web = Common.get_driver()

    # def base64_to_image(self, base64_str):
    #     base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    #     byte_data = base64.b64decode(base64_data)
    #     image_data = BytesIO(byte_data)
    #     img = Image.open(image_data)
    #     return img

    def download_img_by_url(self, url, filename):
        # 下载图片
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            open(filename, 'wb').write(r.content)  # 将内容写入图片
        del r
    # def download_img_by_request_log(self, filename):
    #     for r in self.web.iter_requests():
    #         print(filename, r.url)
    #         if filename in r.url:
    #             with open(filename, 'wb') as f:
    #                 f.write(r.response.body)
    #
    # def download_whole_page_imgs(self, size):
    #     for i in range(size):
    #         css_selector = '#root > div:nth-child(1) > section.tf-section.sc-explore-1 > div > div > div > div > div.card-media > a > img'
    #         js = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
    #              f"let img = document.querySelectorAll('{css_selector}')[{i}]; /*找到图片*/ " \
    #              "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
    #              "img.setAttribute('crossorigin', 'anonymous');" \
    #              "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
    #              "let base64String = c.toDataURL();return img.src.split('/').pop() + '`'+ base64String;"
    #
    #         img_name, base64_str = self.web.execute_script(js).split("`")
    #         img = self.base64_to_image(base64_str)
    #         img.save(img_name)

    # def get_img_by_js(self, filename):
    #     css_selector = '#root > div:nth-child(1) > section.tf-section.sc-explore-1 > div > div > div > div > div.card-media > a > img'
    #     js = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
    #          f"let img = document.querySelectorAll('{css_selector}')[0]; /*找到图片*/ " \
    #          "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
    #          "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
    #          "let base64String = c.toDataURL();return base64String;"
    #
    #     base64_str = self.web.execute_script(js)
    #     img = self.base64_to_image(base64_str)
    #     img.save(filename)

    def main(self):
        Common.mutex.acquire()
        # 首先打开浏览器，跳转到 知网高级检索的页面
        nft_url = 'https://www.7seasweb.com/explore'

        self.web.get(nft_url)
        del self.web.requests
        time.sleep(10)
        page_size_ele = self.web.find_element(By.XPATH, '//*[@id="antd"]/ul/li[11]/div[1]/div[1]/span[2]')
        page_size_ele.click()
        time.sleep(2)
        btn_108_ele = self.web.find_element(By.XPATH,
                                            '//*[@id="antd"]/ul/li[11]/div[1]/div[2]/div/div/div/div[2]/div/div/div/div[4]')
        btn_108_ele.click()
        time.sleep(10)
        count = 1
        while True:
            try:
                cardproducts = self.web.find_elements(By.CLASS_NAME, "sc-card-product")
                for item in tqdm(cardproducts, desc=f'第{count}页'):
                    title = item.find_element(By.CLASS_NAME, 'style2').text
                    tag = item.find_element(By.CLASS_NAME, 'tags').text
                    author = item.find_element(By.CSS_SELECTOR, 'div.info.text-truncate > h6').text
                    bid = item.find_element(By.CLASS_NAME, 'color-popup').text
                    img_src = item.find_element(By.TAG_NAME, 'img').get_attribute("src")
                    img_filename = img_src.split("/")[-1]
                    # self.download_img_by_request_log(img_filename)
                    self.download_img_by_url(img_src, img_filename)
                    print(title, tag, author, bid, img_filename)

                next_btn_ele = self.web.find_element(By.XPATH, '//*[@id="antd"]/ul/li[10]/button')
                next_btn_ele.click()
                time.sleep(10)
            except exception as e:
                break

        Common.mutex.release()

    def main2(self):
        Common.mutex.acquire()
        # 首先打开浏览器，跳转到 知网高级检索的页面
        nft_url = 'https://www.7seasweb.com/explore'

        self.web.get(nft_url)
        del self.web.requests
        time.sleep(10)
        page_size_ele = self.web.find_element(By.XPATH, '//*[@id="antd"]/ul/li[11]/div[1]/div[1]/span[2]')
        page_size_ele.click()
        time.sleep(2)
        btn_108_ele = self.web.find_element(By.XPATH,
                                            '//*[@id="antd"]/ul/li[11]/div[1]/div[2]/div/div/div/div[2]/div/div/div/div[4]')
        btn_108_ele.click()
        time.sleep(10)
        count = 1
        while True:
            try:
                next_btn_ele = self.web.find_element(By.XPATH, '//*[@id="antd"]/ul/li[10]/button')
                next_btn_ele.click()
                time.sleep(10)
            except exception as e:
                break
        Common.mutex.release()


if __name__ == "__main__":
    if not os.path.exists("D:/tmp/chromedriver"):
        os.mkdir("D:/tmp/chromedriver")

    # 清理后台进程
    os.system(r'taskkill /F /im chromedriver.exe')

    nft_crawler = NFTCrawler()
    nft_crawler.main()
