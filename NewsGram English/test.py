import requests
from bs4 import BeautifulSoup
import csv
import json
from pprint import pprint
import wget
from datetime import datetime
import time
import random, string
from PIL import Image
import re

def find_subtitle(link):
    content = requests.get("https://www.newsgram.com/wp-json/wp/v2/posts/" + str(link))
    content = json.loads(content.text)
    content = requests.get(content['link'])
    content = content.text

    soup = BeautifulSoup(content, features="html.parser")
    text = "" 
    tag = "td-post-sub-title"
    for x in soup.find_all("p", class_= tag):
        if (x.getText() != ""):
            text = text + x.getText()
    text = text.replace("\n", "", -1)
    print(text)
    return text

find_subtitle(294869)