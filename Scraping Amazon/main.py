import os
import telebot
import multiprocessing
import timeout_decorator
import time

from scrapeAmazonUrl import get_amazon_url
from get_bsr import extract_content

TOKEN = "TELEGRAM_TOKEN" # Set to telegram bot token
CHAT_ID = "TELEGRAM_CHAT_ID" # Set to the telegram chat ID
MIN_BEST_SELLER_RANK = 0 # Set to the number the BSR should be below

PATH = '/input/' # The directory it will look for .txt files (Directory has to be in the same folder as this file)
PATH = os.path.dirname(os.path.realpath(__file__)) + PATH
os.chdir(PATH)

if TOKEN == "TELEGRAM_TOKEN": TOKEN = input("No telegram bot token provided, please provide one: ")
if TOKEN == "TELEGRAM_CHAT_ID": CHAT_ID = input("No telegram chat id provided, please provide one: ")

print("Currently the PATH variable is set to: ", PATH)
print("And products will only be selected with a BSR below: ", MIN_BEST_SELLER_RANK)

# Loop through the directory and open every text file
urls = []
for file in os.listdir():
    if file.endswith(".txt"):
        # Get path to .txt file
        file_path = f"{PATH}{file}"

        # Open file and append every line as a different URL
        with open(file_path, 'r') as f: [urls.append(line.strip()) for line in f.readlines()]

# Only run when this file is run and not when called (REQUIRED BY MULTIPROCESSING)
if __name__ == '__main__':
    # Setup a list that can be used over multiple processes
    manager = multiprocessing.Manager()
    actual_urls = manager.list()

    # Get the maximum amount of processes that can be run net to each other without bottlenecks
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)

    # Make a list with seperate urls for every process
    input_ = []
    [input_.append((url, actual_urls)) for url in urls]

    # Run url seperate and wait for every process to finish (There is a timeout after 5 seconds)
    try: pool.starmap(get_amazon_url, input_)
    except timeout_decorator.TimeoutError as e: print(f"Function with URL={e} timed out.")

    finally:
        # Wait for all processes to finish
        pool.close()
        pool.join()

    # Make the multiprocess list into a normal python list
    actual_urls_list = list(actual_urls)

    # Double check that there are no duplicates
    actual_urls = []
    for item in actual_urls_list:
        if item not in actual_urls:
            actual_urls.append(item)

    print(len(actual_urls))

    # Get the separate products from every url and put them in one list instead of separate ones
    products = extract_content(actual_urls)

    list_products = []
    for product_list in products: [list_products.append(item) for item in product_list]

    # Start the Telegram bot
    bot = telebot.TeleBot(TOKEN)

    # Sends all the messages to the specified channel
    limiter = 1
    for product in list_products:
        # If BSR is not None and lower than the minimum it sends the message
        if product[1]:
            if int(product[1]) < MIN_BEST_SELLER_RANK:
                message = "Best Seller Rank: " + product[1] + "\nName: " + product[0][1] + "\n\n" + product[0][0]
                bot.send_message(CHAT_ID, message)

                # This is to not go over the maximum amount of messages (20msg/minute) for a group.
                limiter += 1
                if limiter >= 20:
                    time.sleep(60)
                    limiter = 0