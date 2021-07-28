import requests
from csv import writer
import json
from pprint import pprint
import wget
from datetime import datetime
import time
import html

# Configuration
header = {
    'X-RMAuth': '${XAUTH_KEY_FOR_NEWSGRAM_ENGLISH}', 
    'User-Agent': 'PostmanRuntime/7.28.0', 
    'Accept': '*/*', 
    'Cache-Control': 'no-cache', 
    'Postman-Token': '3381a69f-f418-41b3-89a4-33b1106fd976', 
    'Host': 'newsgram.rebelmouse.dev', 
    'Accept-Encoding': 'gzip%2C deflate%2C br', 
    'Connection': 'keep-alive',
    'Authorization': 'Basic bmV3c2dyYW06bmV3czIwMjE='
}

recieving_server = "https://newsgram.rebelmouse.dev/"
requesting_server = "https://www.newsgram.com/"
start = 1
end = 413

# Data Collection Point
returnData_404 = [0]
unverified = [0]

stat = [0, 0, 0]

def down():
    time.sleep(120)


def verify_upload(link):
    global header
    try:
        page = requests.get(link, headers=header)
    except: 
        x = input('Service Interrupted. Press Enter to continue: ')
        page = requests.get(link, headers=header)
    if (str(page) != "<Response [200]>" and str(page) != "<Response [404]>"):
        print("[PAUSED] Server Responded with " + str(page) + ". Retrying after 120 seconds")
        down()
        verify_upload(link)
    elif (len(json.loads(page.text)) == 0):
        print("[FAILED] " + str(json.loads(page.text)[0]['id']))
        return True
    else:
        print("[SUCCESS] " + str(json.loads(page.text)[0]['id']))
        return False


def run():
    for respond in range(start, end):
        x = input("Enter Slug: ")
        response = verify_upload("https://newsgram.rebelmouse.dev/api/1.3/posts/basename?basename={}".format(x))
        
run()
print("Failed\n")
print(returnData_404)
print("\n\nUnverified\n")
print(unverified)
