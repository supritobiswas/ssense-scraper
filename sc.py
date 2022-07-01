from concurrent.futures import ThreadPoolExecutor
from csv import DictWriter
from tenacity import retry
from pathlib import Path
import browser_cookie3
import pandas as pd
import requests
import json
import re


final_data = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

def refreshCookies():
	cj = browser_cookie3.chrome()
	domain_url = 'ssense.com'
	ss_cookies = {}
	for c in cj:
		if domain_url in c.domain:
			ss_cookies['{}'.format(c.name)] = c.value
	return ss_cookies

# Get Data from each URL
@retry(wait=wait_fixed(2))
def getData(prod_url):
	item_main_cat = prod_url['category']
	item_url = prod_url['url']
	resp = requests.get(url=f'{item_url}.json', headers=headers, cookies=refreshCookies())
	if 'Access to this page has been denied' in resp.text:
		print('Perimeter-x Block! Retrying.')
		raise HTTPError("PX-Block!")
	elif '"product":{"id"' in resp.text:
		try:
			data = resp.json()['product']
			#Get Fields
			brand = data['brand']['name']
			prodname = data['name']
			desc = data['description']
			sku = data['sku']
			price = data['price']['regular']
			curr = data['price']['currency']
			comp = data['composition']
			imgurls = data['images']
			item_cat = data['category']['name'].title()
			#Download Images
			Path(f'{item_main_cat}_{item_cat}/{item_main_cat}_{item_cat}_Images').mkdir(parents=True, exist_ok=True)
			Path(f'{item_main_cat}_{item_cat}/{item_main_cat}_{item_cat}_Data').mkdir(parents=True, exist_ok=True)
			for idx, imgurl in enumerate(imgurls):
				imgurl = imgurl.replace('__IMAGE_PARAMS__', 'b_white,g_center,f_auto,q_auto:best')
				resp = requests.get(url=imgurl, stream=True)
				with open(f'{item_main_cat}_{item_cat}/{item_main_cat}_{item_cat}_Images/{sku}_{idx+1}.jpg', 'wb') as f:
					f.write(resp.content)
					f.close()
			#Data to Dictionary
			datum = {
				'URL': item_url,
				'Brand': brand,
				'Product Name': prodname,
				'Description': desc,
				'SKU': sku,
				'Price': price,
				'Currency': curr,
				'Fabric': comp,
				'Main Image': imgurls[0].replace('__IMAGE_PARAMS__', 'b_white,g_center,f_auto,q_auto:best'),
			}
			final_data.append(datum)
			#Dictionary to Category CSV
			csv_headers = ['URL','Brand','Product Name','Description','SKU','Price','Currency','Fabric','Main Image']
			with open(f'{item_main_cat}_{item_cat}/{item_main_cat}_{item_cat}_Data/Data.csv', 'a', newline='', encoding='utf-8') as f:
				dw = DictWriter(f, fieldnames=csv_headers)
				if f.tell() == 0:
					dw.writeheader()
				dw.writerow(datum)
				f.close()
			print('{} done!'.format(datum['URL']))
			return final_data
		except:
			with open('Exceptions.txt', 'a') as ex_f:
				ex_f.write(f'{item_url}\n')
			return

@retry(wait=wait_fixed(2))
def main_get_URLs(mainurl):
	prod_urls = []
	category = re.search(r'/([^/]*)$', mainurl).group(1).title()
	pagenum = 0
	while True:
		pagenum+=1
		starturl = f'{mainurl}.json?page={pagenum}'
		resp = requests.get(url=starturl, headers=headers, cookies=refreshCookies())
		if 'Access to this page has been denied' in resp.text:
			print('Perimeter-x Block! Retrying.')
			raise HTTPError("PX-Block!")
			break
		else:
			data = resp.json()
			for product in data['products']:
				url = 'https://www.ssense.com/en-ca{}'.format(product['url'])
				prod_url_datum = {'url': url, 'category': category}
				prod_urls.append(prod_url_datum)
			print(f'Done {category} page {pagenum}')
			if data['meta']['total_pages'] == pagenum:
				break
	print('Getting data for {} {} products->'.format(len(prod_urls), category))
	with ThreadPoolExecutor(max_workers=None) as executor:
		executor.map(getData, prod_urls)

	df = pd.DataFrame.from_dict(final_data)
	writer = pd.ExcelWriter(f'{category}.xlsx', engine='xlsxwriter')
	df.to_excel(writer, sheet_name='Data', index=False)
	writer.save()
	return

mainurl = 'https://www.ssense.com/en-ca/women/activewear'

main_get_URLs(mainurl)


#Testing only
# getData({'url':'https://www.ssense.com/en-ca/women/product/kimhekim/white-logo-yoga-bra/9094001', 'category':'Tops'})
