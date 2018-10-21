from urllib.parse import urlencode
from pyquery import PyQuery as pq
import requests

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
	'Host': 'm.weibo.cn',
	'Referer': 'https://m.weibo.cn/u/2719139813',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest'
}


def get_page(page):
	params = {
		'type': 'uid',
		'value': '2719139813',
		'containerid': '1076032719139813',
		'page': page
	}
	url = base_url + urlencode(params)
	try:
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			return response.json()
	except requests.ConnectionError as e:
		print('Error', e.args)

def parse_page(json):
	if json:
		items = json.get('data').get('cards')
		for item in items:
			item = item.get('mblog')
			weibo = {}
			weibo['id'] = item.get('id')
			weibo['text'] = pq(item.get('text')).text()
			weibo['attitudes'] = item.get('attitudes_count')
			weibo['comments'] = item.get('comments_count')
			weibo['reposts'] = item.get('reposts_count')
			yield weibo

if __name__ == '__main__':
	for page in range(1, 11):
		json = get_page(page)
		results = parse_page(json)
		for result in results:
			print(result)