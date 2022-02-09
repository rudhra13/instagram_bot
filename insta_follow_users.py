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

def account_db(connection, query, query_type):
    query = ' '.join([line.strip() for line in query.splitlines()]).strip()
    result = []
    try:
        if (connection):
            cursor = connection.cursor()
            cursor.execute(query)
            if query_type == "insert" or query_type == "update":
                result = cursor.fetchall()
                connection.commit()
            elif query_type == "get_row_count":
                result = cursor.rowcount
            elif query_type == "select_rows":
                result = cursor.fetchall()
        else:
            print "Connection unsuccessful"
            connection.close()
            exit()
    except Exception as err:
        print("ERROR: DB Operation: "+str(err))
    finally:
        return result

def check_exists_by_xpath(webdriver,xpath):
    try:
        webdriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def follow_user_attempt(webdriver, act_name, user, follow_user_button, action, follow_type, connection):
	global total_followed_count
	now = datetime.now()
	date_time = now.strftime('%Y-%m-%d %H:%M:%S')

	user_follow_attempt= 0
	while user_follow_attempt <= 3:
		if follow_user_button.text == 'Follow':
			follow_user_button.click()
			sleep(randint(4,5))
			user_follow_attempt += 1
		else:
			if user_follow_attempt >= 1:
				total_followed_count += 1
				print(str(date_time)+" "+str(account_name)+" "+follow_type+" "+str(user)+" "+str(follow_user_button.text))
				
				check_user_exists_query = "SELECT user_name, COUNT(*) FROM "+account_name+"_"+action+" WHERE user_name = '"+user+"' GROUP BY user_name;"
				row_count = account_db(connection, check_user_exists_query, "get_row_count")
				if row_count == 0:
					sql_query = "INSERT INTO "+account_name+"_"+action+" (`first_"+action+"_time`, `account_name`, `follow_type`, `user_name`, `status`) VALUES ('"+date_time+"', '"+account_name+"', '"+follow_type+"', '"+user+"','"+follow_user_button.text+"');"
					status = account_db(connection, sql_query, "insert")
					if not str(type(status)) == "<type 'tuple'>":
						print("ERROR: Query Failed, For reference Query is: "+sql_query)

				if follow_user_button.text == "Following":
					check_user_exists_query = "SELECT user_name, COUNT(*) FROM "+account_name+"_following WHERE user_name = '"+user+"' GROUP BY user_name;"
					row_count = account_db(connection, check_user_exists_query, "get_row_count")
					if row_count == 0:
						sql_query = "INSERT INTO `"+account_name+"_following` (`first_following_check_time`, `updated_following_check_time`, `account_name`, `user_name`) VALUES ('"+str(date_time)+"', '"+str(date_time)+"', '"+account_name+"',  '"+user+"');"
						status = account_db(connection, sql_query, "insert")
						if not str(type(status)) == "<type 'tuple'>":
							print("ERROR: Query Failed, For reference Query is: "+sql_query)

				return user_follow_attempt
	return user_follow_attempt


def follow_users(webdriver, act_name, action, follow_type, connection):
	scrolling_section = webdriver.find_element_by_css_selector("body > div.RnEpo.Yx5HN > div > div > div.isgrP")
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

		_run = True
		j = 0
		while _run:
			try:
				if check_exists_by_xpath(webdriver,"/html/body/div[5]/div/div/div/div[1]/h3"):
					print("Instagram Blocking Us out, Error: "+str(webdriver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[1]/h3").text))
					webdriver.close()
					webdriver.quit()
					connection.close()
					exit()
				# action_count_on_other_users += 1
				print("Account Followed User Count -> "+str(action_count_on_other_users))
				if action_count_on_other_users >= 1:
					if check_exists_by_xpath(webdriver,"/html/body/div[4]/div/div/div[2]/ul/div/li["+str(action_count_on_other_users)+"]/div/div[1]/div[2]/div[1]/span/a"):
						user = webdriver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li["+str(action_count_on_other_users)+"]/div/div[1]/div[2]/div[1]/span/a").text

						check_user_exists_in_db_query = "SELECT temp.user_name, COUNT(*) from (SELECT user_name FROM "+account_name+"_followed UNION SELECT user_name FROM "+account_name+"_following UNION SELECT user_name FROM "+account_name+"_follow_attempt) as temp where temp.user_name = '"+user+"' GROUP BY temp.user_name;"
						row_count = account_db(connection, check_user_exists_in_db_query, "get_row_count")
						if row_count == 0:
							follow_user_button = webdriver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li["+str(action_count_on_other_users)+"]/div/div[2]/button")
							follow_user_button_next = webdriver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li["+str(action_count_on_other_users+1)+"]/div/div[2]/button")
							if follow_user_button.text == "Follow":
							# and follow_user_button_next.text == "Follow":
								user_follow_attempt = follow_user_attempt(webdriver, act_name, user, follow_user_button, action, follow_type, connection)
								if user_follow_attempt == 3:
									print("Not able to Follow Last Account")
									webdriver.close()
									webdriver.quit()
									connection.close()
									exit()

								print("Total User Account Followed Count Till Now: "+str(total_followed_count))
								if total_followed_count == 40:
									print("Max Account Followed")
									webdriver.close()
									webdriver.quit()
									connection.close()
									exit()

						if action_count_on_other_users % randint(30,35) == 0:
							sleep(randint(20,30))
					else:
						_run = False
						action_count_on_other_users -= 1

				action_count_on_other_users += 1

			except Exception as e:
				print(str(e))
				j += 1
				if j == 10:
					webdriver.close()
					webdriver.quit()
					connection.close()
					exit()
				pass

		if new_height == last_height:
			print("end")
			sleep(10)
			break
		last_height = new_height


def follow_users_from_act(webdriver, act_name, action, follow_type,connection):

	global total_followed_count
	# global total_skipped_count

	webdriver.get('https://www.instagram.com/'+str(act_name)+'/')
	print("Opening "+str(act_name)+" Account")
	sleep(3)

	followers_section = webdriver.find_element_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(2) > a")
	followers_section.click()
	print("Clicking followers button for getting the usernames")
	sleep(10)

	follow_users(webdriver, act_name, action, follow_type, connection)

chromedriver_path = '/Users/rudhra.r/Desktop/flock/other_projects/selenium/chromedriver' # Change this to your own chromedriver path!
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
chrome_options.add_argument('window-size=1400,600')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

db = push_domain_db 
connection = pymysql.connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'],charset='utf8mb4')

webdriver1 = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)

sleep(5)
act_login(webdriver1,account_name, account_passwd)
follow_users_from_act(webdriver1, account_to_follow, "follow_attempt", "account_general_followers", connection)
# follow_users_from_act(webdriver1, account_to_follow, "follow_attempt", "account_post_likers",connection)
webdriver1.close()
webdriver1.quit()
connection.close()


