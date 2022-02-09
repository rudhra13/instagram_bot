from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.chrome.options import Options
import pymysql
from datetime import datetime



chromedriver_path = '/Users/rudhra.r/Desktop/flock/other_projects/selenium/chromedriver' # Change this to your own chromedriver path!

# account_name = "rudhra13"
# account_passwd = "arhdur0250_IG"
# account_to_get_details = "rudhra13"


# account_name = "rudhra13"
# account_passwd = "arhdur0250_IG"
# account_to_get_details = "chetantulsyan"

account_name = "taste_with_bhukkad"
account_passwd = "arhdur0250_IG"
account_to_get_details = "taste_with_bhukkad"

# account_to_get_details = "bakery_cornor"
# account_to_get_details = "indianfoodchannel"
# account_to_get_details = "indianfoodyy"

# account_name = "bakarchodno1"
# account_passwd = "arhdur0250_IG"

# account_name = "saint_insights"
# account_passwd = "arhdur0250_IG"
# account_to_get_details = "saint_insights"

# account_name = "memeworld_in"
# account_passwd = "arhdur0250_IG"
# account_to_get_details = "memeworld_in"



total_followed_count = 0
total_skipped_count = 0


push_domain_db = {
	'user': 'root',
	'password': 'Root@123',
	'db': 'instagram_bot',
	'host': '127.0.0.1'
}

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
            print "Connection Unsuccessful"
            connection.close()
            exit()
    except Exception as err:
        print("ERROR: DB Operation: "+str(err))
    finally:
        return result
 
def check_exists_by_xpath(webdriver, xpath):
    try:
        webdriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def count_users(webdriver, connection, action):

	scrolling_section = webdriver.find_element_by_css_selector("body > div.RnEpo.Yx5HN > div > div > div.isgrP")
	# Get scroll height
	last_height = webdriver.execute_script("return arguments[0].scrollHeight",scrolling_section)
	action_count_on_other_users = 0
	while True:
		# Scroll down to bottom
		webdriver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrolling_section)
		# Wait to load page
		sleep(randint(3,4))
		# Calculate new scroll height and compare with last scroll height
		new_height = webdriver.execute_script("return arguments[0].scrollHeight",scrolling_section)

		_run = True
		j = 0
		while _run:
			action_count_on_other_users += 1
			try:
				if check_exists_by_xpath(webdriver,"/html/body/div[5]/div/div/div/div[1]/h3"):
					print("Instagram Blocking Us out, Error: "+str(webdriver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[1]/h3").text))
					webdriver.close()
					webdriver.quit()
					connection.close()
					exit()
				if check_exists_by_xpath(webdriver,"/html/body/div[4]/div/div/div[2]/ul/div/li["+str(action_count_on_other_users)+"]/div/div[1]/div[2]/div[1]/span/a"):
					user = webdriver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div/li["+str(action_count_on_other_users)+"]/div/div[1]/div[2]/div[1]/span/a").text
					if user == "" and check_exists_by_xpath(webdriver,"/html/body/div[5]/div/div/div[2]/ul/div/li["+str(action_count_on_other_users)+"]/div/div[1]/div[2]/div[1]/span/a"):
						user = webdriver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li["+str(action_count_on_other_users)+"]/div/div[1]/div[2]/div[1]/span/a").text
					now = datetime.now()
					date_time = now.strftime('%Y-%m-%d %H:%M:%S')

					check_user_exists_query = "SELECT user_name, COUNT(*) FROM `"+account_to_get_details+"_"+action+"` WHERE user_name = '"+user+"' GROUP BY user_name;"
					row_count = account_db(connection, check_user_exists_query,"get_row_count")
					if row_count == 0:
						print(str(date_time)+" "+account_to_get_details+" "+action+" "+str(action_count_on_other_users)+" New User: "+user)
						sql_query = "INSERT INTO `"+account_to_get_details+"_"+action+"` (`first_"+action+"_check_time`, `updated_"+action+"_check_time`, `account_name`, `user_name`) VALUES ('"+str(date_time)+"', '"+str(date_time)+"', '"+account_to_get_details+"',  '"+user+"');"
						status = account_db(connection, sql_query,"insert")
						if not str(type(status)) == "<type 'tuple'>":
							print("ERROR: Query Failed, For reference Query is: "+sql_query)
					else:
						if action == "Following":
							print(str(date_time)+" "+account_to_get_details+" "+action+" "+str(action_count_on_other_users)+" Existing User: "+user)
							sql_query = "UPDATE `"+account_to_get_details+"_"+action+"` SET updated_"+action+"_check_time = '"+str(date_time)+"',status = NULL WHERE user_name = '"+user+"';"
							status = account_db(connection, sql_query,"update")
							if not str(type(status)) == "<type 'tuple'>":
								print("ERROR: Query Failed, For reference Query is: "+sql_query)
						else:
							print(str(date_time)+" "+account_to_get_details+" "+action+" "+str(action_count_on_other_users)+" Existing User: "+user)
							sql_query = "UPDATE `"+account_to_get_details+"_"+action+"` SET updated_"+action+"_check_time = '"+str(date_time)+"' WHERE user_name = '"+user+"';"
							status = account_db(connection, sql_query,"update")
							if not str(type(status)) == "<type 'tuple'>":
								print("ERROR: Query Failed, For reference Query is: "+sql_query)
				else:
					_run = False
					action_count_on_other_users -= 1
			except Exception as e:
				print(str(e))
				j+=1
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


def act_login(webdriver, user_name, passwd):
	print("Opening https://www.instagram.com/")
	webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
	sleep(randint(3,5))

	print("Putting Username and Password")
	username = webdriver.find_element_by_name('username')
	username.send_keys(user_name)
	password = webdriver.find_element_by_name('password')
	password.send_keys(passwd)

	print("Logging in to the account -> "+str(user_name))
	button_login = webdriver.find_element_by_css_selector("#loginForm > div > div:nth-child(3) > button")
	button_login.click()
	sleep(randint(4,6))

	print("Save Login Info Pop Up -> Not Now")
	button_login = webdriver.find_element_by_css_selector("#react-root > section > main > div > div > div > div > button")
	button_login.click()
	sleep(randint(3,5))

def get_followed_users(webdriver, connection, act_name):
	print("Opening "+str(act_name)+" Account")
	webdriver.get('https://www.instagram.com/'+str(act_name)+'/')
	sleep(5)

	print("Clicking followers button for getting the usernames(Followed Users)")
	followers_section = webdriver.find_element_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(2) > a")
	followers_section.click()
	sleep(10)

	count_users(webdriver, connection, "followed")


def get_following_users(webdriver, connection, act_name):
	print("Opening "+str(act_name)+" Account")
	webdriver.get('https://www.instagram.com/'+str(act_name)+'/')
	sleep(3)

	print("Clicking following button for getting the usernames(Following Users)")
	followers_section = webdriver.find_element_by_css_selector("#react-root > section > main > div > header > section > ul > li:nth-child(3) > a")
	followers_section.click()
	sleep(10)

	count_users(webdriver, connection, "following")


chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
chrome_options.add_argument('window-size=1400,600')
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

webdriver1 = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)

db = push_domain_db 
connection = pymysql.connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'], charset='utf8mb4')

print("Web Driver Initilized")
sleep(5)
act_login(webdriver1,account_name, account_passwd)
get_followed_users(webdriver1, connection, account_to_get_details)
get_following_users(webdriver1, connection, account_to_get_details)

webdriver1.close()
webdriver1.quit()
connection.close()

