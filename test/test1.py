from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

server = Server(".\\bin\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat")
server.start()
proxy = server.create_proxy()

chrome_options = Options()
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
chrome_options.add_argument('--disable-gpu')  # 禁用浏览器正在被自动化程序控制的提示
chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # 禁止图片加载
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 防止被发现
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("allow-running-insecure-content")
chrome_options.add_argument("--test-type")
driver = webdriver.Chrome(options=chrome_options)
# 要访问的地址
base_url = "https://www.7seasweb.com/explore"
proxy.new_har("ht_list2", options={'captureContent': True})

driver.get(base_url)
# 此处最好暂停几秒等待页面加载完成，不然会拿不到结果
time.sleep(3)
result = proxy.har

for entry in result['log']['entries']:
    _url = entry['request']['url']
    print(_url)
    # # 根据URL找到数据接口,这里要找的是 http://git.liuyanlin.cn/get_ht_list 这个接口
    if "http://git.liuyanlin.cn/get_ht_list" in _url:
        _response = entry['response']
        _content = _response['content']
        # 获取接口返回内容
        print(_response)

server.stop()
driver.quit()