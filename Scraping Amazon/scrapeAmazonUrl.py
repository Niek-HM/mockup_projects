import requests
from bs4 import BeautifulSoup

import timeout_decorator

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

# If it is still not finished after 30 seconds it will throw an error and quit
@timeout_decorator.timeout(30)
def get_amazon_url(url, actual_url):
    # Default headers which allow it to get past idealo's anti-bot protection
    headers = ({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)  AppleWebKit/537.36 (KHTML, like Gecko)  Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.bauhof.ee/et/tooriistad',

        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'authority': 'https://www.bauhof.ee/et/tooriistad',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    })

    # Request the html page from idealo
    response = requests.get(url, headers=headers)

    # Exit if the page did not load correctly
    if not response.status_code == 200:
        print("Failed to fetch the idealo page.")
        return

    # Make the response readable html
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the amazon image since it is the most clear way to find the redirect URL
    try: links = soup.find(
        'img',
        class_="productOffers-listItemOfferShopV2LogoImage",
        alt=lambda alt_text: alt_text and 'Amazon' in alt_text
    ).parent.parent.parent.parent.parent.find_all('a', href=True)

    except AttributeError:
        """ 
        If we can't find it then that means it is to low on the list.
        So we open selenium to open a window and press the "more" button 
        (not visible because of --headless)
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headless to hide the browser window
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        driver.get(url)
        try:
            driver.find_element(By.CLASS_NAME, "productOffers-listLoadMore button-ghost button-ghost--blue").click()

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            links = soup.find(
                'img',
                alt=lambda alt_text: alt_text and 'Amazon' in alt_text
            ).parent.parent.parent.parent.parent.find_all('a', href=True)

        # If we still can't find it then it will probably not exist or we are on the wrong page
        except (AttributeError, NoSuchElementException): links = []

        # Close the Chrome window
        driver.quit()

    # Get the title of the product
    try: title = ''.join([child.text for child in soup.find('h1', class_="oopStage-title").find_all()])
    except AttributeError:
        print("NO TITLE FOUND FOR: ", url)
        title = ''

    # Filter links that contain Amazon keywords
    for link in links:
        # Get the href
        url = link.get("href", "")

        # Check if it is a relocator
        if url.startswith("/relocator/"):
            # Print the URL it found to show progress
            data = requests.get('https://www.idealo.de/'+url, headers=headers)

            # Get the actual amazon url to make sure no other ones are accedently appended
            if data.status_code == 200 and 'amazon' in data.url and data.url not in actual_url:
                print(url)
                actual_url.append([data.url, title])