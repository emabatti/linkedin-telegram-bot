import random
import time

def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.1 + 0.05 * random.random())  # Human-like delay

def human_sleep(seconds):
    time.sleep(seconds + random.uniform(1, 5))