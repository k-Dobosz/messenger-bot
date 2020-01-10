#!/usr/bin/env python
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from python_json_config import ConfigBuilder
import chromedriver_binary
import getopt
import logging
import sys
import time

builder = ConfigBuilder()
config = builder.parse_config('config.json')

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
logs = logging.FileHandler('logs.log')
logs.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logs.setFormatter(formatter)
logger.addHandler(logs)


def main():
    show_browser = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvs", ["help", "showbrowser"])
    except getopt.GetoptError as err:
        print(err)
    for o,a in opts:
        if o == '-v':
            logging.getLogger(__name__).setLevel(logging.DEBUG)
        elif o in ('-h', '--help'):
            sys.exit()
        elif o in ('-s', '--showbrowser'):
            show_browser = True
        else:
            assert False, 'Unhandled option'

    chrome_options = Options()

    if not show_browser:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920x1080')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(config.url)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))
        email = driver.find_element_by_xpath('//*[@id="email"]')
        email.send_keys(config.account.email)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pass"]')))
        passwd = driver.find_element_by_xpath('//*[@id="pass"]')
        passwd.send_keys(config.account.password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginbutton"]')))
        submit = driver.find_element_by_xpath('//*[@id="loginbutton"]')
        submit.click()

        while True:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_aok _7i2m"]')))
            message = driver.find_elements_by_xpath("//div[@class='_aok _7i2m']")[-1].text.lower()
            if message == '!all':
                try:
                    message_box = driver.switch_to.active_element
                    for person in config.lists.all:
                        message_box.send_keys('@' + person)
                        time.sleep(0.035)
                        message_box.send_keys(Keys.TAB)
                        message_box.send_keys(Keys.SPACE)
                finally:
                    message_box.send_keys(Keys.ENTER)

                logger.info(message)
            elif message == '!boys':
                try:
                    message_box = driver.switch_to.active_element
                    for person in config.lists.boys:
                        message_box.send_keys('@' + person)
                        time.sleep(0.035)
                        message_box.send_keys(Keys.TAB)
                        message_box.send_keys(Keys.SPACE)
                finally:
                    message_box.send_keys(Keys.ENTER)

                logger.info(message)
            elif message == '!girls':
                try:
                    message_box = driver.switch_to.active_element
                    for person in config.lists.girls:
                        message_box.send_keys('@' + person)
                        time.sleep(0.035)
                        message_box.send_keys(Keys.TAB)
                        message_box.send_keys(Keys.SPACE)
                finally:
                    message_box.send_keys(Keys.ENTER)

                logger.info(message.text)
            elif message == '!help':
                message_box = driver.switch_to.active_element
                message_box.send_keys('Available commands:')

                for command in config.commands:
                    message_box.send_keys(Keys.CONTROL + Keys.ENTER)
                    message_box.send_keys(command)

                message_box.send_keys(Keys.ENTER)
            else:
                logger.info('message')

            time.sleep(1)
    except NoSuchElementException:
        logger.error('Element not found')


if __name__ == "__main__":
    main()