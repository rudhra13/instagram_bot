from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.chrome.options import Options
import pymysql
from datetime import datetime

# account_name = "taste_with_bhukkad"
# account_passwd = "arhdur0250_IG"
# account_to_follow = "khana_bazaar"

# account_to_follow = "bakery_cornor"
# account_to_follow = "indianfoodchannel"
# account_to_follow = "foodul"

account_name = "saint_insights"
account_passwd = "arhdur0250_IG"
account_to_follow = "chanakya_niti_quotes"

# account_name = "memeworld_in"
# account_passwd = "arhdur0250_IG"
# account_to_follow = "memesleela"

total_followed_count = 0
total_skipped_count = 0

push_domain_db = {
	'user': 'root',
	'password': 'Root@123',
	'db': 'instagram_bot',
	'host': '127.0.0.1'
}

def check_exists_by_xpath(webdriver,xpath):
    try:
        webdriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def act_login(webdriver,user_name,passwd):
	webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
	sleep(randint(3,5))

	username = webdriver.find_element_by_name('username')
	username.send_keys(user_name)
	password = webdriver.find_element_by_name('password')
	password.send_keys(passwd)

	button_login = webdriver.find_element_by_css_selector("#loginForm > div > div:nth-child(3) > button")
	button_login.click()
	print("logging in to the account -> "+str(user_name))
	sleep(randint(4,6))

	button_login = webdriver.find_element_by_css_selector("#react-root > section > main > div > div > div > div > button")
	button_login.click()
	print("Save Login Info Pop Up -> Not Now")
	sleep(randint(3,5))

def switch_to_account(webdriver,act_name):
	webdriver.get('https://www.instagram.com/'+str(act_name)+'/')
	print("Opening "+str(act_name)+" Account")
	sleep(3)

