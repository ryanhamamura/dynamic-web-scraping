from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    val = input("Enter a url: ")
    wait = WebDriverWait(driver, 10)
    driver.get(val)
    get_url = driver.current_url
    wait.until(EC.url_to_be(val))
    if get_url == val:
        page_source = driver.page_source

if __name__ == "__main__":
    main()
