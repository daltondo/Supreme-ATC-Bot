import time, sys, requests, hashlib, configparser
from bs4 import BeautifulSoup 
from splinter import Browser 
from selenium import webdriver


# t0 = time.time()
""" Aquire info from info.cfg """
config = configparser.ConfigParser()
config.read('info.cfg')

# User's info 
name = config.get('Info', 'name')
email = config.get('Info', 'email')
tel = config.get('Info', 'tel')
address = config.get('Info', 'address')
zipcode = config.get('Info', 'zip')
city = config.get('Info', 'city')
state = config.get('Info', 'state')
country = config.get('Info', 'country')

# Card info 
cctype = config.get('Card', 'type').lower()
ccnumber = config.get('Card', 'number') 
ccmonth = config.get('Card', 'month')
ccyear = config.get('Card', 'year') 
cvv = config.get('Card', 'CVV') 

# Product info
product_name = config.get('Product', 'keyword')
product_color = config.get('Product', 'color')
selectOption = config.get('Product', 'size')
category = config.get('Product', 'category')

# Product 2 info
product_name2 = config.get('Product2', 'keyword')
product_color2 = config.get('Product2', 'color')
selectOption2 = config.get('Product2', 'size')
category2 = config.get('Product2', 'category')

# Website info
mainUrl = 'http://www.supremenewyork.com/shop/all/'
baseUrl = 'http://supremenewyork.com'
checkoutUrl = 'https://www.supremenewyork.com/checkout'
browser = Browser('chrome')
""" End info aquisition """




r = requests.get(mainUrl + category).text
r2 = requests.get(mainUrl + category2).text

# checks if product has been uploaded to site 
def main(r, pname, pcolor, size): 
	if product_name in r:
		checkPage(r, pname, pcolor, size)


# checks if the current site page contains the item you wish to purchase
def checkPage(r, pname, pcolor, size): 
	soup = BeautifulSoup(r, 'html.parser')
	product, color, link, checker = '', '', '', False  

	while True:
		for div in soup.find_all('div', 'turbolink_scroller'):
			for a in div.find_all('a', href=True, text=True): 
				if pname in a.text:
					product = a.text
					checker = a['href']
				if a['href'] == checker and pcolor in a.text:
					color = a.text 
					link = a['href']

					if (product != '') and (color != '') and (link != ''): 
						check_product(product, color, link, size)


# verifies with the user that this is the item you are purchasing
def check_product(product, color, link, size):  
	product_url = baseUrl + link 
	print('WHAT YOU\'RE PURCHASING: \n' + 
		  'NAME: ' + product + '\n' + 
		  'COLOR: ' + color + '\n' + 
		  'LINK: ' + product_url)	
			
	buy_product(product_url, size)


# completes check out for the product
def buy_product(url, size): 
	browser.visit(url)
	try: 
		browser.find_option_by_text(size).first.click()
	except: 
		print('Sold out :(')
		quit()
	browser.find_by_name('commit').click()

	if (product_name2 != ""): 
		main(r2, product_name2, product_color2, selectOption2)

	if browser.is_text_present('item'): 
		print('Added to cart!')
		print('About to check out!')
		time.sleep(0.1)
		browser.visit(checkoutUrl)

	print('Filling in your info!')
	browser.fill('order[billing_name]', name)
	browser.fill('order[email]', email)
	browser.fill('tl', tel)
	browser.fill('order[billing_address]', address)  
	browser.fill('order[billing_zip]', zipcode) 
	browser.fill('order[billing_city]', city)
	browser.select('order[billing_state]', state)
	browser.select('order[billing_country]', country) 

	print('Filling in your card!')
	browser.select('credit_card[type]', cctype)
	browser.fill('credit_card[cnb]', ccnumber)
	browser.select('credit_card[month]', ccmonth)
	browser.select('credit_card[year]', ccyear) 
	
	try: 
		browser.fill('credit_card[vval]', cvv)
	except: 
		browser.fill('credit_card[ovv]', cvv)

	browser.find_by_name('commit').click()
	quit()


start_time = time.time()
while True: 
	main(r, product_name, product_color, selectOption)
	print('Seconds: ' + str(time.time() - start_time))
	time.sleep(0.5)