def follow_users(webdriver, act_name):
	scrolling_section = webdriver.find_element_by_css_selector("body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div")
	# Get scroll height
	last_height = webdriver.execute_script("return arguments[0].scrollHeight",scrolling_section)
	# action_count_on_other_users = 1
	while True:
		# Scroll down to bottom
		webdriver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrolling_section)
		# Wait to load page
		sleep(randint(8,10))
		# Calculate new scroll height and compare with last scroll height
		new_height = webdriver.execute_script("return arguments[0].scrollHeight",scrolling_section)

		_run = True
		j = 0
		action_count_on_other_users = 1
		while _run:
			try:
				if check_exists_by_xpath(webdriver,"/html/body/div[5]/div/div/div/div[1]/h3"):
					print("Instagram Blocking Us out, Error: "+str(webdriver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[1]/h3").text))
					webdriver.close()
					webdriver.quit()
					exit()
				if action_count_on_other_users >= 1:
														/html/body/div[5]/div/div/div[2]/div/div/div[1]
														/html/body/div[5]/div/div/div[2]/div/div/div[1]
														body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div > div > div:nth-child(1)
														body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div > div > div:nth-child(2)
														body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div > div > div:nth-child(11)
														body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div > div > div:nth-child(17)
					if check_exists_by_xpath(webdriver,"/html/body/div[5]/div/div/div[2]/div/div/div["+str(action_count_on_other_users)+"]/div[2]/div[1]/div/span/a"):
						print("Account Followed User Count -> "+str(action_count_on_other_users))
						user = webdriver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div/div/div["+str(action_count_on_other_users)+"]/div[2]/div[1]/div/span/a")
						print(user.text)
						# sleep(1)
					elif check_exists_by_xpath(webdriver,"/html/body/div[6]/div/div/div[2]/div/div/div["+str(action_count_on_other_users)+"]/div[2]/div[1]/div/span/a"):
						user = webdriver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div/div/div["+str(action_count_on_other_users)+"]/div[2]/div[1]/div/span/a")
						print(user.text)
						# sleep(1)
					else:
						_run = False
						sleep(10)
						# scroll_1 = randint(15,20)
						# webdriver.execute_script("arguments[0].scrollBy(0,-"+str(scroll_1)+");",scrolling_section) 
						# sleep(randint(3,4))
						# webdriver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrolling_section)
						# sleep(randint(7,10))
						# webdriver.execute_script("arguments[0].scrollBy(0,-"+str(scroll_1)+");",scrolling_section) 
						# sleep(randint(3,4))
						# webdriver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrolling_section)
						# sleep(randint(7,10))
						break

					# if action_count_on_other_users >= 10:
					# 	_run = False
					# 	sleep(5)
				# sleep(4)

				action_count_on_other_users += 1
			except Exception as e:
				print(str(e))
				j += 1
				if j == 10:
					# webdriver.close()
					# webdriver.quit()
					# connection.close()
					# exit()
					break
				pass
		webdriver.execute_script("arguments[0].scrollBy(0,-"+str(randint(30,40))+");",scrolling_section) 
		sleep(randint(2,4))
		webdriver.execute_script("arguments[0].scrollHeight", scrolling_section)
		sleep(randint(5,7))
		webdriver.execute_script("arguments[0].scrollBy(0,-"+str(randint(20,30))+");",scrolling_section) 
		sleep(randint(2,4))
		webdriver.execute_script("arguments[0].scrollHeight", scrolling_section)
		sleep(randint(7,10))


		if new_height == last_height:
			print("Liked Users list end")
			print("############################")
			sleep(10)
			return
		last_height = new_height

	return

def profile_scrolling(webdriver,act_name):
	scrolling_section = webdriver.find_element_by_css_selector("#react-root > section > main > div > div._2z6nI > article > div:nth-child(1) > div")
	# Get scroll height
	last_height = webdriver.execute_script("return arguments[0].scrollHeight",scrolling_section)
	action_count_on_other_users = 1
	while True:
		# Scroll down to bottom
		webdriver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrolling_section)
		# Wait to load page
		sleep(randint(2,3))
		# Calculate new scroll height and compare with last scroll height
		new_height = webdriver.execute_script("return arguments[0].scrollHeight",scrolling_section)

		vertical=1
		while vertical <= 1:
			horizontal = 1
			while horizontal <=1:
				if check_exists_by_xpath(webdriver,"/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div["+str(vertical)+"]/div["+str(horizontal)+"]/a"):
					photo = webdriver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[3]/article/div[1]/div/div["+str(vertical)+"]/div["+str(horizontal)+"]/a")
					photo.click()
					sleep(10)

				if check_exists_by_xpath(webdriver,"/html/body/div[4]/div[2]/div/article/div[3]/section[2]/div/div[2]/button"):
					liked_by = webdriver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[3]/section[2]/div/div[2]/button")
					liked_by.click()

				sleep(10)
				follow_users(webdriver, act_name)
				# sleep(10)
				user_close_button = webdriver.find_element_by_css_selector("body > div.RnEpo.Yx5HN > div > div > div:nth-child(1) > div > div:nth-child(3) > button")
				user_close_button.click()
				photo_close_button = webdriver.find_element_by_css_selector("body > div._2dDPU.CkGkG > div.Igw0E.IwRSH.eGOV_._4EzTm.BI4qX.qJPeX.fm1AK.TxciK.yiMZG > button")
				photo_close_button.click()

				horizontal += 1
				sleep(5)
			vertical += 1
		if vertical == 5:
			print("Profile end by threshold")
			print("############################")
			sleep(10)
			break

		# if new_height == last_height:
		# 	print("Profile end")
		# 	print("############################")
		# 	sleep(10)
		# 	break
		last_height = new_height

chromedriver_path = '/Users/rudhra.r/Desktop/flock/other_projects/selenium/chromedriver' # Change this to your own chromedriver path!
chrome_options = webdriver.ChromeOptions()
# chrome_options.headless = True
chrome_options.add_argument('window-size=1400,600')
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# db = push_domain_db 
# connection = pymysql.connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'],charset='utf8mb4')

webdriver1 = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)

sleep(5)
act_login(webdriver1,account_name, account_passwd)
switch_to_account(webdriver1,account_to_follow)
profile_scrolling(webdriver1,account_to_follow)
webdriver1.close()
webdriver1.quit()
# connection.close()

