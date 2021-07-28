#!python
# vim: set fileencoding=UTF-8 :

import requests
from bs4 import BeautifulSoup
import csv
import json
from pprint import pprint
import wget
from datetime import datetime
import time
import random
import string
from PIL import Image
import re
import html
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

def getImagedetails(media_id):
    content = requests.get("https://hindi.newsgram.com/wp-json/wp/v2/media/" + str(media_id))
    content = json.loads(content.text)

    soup = BeautifulSoup(content["caption"]["rendered"], features="html.parser")
    text = soup.getText()
    return [text.replace("\n", "", -1), content["alt_text"]]
    
print(getImageSubs(37043))