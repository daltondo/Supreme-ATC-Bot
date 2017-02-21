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
product_name = config.get('Product', 'keyword')[0].upper() + config.get('Product', 'keyword')[1:].lower()
product_color = config.get('Product', 'color')[0].upper() + config.get('Product', 'color')[1:].lower()
selectOption = config.get('Product', 'size')
category = config.get('Product', 'category')

# Website info
mainUrl = 'http://www.supremenewyork.com/shop/all/'
baseUrl = 'http://supremenewyork.com'
checkoutUrl = 'https://www.supremenewyork.com/checkout'
browser = Browser('chrome')
""" End info aquisition """




r = requests.get(mainUrl + category).text

# checks if product has been uploaded to site 
def main(): 
	if product_name in r:
		checkPage(r, t1)


# checks if the current site page contains the item you wish to purchase
def checkPage(r, t1): 
	soup = BeautifulSoup(r, 'html.parser')
	product, color, link, checker = '', '', '', False  

	while True:
		for div in soup.find_all('div', 'turbolink_scroller'):
			for a in div.find_all('a', href=True, text=True): 
				if product_name in a.text:
					product = a.text
					checker = a['href']
				if a['href'] == checker and product_color in a.text:
					color = a.text 
					link = a['href']

					if (product != '') and (color != '') and (link != ''): 
						check_product(product, color, link, t2)


# verifies with the user that this is the item you are purchasing
def check_product(product, color, link, t2): 
	while True: 
		if product_name in product and product_color in color: 
			product_url = baseUrl + link 
			print('WHAT YOU\'RE PURCHASING: \n' + 
				  'NAME: ' + product + '\n' + 
				  'COLOR: ' + color + '\n' + 
				  'LINK: ' + product_url)
			buy_product(product_url, t3)


# completes check out for the product
def buy_product(url, t3): 
	browser.visit(url)
	try: 
		browser.find_option_by_text(selectOption).first.click()
	except: 
		print('Sold out :(')
		quit()
	browser.find_by_name('commit').click()

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
	
	# browser.find_by_css('.string')[0].fill(cvv)
	# browser.find_by_value('CVV')[0].fill(cvv)
	# print(browser.find_by_text('CVV').__str__())
	# print(browser.find_by_text('CVV').__repr__())

	# id = cvw, vval
	# ovv, vval
	try: 
		browser.fill('credit_card[vval]', cvv)
	except: 
		browser.fill('credit_card[ovv]', cvv)

	browser.find_by_name('commit').click()
	quit()


start_time = time.time()
while True: 
	main()
	print('Seconds: ' + str(time.time() - start_time))
	time.sleep(0.5)

# browser.visit(checkoutUrl)
# browser.find_by_css('CVV')



""" ### TODO ### 
1. Fix time consumption of filling out shit 
   - Fix the cvv issue especially 
2. Fix user option of hats 
""" 









