# README.md

This project reads idealo urls and gets the amazon url, title and best seller rank. This will be checked for specific values and sent over telegram. (This was used until the client had an Amazon API key.)

## Installation

There should be a requirements.txt, you can install all dependencies with the command:

```bash
pip install -r requirements.txt
```

## Changes to make

All the files to scan should be in the folder the main.py is in + /input/. This can also be changed but is not necessary. All variables that can be changed in the main.py file:

```python
TOKEN = "" # Set to telegram bot token
CHAT_ID = "" # Set to the telegram chat ID
MIN_BEST_SELLER_RANK = 200000 # Set to the number the BSR should be below

# The directory is the location of main.py + /input/
PATH = os.path.dirname(os.path.realpath(__file__))+'/input/'
```

In get_bsr.py there is also 1 variable that can be changed. This is the amount of chrome windows that open to scan amazon. The number you choose is equal to the amount of ReCaptcha's you need to do:

```python
def extract_content(urls):
    """
    Every process will open a separate Chrome tab 
    This gives the question: "are you a robot", 
    change based on speed vs. ReCaptcha's
    """
    NUM_PROCESSES = 4
```

## Contact

For more information, contact me on [niek+git@meijlink5.nl](niek+git@meijlink5.nl) or <PHONE_NUMBER>. 

Made by: Niek M.