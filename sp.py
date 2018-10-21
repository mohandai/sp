from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery as pq
from time import sleep


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
KEYWORD = 'iPad'
browser.get('https://s.taobao.com/')
cookies = {'v': '0', 'cookie2': '1b6efc49e2f899d0bb0d855efdf474da', '_tb_token_': '738e7fb8b5d95', 'cna': 'etYbEk1StDACAWViJrgMIpxw', 'thw': 'cn', 't': 'a205e1b643c9fffecb5cbfae2b767664', 'tracknick': 'hunterd0116', 'dnk': 'hunterd0116', 'tg': '0', 'enc': 'UNtoW%2BQ0ScIB%2BYrKXwi51I%2F31j7APK2FKTqIzhfGmlLXIMswA5lPrmiqhChOmcFfdl9jieUL%2BJGnbqgcR%2FNjJA%3D%3D', 'hng': 'CN%7Czh-CN%7CCNY%7C156', 'unb': '44341965', 'sg': '658', '_l_g_': 'Ug%3D%3D', 'skt': '21ec2e5d2063f765', 'cookie1': 'URn5%2FHWcWCfumiTe%2F7o3CsYrB4YMAwYhrmJbK9QssX4%3D', 'csg': '69adf92f', 'uc3': 'vt3=F8dByRmpFIYSjz%2Bktj8%3D&id2=Vyh%2FYBGbJGc%3D&nk2=CzhD91kKh1UEgOk%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D', 'existShop': 'MTU0MDEwNjM1OA%3D%3D', 'lgc': 'hunterd0116', '_cc_': 'V32FPkk%2Fhw%3D%3D', '_nk_': 'hunterd0116', 'cookie17': 'Vyh%2FYBGbJGc%3D', 'mt': 'ci=10_1', 'uc1': 'cookie14=UoTYNkZCkkexbg%3D%3D&lng=zh_CN&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&existShop=false&cookie21=W5iHLLyFe3xm&tag=10&cookie15=VT5L2FSpMGV7TQ%3D%3D&pas=0', 'isg': 'BO3tvsCHSoAuSS67WTFKoi8i_I-n4iF1nAQMQS_yKQTzpg1Y95ox7Dt0lXpADTnU'}
cookie_keys = cookies.keys()
print(cookies)
for c in cookie_keys:
    browser.add_cookie({'name':c, 'value':cookies[c]})
    #print(c,' with: ', cookies[c])

def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """
    print('正在爬取第', page, '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        #browser.get(url)
        #browser.add_cookie()
        #sleep(1)
        browser.get(url)
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products(browser.page_source)
    except TimeoutException:
        index_page(page)


def get_products(html):
    """
    提取商品数据
    """
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)

MAX_PAGE = 3
def main():
    """
    遍历每一页
    """
    for i in range(1, MAX_PAGE + 1):
        index_page(i)

main()






