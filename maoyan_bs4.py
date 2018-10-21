import requests
from bs4 import BeautifulSoup
import json, time

def parser(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
    	print(item)
    	write_to_file(item)
    #print(html)`
 
def get_one_page(url):
	headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
	}
	response = requests.get(url, headers = headers)
	if response.status_code == 200:
		return response.text
	print('response status:' + str(response.status_code))
	return None

def parse_one_page(html):
	soup = BeautifulSoup(html, 'lxml')
	#print(soup.dd)
	dds = soup.find_all(name='dd')
	#print(dds)
	for d in dds:
		i = {}
		i['name'] = d.find(name='p',class_ ='name').a.string
		i['star'] = d.find(name='p',class_ ='star').string.strip()[3:]
		i['releasetime'] = d.find(name='p',class_ ='releasetime').string.strip()[5:]
		integer = d.find(name='p',class_ ='score').find(class_='integer').string
		fraction = d.find(name='p',class_ ='score').find(class_='fraction').string
		#print()
		i['score'] = float(integer+fraction)
		yield i

def write_to_file(content):
    with open('maoyan.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    for i in range(10):
        parser(offset=i * 10)
        time.sleep(1)