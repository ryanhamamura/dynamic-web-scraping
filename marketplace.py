from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
from pprint import pp

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)
    val = 'https://www.facebook.com/marketplace/honolulu/search/?query='
    keyword = input("Enter search marketplace search keyword: ")
    val = val + keyword
    driver.get(val)
    get_url = driver.current_url
    wait.until(EC.url_to_be(val))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sel = Selector(text=driver.page_source)
    # items = sel.xpath("//a[@role]//img[@alt]") 
    items = sel.xpath("//a[@role]//div//span//div//span[@class][@dir]")
    state = 'current_price'
    parsed = [{},]
    count = 0
    for item in items:
        text = item.css('span::text').get()
        # print(text)
    for item in items:
        text = item.css('span::text').get()
        # print(f'[DEBUG] text is {text}')
        if state == 'current_price':
            # print(f'[DEBUG] state is {state}')
            if len(parsed) <= count:
                parsed.append({})
            parsed[count]['current_price'] = text
            # print(f'[DEBUG] {listing}')
            state = 'previous_price'
        elif state == 'previous_price':
            # print(text[0])
            # print(f'[DEBUG] state is {state}')
            if text[0] == '$':
                parsed[count]['previous_price'] = text
                state = 'title'
            else:
                parsed[count]['title'] = text
                state = 'location'
            # print(f'[DEBUG] {listing}')
        elif state == 'title':
            # print(f'[DEBUG] state is {state}')
            parsed[count]['title'] = text
            # print(f'[DEBUG] {listing}')
            state = 'location'
        elif state == 'location':
            # print(f'[DEBUG] state is {state}')
            parsed[count]['location'] = text
            # print(f'[DEBUG] {listing}')
            state = 'current_price'
            count += 1
        else:
            print("undefined state") 
    pp(parsed)
    cont = input("Are you done? (y/n)")
    driver.quit()

if __name__ == "__main__":
    main()
