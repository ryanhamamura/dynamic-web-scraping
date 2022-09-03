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

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10)
    val = 'https://www.facebook.com/marketplace/honolulu/search/?query='
    keyword = input("Enter search marketplace search keyword: ")
    val = val + keyword + '&exact=false'
    driver.get(val)
    get_url = driver.current_url
    wait.until(EC.url_to_be(val))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    if get_url == val:
        # page_source = driver.page_source
        search = driver.find_elements(by=By.TAG_NAME, value='img')
        alts = driver.find_elements(by=By.TAG_NAME, value='img')
        alts = [alt.get_dom_attribute('alt') for alt in alts]
        for alt in alts:
            print(alt)
        driver.save_screenshot('search_results.png')
    cont = input("Are you done? (y/n)")
    driver.quit()

if __name__ == "__main__":
    main()
