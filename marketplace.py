from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from parsel import Selector
from pprint import pp
import sqlite3
import datetime

def main():
   # Chrome Driver options
    options = Options()
    options.headless = True  # hide GUI
    options.add_argument('--window-size=1920,1080')  # set window size
    options.add_argument('start-maximized')  # ensure window is maximized
    # Start Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    val = 'https://www.facebook.com/marketplace/honolulu/search/?query='
    keyword = input("Enter search marketplace search keyword: ")
    val = val + keyword
    driver.get(val)
    get_url = driver.current_url
    wait.until(EC.url_to_be(val))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sel = Selector(text=driver.page_source)
    items = sel.xpath("//a[@role]//div//span//div//span[@class][@dir]")
    state = 'current_price'
    parsed = [{
        'title': '',
        'current_price': '',
        'previous_price': '',
        'location': '',
        'listing_date': '',
    },]
    count = 0
    for item in items:
        text = item.css('span::text').get()
        # print(f'[DEBUG] text is {text}')
        if state == 'current_price':
            # print(f'[DEBUG] state is {state}')
            if len(parsed) <= count:
                parsed.append({
                    'title': '',
                    'current_price': '',
                    'previous_price': '',
                    'location': '',
                    'listing_date': '',
                })
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
            parsed[count]['listing_date'] = datetime.date.today()
            # print(f'[DEBUG] {listing}')
            state = 'current_price'
            try:
                # database connection
                con = sqlite3.connect('marketplace.db')
                with con:
                    cur = con.execute("UPDATE listings SET current_price = :current_price, previous_price = :previous_price WHERE title = :title AND location = :location", parsed[count])
                    print(f'[DEBUG] cur.rowcount is {cur.rowcount}')
                    if cur.rowcount == 0:
                        con.execute("INSERT INTO listings VALUES(:title, :current_price, :previous_price, :location, :listing_date)", parsed[count])
                        pp(f'[DEBUG] New row added: {parsed[count]}', indent=4)   
                    con.commit()
            except sqlite3.IntegrityError:
                print("couldn't add values twice")
            count += 1
        else:
            print("undefined state") 
    # pp(parsed, indent=4)
    con.close()
    driver.quit()

if __name__ == "__main__":
    main()
