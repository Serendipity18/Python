'''
Created on Oct 28, 2019
This is a program I created to automate logging in to my colleges website.

Once this program is run it will ask you for your username and password to enter the site.
To fully automate this process you can set the username and password variables equal to your credentials.
The reason I don't have the code setup this way is for security reasons. I do not like keeping my usernames and passwords
in plain text in my program, and that is why it is not fully automated.
@author: Josh
'''
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

file = "geckodriver.log"


def SiteLogin(USERNAME, PASSWORD):
    # chooses the browser
    browser = webdriver.Firefox()
    # open website
    browser.get('http://put the url you want to use in between these quotes')
    # find element where to type in username
    button = browser.find_elements_by_xpath("//*[@id='username']")[0]
    # type in username
    button.send_keys(USERNAME)
    # find element where to type in username
    button = browser.find_elements_by_xpath("//*[@id='password']")[0]
    # type in password
    button.send_keys(PASSWORD)
    # click the login
    button = browser.find_elements_by_xpath("/html/body/div/div/div[2]/form/section[3]/input[4]")[0]
    button.click()
    # open new tab
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    # refreshes the page 
    browser.get('type the same url you entered earlier here')


def Credentials():
    USERNAME = input("Username: ")
    PASSWORD = getpass.getpass("Password: ")
    
    if USERNAME and PASSWORD:
        SiteLogin(USERNAME, PASSWORD)
    else:
        print("ERROR: There was an error with your credentials")

Credentials()
