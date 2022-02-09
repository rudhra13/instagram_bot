from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd
from selenium.common.exceptions import NoSuchElementException   
from selenium.webdriver.chrome.options import Options
import pymysql
from datetime import datetime

# account_name = "memeworld_in"
# account_passwd = "arhdur0250_IG"

account_name = "saint_insights"
account_passwd = "arhdur0250_IG"

# account_name = "taste_with_bhukkad"
# account_passwd = "arhdur0250_IG"

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

def check_exists_by_css_selector(webdriver,css_selector):
    try:
        webdriver.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        return False
    return True

def act_login(webdriver,user_name,passwd):
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

def unfollow_users(webdriver, connection, account_name, action):

    unfollow_user_arr = ["/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/div[2]/button",
                        "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/button",
                        "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/div[2]/div/span/span[1]/button",
                        "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button",]
    
    unfollow_user_check_arr = ["/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button",
                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button",
                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/div[2]/div/span/span[1]/button",
                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button"]
    try:
        check_minimum_users = "select user_name from "+account_name+"_following where current_status != 'unfollowed' or current_status is null ;"
        row_count = account_db(connection, check_minimum_users, "get_row_count")
        if row_count >= 1000:
            sql_query = "select user_name from "+account_name+"_following where current_status != 'unfollowed' or current_status is null order by first_following_check_time desc limit 300;"
            following_users = account_db(connection, sql_query, "select_rows")
            if not str(type(following_users)) == "<type 'tuple'>":
                print("ERROR: Query Failed, For reference Query is: "+sql_query)

            user_count = 0
            user_account_count = 1
            for user_name in following_users:
                
                user_name = user_name[0]
                webdriver.get('https://www.instagram.com/'+str(user_name)+'/')
                print(str(user_account_count)+" Opening "+str(user_name)+" Account")
                sleep(randint(6,8))
                now = datetime.now()
                date_time = now.strftime('%Y-%m-%d %H:%M:%S')

                for unfollow_user in unfollow_user_arr:
                    if check_exists_by_xpath(webdriver, unfollow_user):
                        unfollow_user_button = webdriver.find_element_by_xpath(unfollow_user)
                        print(unfollow_user_button.text)
                        unfollow_user_button.click()
                sleep(randint(6,8))

                unfollow_user_confirm = "body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.-Cab_"
                if check_exists_by_css_selector(webdriver,unfollow_user_confirm):
                    unfollow_user_confirm_button = webdriver.find_element_by_css_selector(unfollow_user_confirm)
                    unfollow_user_confirm_button.click()
                    sleep(randint(4,6))

                for unfollow_user_check in unfollow_user_check_arr:
                    if check_exists_by_xpath(webdriver, unfollow_user_check):
                        unfollow_user_check_button = webdriver.find_element_by_xpath(unfollow_user_check)
                        if unfollow_user_check_button.text == "Follow" or unfollow_user_check_button.text == "Follow Back":
                            sql_query = "UPDATE `"+account_name+"_"+action+"` SET updated_"+action+"_check_time = '"+str(date_time)+"',current_status = 'unfollowed' WHERE user_name = '"+user_name+"';"
                            status = account_db(connection, sql_query, "update")
                            if not str(type(status)) == "<type 'tuple'>":
                                print("ERROR: Query Failed, For reference Query is: "+sql_query)
                            user_count += 1
                               
                user_not_found = "body > div.root.-cx-PRIVATE-Page__root.-cx-PRIVATE-Page__root__ > div.page.-cx-PRIVATE-Page__body.-cx-PRIVATE-Page__body__ > div > div > h2"                        
                user_not_found_other = "#react-root > section > main > div > h2"  

                if check_exists_by_css_selector(webdriver,user_not_found):
                    user_not_found_text = webdriver.find_element_by_css_selector(user_not_found)
                    if user_not_found_text.text == "Sorry, this page isn't available.":
                        print("User Not Found")
                        sql_query = "UPDATE `"+account_name+"_"+action+"` SET updated_"+action+"_check_time = '"+str(date_time)+"',current_status = 'unfollowed' WHERE user_name = '"+user_name+"';"
                        status = account_db(connection, sql_query, "update")
                        if not str(type(status)) == "<type 'tuple'>":
                            print("ERROR: Query Failed, For reference Query is: "+sql_query)
                        user_count += 1                  
                elif check_exists_by_css_selector(webdriver,user_not_found_other):
                    user_not_found_other_text = webdriver.find_element_by_css_selector(user_not_found_other)
                    if user_not_found_other_text.text == "Sorry, this page isn't available.":
                        print("User Not Found")
                        sql_query = "UPDATE `"+account_name+"_"+action+"` SET updated_"+action+"_check_time = '"+str(date_time)+"',current_status = 'unfollowed' WHERE user_name = '"+user_name+"';"
                        status = account_db(connection, sql_query, "update")
                        if not str(type(status)) == "<type 'tuple'>":
                            print("ERROR: Query Failed, For reference Query is: "+sql_query)
                        user_count += 1


                print("User Unfollowed: "+str(user_count))
                print("##################################")
                user_account_count += 1

    except Exception as e:
        print(e)

db = push_domain_db 
connection = pymysql.connect(host=db['host'], user=db['user'], password=db['password'], db=db['db'],charset='utf8mb4')

chromedriver_path = '/Users/rudhra.r/Desktop/flock/other_projects/selenium/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
chrome_options.add_argument('window-size=1400,600')
chrome_options.add_argument("--incognito")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)


webdriver1 = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
print("Web Driver Initilized")
sleep(5)

act_login(webdriver1, account_name, account_passwd)
unfollow_users(webdriver1, connection, account_name, "following")

webdriver1.close()
webdriver1.quit()
connection.close()

