import time
import pandas as pd
import selenium.common.exceptions
from bs4 import BeautifulSoup
from selenium import webdriver
pd.options.mode.chained_assignment = None
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import multiprocessing
import math

def extract_content(urls):
    """
    Every process will open a separate Chrome tab
    This gives the question: "are you a robot",
    change based on speed vs. ReCaptcha's
    """
    NUM_PROCESSES = 4

    # Split urls into multiple lists (based on amount of processes)
    batch_size = math.ceil(len(urls)/NUM_PROCESSES)
    batches = [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]

    # Setup amount of processes and run them
    pool = multiprocessing.Pool(processes=NUM_PROCESSES)
    list_products = pool.map(main, batches)

    # Wait for all processes to finish
    pool.close()
    pool.join()

    return list_products

def main(urls):
    # Setup the driver and make a list to store all valid products in (url, BSR)
    products = []
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Loop through every URL
    for url in urls:
        # Open the URL
        driver.get(url[0])

        # Wait until ReCaptcha is solved
        while 'To discuss automated access to Amazon data please contact api-services-support@amazon.com.' in driver.page_source: time.sleep(1)

        # Control+F To load the BSR rank so we can scrape it
        load_bsr(driver)

        # Make the page readable/editable
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find a object that gets it closed to the actual BSR rank
        rank_span = soup.find('span', text=re.compile(r'Best Sellers Rank'))

        if not rank_span or rank_span == None or rank_span.text.lower() == '':
            try: rank_span = soup.find('th', text=' Best Sellers Rank ')
            except AttributeError as e: rank_span = ''

        # Get to the area from where it is actualy visable (if it would be printed)
        try: rank_text = rank_span.find_next_sibling().parent.text.strip()
        except Exception: rank_text = ''

        # Use re to find for a pattern that looks like a bsr number
        match = re.search(r'([\d,]+)', rank_text)

        if match: rank_number = match.group(1).replace(',', '')
        else:
            rank_number = None
            print("NO BSR FOUND: ", url)

        # Append the url together with the BSR to products
        products.append([url, rank_number])

    # Close the Chrome window and return products
    driver.quit()
    return products

def load_bsr(driver):
    # Simulate Control+F input
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 'f')

    # Switch to the find input field
    find_input = driver.switch_to.active_element

    # Enter the text to search for
    find_input.send_keys("Best Sellers Rank")

    # Simulate pressing Enter to start the search
    find_input.send_keys(Keys.RETURN)

    # Wait until the BSR is loaded, just continue if it is still not here after 4 seconds
    try:
        WebDriverWait(driver, 4).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*'),
                text_='Best Sellers Rank'
            )
        )
    except selenium.common.exceptions.TimeoutException: pass