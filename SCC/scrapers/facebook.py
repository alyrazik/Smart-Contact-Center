import pandas as pd
from facebook_scraper import get_posts
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import time


def get_fb_posts(group, pages):
    posts = []
    for post in get_posts(group=group, pages=pages):  # group ID for don't shop here group
        posts.append(post)
    return posts


def get_fb_profile(path_to_web_driver, user_name, pw, profile_page):
    """
    1. Open Chrome driver.
    2. Open Facebook.com
    3. Enter user name and password.
    4. Enter the user's profile URL.
    5. Click on "About".
    6. Click on "Contact and Basic Info".
    7. Return the target information.
    :rtype: object
    """

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--incognito")
    driver = webdriver.Chrome(path_to_web_driver)
    driver.implicitly_wait(4)  # seconds
    driver.maximize_window()  # For maximizing window

    # Open Facebook
    driver.get("https://facebook.com")

    # Login to get more data
    # Find user name xpath
    userName = driver.find_element_by_xpath('//*[@id="email"]')
    # Enter user name
    userName.send_keys(user_name)
    # Find password xpath
    password = driver.find_element_by_xpath('//*[@id="pass"]')
    # Enter password
    password.send_keys(pw)
    # Find login button xpath
    login = driver.find_element_by_xpath('//*[@id="u_0_b"]')
    # Press login
    login.click()
    # Add delay to get time for loading the profile
    time.sleep(2)
    # Open the user's profile
    driver.get(profile_page)

    # Get "About" tab xpath and click on it
    while True:
        try:
            About = driver.find_element_by_xpath(
                '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/div/a[2]/div[1]/span'
            )
            About.click()
        except Exception:
            continue  # If StaleElement appears, try again
        break  # once try is successful, stop while loop

    # Get "Contact and Basic Info" tab xpath and click on it
    while True:
        try:
            Contact_and_Basic_Info = driver.find_element_by_xpath(
                '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[1]/div[5]/a/span'
            )
            Contact_and_Basic_Info.click()
        except Exception:
            continue
        break

    # Get Gender tab xpath and return value
    while True:
        try:
            Gender = driver.find_element_by_xpath(
                '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div[2]/div/div/div[3]/div[5]/div/div/div[1]/div/div[2]/div/div[1]/div/div/div[1]/span'
            )
        except Exception:
            continue
        break

    user_info = [Gender.text]
    return user_info
