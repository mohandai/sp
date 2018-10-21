from urllib.parse import urlencode
from pyquery import PyQuery as pq
import requests
import os
from hashlib import md5
from multiprocessing.pool import Pool
import time

base_url = 'https://www.toutiao.com/search_content/?'

headers = {
	'Host': 'www.toutiao.com',
	'Referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest'
}


def get_page(offset):
	params = {
		'offset': offset,
		'format': 'json',
		'keyword': '街拍',
		'autoload': 'true',
		'count': '20',
		'cur_tab': '1',
		'from': 'search_tab'
	}
	url = base_url + urlencode(params)
	try:
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			print('successfully get page offset: ' + str(offset))
			return response.json()
	except requests.ConnectionError as e:
		print('Error', e.args)

def get_images(json):
	if json.get('data'):
		for cell in json.get('data'):
			if cell.get('title') and cell.get('image_list'):
				title = cell.get('title')
				images = cell.get('image_list')
				print('getting images list: ' + title)
				image_set = []
				for image in images:
					image_set.append({
					'image': 'http:'+image.get('url'),
					'title': title
					})
					'''
					yield {
					'image': 'http:'+image.get('url'),
					'title': title
					}'''
				return image_set
	print('get images json failed')

	def save_image(item):
	if not os.path.exists(item.get('title')):
		os.mkdir(item.get('title'))
	try:
		response = requests.get(item.get('image'))
		if response.status_code == 200:
			file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
			if not os.path.exists(file_path):
				with open(file_path, 'wb') as f:
					f.write(response.content)
				print('image saved: ' + file_path)
			else:
				print('Already Downloaded', file_path)
	except requests.ConnectionError:
		print('Failed to Save Image')


	def main(offset):
	json = get_page(offset)
	for item in get_images(json):
		print(item)
		save_image(item)


GROUP_START = 1
GROUP_END = 5

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()

'''
if __name__ == '__main__':
	for offset in range(0,200,20):
		main(offset)
		time.sleep(1)

'''








