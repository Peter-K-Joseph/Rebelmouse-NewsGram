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
from colorama import Fore, Back, Style


header = {
    'X-RMAuth': 's9RD97sAtBlqdJtEGewCVITuC6lYUY06bbHL0o9pfkYeoJlPe6WdOA6QUeMS5LEl ', 
    'User-Agent': 'PostmanRuntime/7.28.2', 
    'Accept': '*/*', 
    'Cache-Control': 'no-cache', 
    'Postman-Token': '3381a69f-f418-41b3-89a4-33b1106fd976', 
    'Host': 'hindi-newsgram.rebelmouse.dev', 
    'Accept-Encoding': 'gzip%2C deflate%2C br', 
    'Connection': 'keep-alive'
}

# id_connect_old_to_new = []
id_connect_old_to_new = [[4406, 553712089], [19, 553712090], [18, 553712091], [20, 553712092], [98, 553712093], [4927, 553712094], [25, 553712095], [5078, 553712096], [23, 553712097], [27, 553712098], 
[26, 553712099], [17, 553712100], [24, 553712101], [5209, 553712102], [21, 553712103], [22, 553712104], [99, 553712105], [16, 553712106], [10481, 553712107], [10482, 553712108], [10483, 553712109]]
                    
requesting_server = "https://hindi.newsgram.com/wp-json/wp/v2"
recieving_server = "https://hindi-newsgram.rebelmouse.dev/api/1.3"

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Image Downloader
def ImageDownload(get):
    get = get.replace("https://i0.wp.com/", "")
    try:
        try:
            image = wget.download(get)
        except:
            print(Fore.YELLOW, "[ALERT] MEDIA OVERRIDE\n[ALERT] [OVERRIDE] Target Destination: " + get)
            print(Style.RESET_ALL)
            print(Fore.RED, "[ERROR] Error Downloading. Permission Denied by HOST Machine")
            print(Style.RESET_ALL)
        print(Fore.YELLOW, "\n[IMAGE] Image '" + image + "' was downloaded from " + get)
        print(Style.RESET_ALL)
        ext = image.split(".")
        ext = ext[-1]
        __temp = Image.open(image)
        width, height = __temp.size
        if (ext == "webp"):
            img = Image.open(image).convert('RGB')
            filename = randomword(25) + '.jpg'
            img.save(filename, 'jpeg')
            return filename
        elif (ext == "svg"):
            drawing = svg2rlg(image)
            filename = randomword(25) + '.png'
            renderPM.drawToFile(drawing, filename, fmt="PNG")
            return filename
        elif (width > 5000):
            im = Image.open(image)
            print(Fore.BLUE, "[IMAGINENGINE (IMAGE PROCESSOR)] Resizing Image")
            print(Style.RESET_ALL)
            try:
                im = im.resize((round(width*0.7), round(height*0.7)))
                im.show()
                print(Fore.BLUE, "[IMAGINENGINE (IMAGE PROCESSOR)] Image Resize operation complete")
                print(Style.RESET_ALL)
                filename = randomword(25) + '.jpg'
                im.save(filename, 'jpeg')
                return filename
            except:
                print(Fore.RED, "[ERROR REPORTING SERVICES] Image Resize operation failed!")
                print(Style.RESET_ALL)
                print(Fore.RED, "[ERROR REPORTING SERVICES] Returning Original Image Data")
                print(Style.RESET_ALL)
                return image
        else:
            return image
    except:
        print(Fore.YELLOW, "[ALERT] MEDIA OVERRIDE\n[ALERT] [OVERRIDE] Target Destination: " + get)
        print(Style.RESET_ALL)
        print(Fore.RED, "[ERROR REPORTING SERVICES] ImagesEngine Encountered an Error")
        print(Style.RESET_ALL)

#   Throttle Connection
no_requests = 0
def throttle():
    global no_requests
    no_requests = no_requests + 1
    if (no_requests == 125):
        print(Fore.WHITE, "\n\n\n[ALERT] Throttling Connection!!!\n\n\n")
        print(Style.RESET_ALL)
        time.sleep(40)
        no_requests = 0

def parse_text(content, tag):
    soup = BeautifulSoup(content, features="lxml")
    text = ""
    for x in soup.find_all(tag):
        if (x.getText() != ""):
            text = text + x.getText()

    return "<" + tag + ">" + text + "</" + tag + ">"
    

def find_subtitle(post_id):
    content = requests.get("https://hindi.newsgram.com/wp-json/wp/v2/posts/" + str(post_id))
    content = json.loads(content.text)
    content = requests.get(content['link'])
    content = content.text

    soup = BeautifulSoup(content, features="html.parser")
    text = ""
    tag = "td-post-sub-title"
    for x in soup.find_all("p", class_=tag):
        if (x.getText() != ""):
            text = text + x.getText()
    text = text.replace("\n", "", -1)
    return text

def getImagedetails(media_id):
    content = requests.get("https://hindi.newsgram.com/wp-json/wp/v2/media/" + str(media_id))
    content = json.loads(content.text)

    soup = BeautifulSoup(str(content["caption"]["rendered"]), features="html.parser")
    text = soup.getText()
    img_name = ImageDownload(content["guid"]["rendered"])
    
    return {
        'caption': text.replace("\n", "", -1),
        'alt': content["alt_text"],
        'name': img_name,
        'title': content["title"]["rendered"],
        'description': parse_text(str(content['description']['rendered']), 'p')
    }

def getTags(post_id):
    tags_parsed = []
    r = requests.get("https://hindi.newsgram.com/wp-json/wp/v2/tags?post={}".format(post_id))
    r = json.loads(r.text)
    for i in range(0, len(r)):
        tags_parsed.append(r[i]["name"])
        print(Fore.YELLOW, "[ALERT] TAG DETETCED. APPENDING TAG {} TO FILE".format(r[i]["name"]), Style.RESET_ALL)
    return tags_parsed
    

#HELPS KNOW CONNECTION STATUS
print(Fore.CYAN, "[START] Starting Transfer Sequence...\nChecking Connection...", Style.RESET_ALL)
print("[CONN_CHECK] Connection to NewsGram Services...", Style.RESET_ALL)
response = requests.get(requesting_server + '/posts')
if str(response) == '<Response [403]>' or str(response) == '<Response [500]>':
    print(Fore.RED, "[FAILURE] SERVER DENIED ACCESS", Style.RESET_ALL)
else:
    print(response)
    print(Fore.GREEN, "[CON_ACTIVE] AUTHORISED! Administrative Privilages Granted", Style.RESET_ALL)
    
print("[CON_CHECK] Connection to RebelMouse Services...", Style.RESET_ALL)
response = requests.get(recieving_server + '/posts', headers=header)
throttle()
if str(response) == '<Response [403]>' or str(response) == '<Response [404]>' or str(response) == '<Response [401]>':
    print(Fore.RED, "[FAILURE] SERVER DENIED ACCESS", Style.RESET_ALL)

else:
    print(response)
    print(Fore.GREEN, "[CON_ACTIVE] AUTHORISED! Administrative Privilages Granted", Style.RESET_ALL)

    
print("[SUCCESS] AUTH Success!", Style.RESET_ALL)

# Upload Categories as Sections
consent = input("[ALERT] Upload Category data? Press 1 if Yes: ")
if (consent == '1'):
    print(Fore.CYAN, "Staring Category Transfer")
    print(Style.RESET_ALL)
    page = requests.get(requesting_server + "/categories?per_page=100")
    page = json.loads(page.text)
    print("[NOTIFY] Parsed {} categories".format(len(page)), Style.RESET_ALL)
    for prop in range(0, len(page)):
        
        # Check if the category has a parent class. If yes, then skip
        if (page[prop]['parent'] == 0 and page[prop]['slug'] != 'uncategorized'):
            
            # Prepare JSON Data to be sent to recieving server. [MODIFY ACCORDINGLY]
            jsonData = {
                'title' : page[prop]['name'].replace("&amp;", "&"),
                'about_html' : page[prop]['description'],
                'url' : page[prop]['slug'],
                'status': 2
            }
            
            throttle()
            # Initiate Request to recieving server with auth
            r = requests.post(recieving_server + '/sections', headers=header, json=jsonData)
            print(str(r),Style.RESET_ALL)
            
            # Check Response. TRY => Upload | EXCEPT => Exists
            try:
                id_connect_old_to_new.append([page[prop]['id'], json.loads(r.text)['id']])
                print(Fore.BLUE, "Uploaded " + page[prop]['slug'], Style.RESET_ALL)
            except:
                print(Fore.YELLOW, "[ALERT] ERROR UPLOADING {}".format(page[prop]['name'].replace("&amp;", "&")), Style.RESET_ALL)
                continue

    # Now sending all those ones with a parent category
    page_newsgram_old = requests.get(requesting_server + "/categories?per_page=100")
    page_newsgram_old = json.loads(page_newsgram_old.text)
    for prop in range(0, len(page_newsgram_old)):
        if (page_newsgram_old[prop]['parent'] != 0):
            for prop_scan in range(0, len(id_connect_old_to_new)):
                if (page[prop]['parent'] == id_connect_old_to_new[prop_scan][0]):
                    
                    # Prepare JSON Data to be sent to recieving server. [MODIFY ACCORDINGLY]
                    jsonData = {
                        'parent_id' : id_connect_old_to_new[prop_scan][1],
                        'title' : page_newsgram_old[prop]['name'].replace("&amp;", "&"),
                        'about_html' : page_newsgram_old[prop]['description'],
                        'url' : page_newsgram_old[prop]['slug'],
                        'status': 2
                    }
                    
                    throttle()
                    
                    # Initiate Request to recieving server with auth
                    r = requests.post(recieving_server + '/sections', headers=header, json=jsonData)
                    
                    # Check Response. TRY => Upload | EXCEPT => Exists
                    try:
                        id_connect_old_to_new.append([page[prop]['id'], json.loads(r.text)['id']])
                        print(Fore.BLUE, "Uploaded " + jsonData["url"], Style.RESET_ALL)
                    except:
                        print(Fore.YELLOW, "[ALERT] ERROR UPLOADING {}".format(page[prop]['name'].replace("&amp;", "&")), Style.RESET_ALL)
                        continue
    print(id_connect_old_to_new, Style.RESET_ALL)
else:
    print(Fore.YELLOW, "Aborting Category Transfer")
                    
#________________________________________________________END OF CATEGORY___________________START OF POSTS_______________________________________________________

count = 0

for respond in range(1, 34):
    
    post_upload_session_data = []  
    # Send a requet to collect the data from POSTS API
    page = requests.get(requesting_server + "/posts/?page=" + str(respond) + "&per_page=100")
    print(Fore.BLUE, "[GET] A GET request was sent to " + requesting_server + "/posts/?page=" + str(respond) + "&per_page=100", Style.RESET_ALL)
    page = json.loads(page.text)
    
    # Get Features Media data and download it. Then Prepare to upload the data to server
    for prop in range(0, len(page)):
        # try:
            print(Fore.YELLOW, "[ALERT] STARTED TRANSFER OF {} OF {}".format(respond, prop), Style.RESET_ALL)
            print(Fore.BLUE, "[DEBUG] CURRENT SESSION TRANSFER OF {}".format(page[prop]["link"]), Style.RESET_ALL)
            # Will contain the Category ID of the recieving API Client for their respective ID in requested API
            temp = []
            
            # Gets the Cat ID
            for getIDOne in range(0, len(page[prop]['categories'])):
                for prop_scan in range(0, len(id_connect_old_to_new)):
                    if (page[prop]['categories'][getIDOne] == id_connect_old_to_new[prop_scan][0]):
                        temp.append(id_connect_old_to_new[prop_scan][1])
                        print("[ALERT] Category Information Added", Style.RESET_ALL)
            
            # Send a request to the requesting API to collect Featured Media info and then download them
            feature_data = getImagedetails(page[prop]['featured_media'])
            imageCaption = feature_data['caption']
            throttle()
            # Creates JSON File to be uploading to the recieving API. Modify accordingly
            create_media = {
                'file': open(feature_data['name'], 'rb'),
                'title': feature_data['title'],
                'description': feature_data["description"],
                'alt': feature_data["alt"],
                'caption': feature_data["caption"]
            }
            
            # Deploy Request to send the respective data to the recieving API
            try:
                r = requests.post(recieving_server + '/images', headers = header, files=create_media)
                print(Fore.BLUE, "[POST] REQUEST SENT TO " + recieving_server +  "/images. FEATURE IMAGE UPLOADED", Style.RESET_ALL)
                code = str(r)
                r = json.loads(r.text)
                post_upload_session_data.append({'feature_img': r["id"]})
            except:
                post_upload_session_data.append({'feature_img': 'false'})
                print(Fore.RED, "[ERROR] ERROR UPLOADING FEATURE_ID", Style.RESET_ALL)
                
            content = str(page[prop]['content']['rendered']).replace("\n", "").replace("""\\""","")
            
            soup = BeautifulSoup(content, features="lxml")
            print(Fore.BLUE, "[UPDATE] Images Parsed from HTML Page. System preparing to upload " + str(len(soup.find_all('figure'))) + " images", Style.RESET_ALL)
            if (len(soup.find_all('figure')) != 0):
                image_cap_track = 1
                for link in soup.find_all('figure'):
                    throttle()
                    image_identify = getImagedetails(link.find("img").get("class")[0].replace("wp-image-", ""))
                    print(Fore.BLUE, "[ALERT] [IMAGE] GETTING IMAGE ATTRIBUTED FROM IMG_ID {}".format(link.find("img").get("class")[0].replace("wp-image-", "")), Style.RESET_ALL)
                    
                    create_media = {
                        'file': open(image_identify["name"], 'rb'),
                        'alt': image_identify["alt"],
                        'caption': image_identify["caption"]
                    }
                    
                    link['style'] = ""
                    throttle()
                    try:
                        r = requests.post(recieving_server + '/images', headers = header, files=create_media)
                        code = str(r)
                        r = json.loads(r.text)
                        r = "<div style=\"width: 100%\"><center>" + r["shortcode"].replace("\n", "").replace("\\", "") + "</center><br><p style=\"color: grey;padding: 0;margin: 0;font-size: 1rem; text-align:right\">" + image_identify["caption"] + "</p></div>"
                        link.clear()
                        link.append(BeautifulSoup(r, 'html.parser'))
                        print(Fore.BLUE, "[NOTIFY] A Media file upload request was sent and the server returned a " + code, Style.RESET_ALL)
                    except:
                        print(Fore.RED, str(link.get("id")) + " enountered an error", Style.RESET_ALL)
                        continue
                        
                    print(Fore.BLUE, "[NOTIFY] All Images where uplaoded successfully!")
            content = str(soup).replace("<html><body>", "").replace("</body></html>", "").replace(u'\xa0', u' ')
            print(Fore.BLUE, "[NOTIFY] HTML Code prepared successfully. Preparing to upload POST")
            print(Style.RESET_ALL)
                        
            # Prepare JSON to be send to the recieving server
            dt_obj = datetime.strptime(str(page[prop]['date_gmt']).replace("T", " "), '%Y-%m-%d %H:%M:%S')
            dt_obj = int(dt_obj.timestamp())
            
            try:
                get_subtitle = find_subtitle(page[prop]['id'])
            except:
                get_subtitle = ""
            
            content = content.replace("https://hindi.newsgram.com/","https://hindi-newsgram.rebelmouse.dev/", -1)
            
            headline_set = str(page[prop]['title']['rendered'])
            slug = str(page[prop]['slug'])
            tags = getTags(page[prop]['id'])
                
            print("\n\n_______PARSED DATA________\n", Style.RESET_ALL)
            try:
                print(Fore.MAGENTA, "[ALERT] POST BREWED. PREPARING TO UPLOAD", Style.RESET_ALL)
            except:
                print(Fore.YELLOW, "[WARNING] EXCEPTION DETECTED: unknown", Style.RESET_ALL)
            try:
                print(Fore.LIGHTBLUE_EX, "[ALERT] HEADLINE: {}".format(headline_set), Style.RESET_ALL)
            except:
                print(Fore.YELLOW, "[WARNING] EXCEPTION DETECTED: headline", Style.RESET_ALL)
            try:
                print(Fore.LIGHTBLUE_EX, "[ALERT] CREATED TIMESTAMP: {}".format(dt_obj), Style.RESET_ALL)
            except:
                print(Fore.YELLOW, "[WARNING] EXCEPTION DETECTED: timestamp", Style.RESET_ALL)
            try:
                print(Fore.LIGHTBLUE_EX, "[ALERT] CREATED PAGE TITLE: {}".format(headline_set), Style.RESET_ALL)
            except:
                print(Fore.YELLOW, "[WARNING] EXCEPTION DETECTED: page title", Style.RESET_ALL)
            try:
                print(Fore.LIGHTBLUE_EX, "[ALERT] CREATED SECTION: {}".format(temp), Style.RESET_ALL)
            except:
                print(Fore.YELLOW, "[WARNING] EXCEPTION DETECTED: section", Style.RESET_ALL)
            try:
                print(Fore.LIGHTBLUE_EX, "[ALERT] CREATED SUB HEADLINE: {}".format(get_subtitle), Style.RESET_ALL)
            except:
                print(Fore.YELLOW, "[WARNING] EXCEPTION DETECTED: exception", Style.RESET_ALL)
            try:
                print(Fore.LIGHTBLUE_EX, "[ALERT] CREATED SLUG: {}".format(slug), Style.RESET_ALL)
            except:
                print(Fore.YELLOW, "[WARNING] EXCEPTION DETECTED: slug", Style.RESET_ALL)
            try:
                print(Fore.LIGHTBLUE_EX, "[ALERT] CREATED TAGS: {}".format(tags), Style.RESET_ALL)
            except:
                print(Fore.YELLOW, "[WARNING] EXCEPTION DETECTED: tags", Style.RESET_ALL)
            
            if (post_upload_session_data[0]["feature_img"] != 'false'):
                try:
                    post = {
                        "headline": headline_set,
                        "created_ts": dt_obj,
                        "page_title": headline_set,
                        "body": content,
                        "sections": temp,
                        'action': 'publish',
                        "image_id": post_upload_session_data[0]["feature_img"], 
                        'subheadline': get_subtitle,
                        'manual_basename': slug,
                        'tags': tags,
                        'photo_caption': imageCaption
                    }
                except:
                    print(Fore.RED, "[ERROR] EMERGENCY TERMINATION ON A FEATURED POST!", Style.RESET_ALL)
                    exit() 
            else:
                try:
                    print(Fore.YELLOW, "!>> [ERROR] EXCEPTION FOUND. NO FEATURE ID")
                    post = {
                        "headline": headline_set,
                        "created_ts": dt_obj,
                        "page_title": headline_set,
                        "body": content,
                        "sections": temp,   
                        'action': 'publish',
                        'subheadline': get_subtitle,
                        'manual_basename': slug,
                        'tags': tags
                    }
                except:
                    print(Fore.RED, "[ERROR] EMERGENCY TERMINATION ON A NON FEATURED POST!")
                    exit() 

            # Send the post data to the server
            throttle()
            # print(post)
            pprint(post)
            
            r = requests.post(recieving_server + '/posts?limit=1&offset=0&shortcodes_mode=feeds', headers=header, json=post)
            
			#Just a random counting thing.
            count = count + 1
            
            # Check the Response
            if (str(r) == "<Response [400]>" or str(r) == "<Response [429]>" or str(r) == "<Response [500]>"):
                print(Fore.YELLOW, "[WARNING] UPLOAD OF SELECT POST FAILED WITH {}. REUPLOADING IN RESTRICTED MODE".format(str(r)))
                r = requests.post(recieving_server + '/posts?limit=1&offset=0&shortcodes_mode=feeds', headers=header, json=post)
                
                # Retry is response is 400 or 429 or even 500
                if (str(r) == "<Response [400]>" or str(r) == "<Response [429]>" or str(r) == "<Response [500]>"):
                    print(Fore.RED, "[ERROR] FAILED TO UPLOAD POST. ABORTING TRANSFER" + str(r) , Style.RESET_ALL)
                    print(Fore.RED, "\n[NewsGram.com] xxxxxxxxxxxxxxx( FAILED )xxxxxxxxxxxxxxx [newsgram.rebelmouse.xyz]\n\tPost Name: " + page[prop]['title']['rendered'] + " [" +  str(count) + " of 40400]\n", Style.RESET_ALL)
                    
            elif (str(r) == "<Response [200]>"):
                
                # Hurray! Thats done
	            print(Fore.GREEN, "\n[NewsGram.com] ===============(100%)=============== [newsgram.rebelmouse.xyz]\n\tPost Name: " + page[prop]['title']['rendered'] + " [" +  str(count) + " of 40400]\n", Style.RESET_ALL)
                        
            else:
                try:
                    post = {
                            "headline": headline_set,
                            "created_ts": dt_obj,
                            "page_title": headline_set,
                            "body": content,
                            "sections": temp,   
                            "image_id": post_upload_session_data[0]["feature_img"],
                            'action': 'publish',
                            'manual_basename': slug,
                            'tags': tags
                    }
                except: 
                    try: 
                        post = {
                                "headline": headline_set,
                                "created_ts": dt_obj,
                                "page_title": headline_set,
                                "body": content,
                                "sections": temp,
                                'action': 'publish',
                                'manual_basename': slug,
                                'tags': tags
                        }
                    except:
                        post = {
                            "headline": headline_set,
                            "created_ts": dt_obj,
                            "page_title": headline_set,
                            "body": content,
                            "sections": temp,
                            'action': 'publish',
                            'manual_basename': slug
                        }

                r = requests.post(recieving_server + '/posts?limit=1&offset=0&shortcodes_mode=feeds', headers=header, json=post)
                print(Fore.YELLOW, "\n\n[WARNING] Unable to Verify Upload status. Server responded with code " + str(r) + "\nLoggerMod\n" + str(r.text), Style.RESET_ALL)
                if (str(r) == "<Response [400]>" or str(r) == "<Response [429]>" or str(r) == "<Response [500]>"):
                    print(Fore.GREEN, "\n[NewsGram.com] ===============(100%)=============== [newsgram.rebelmouse.xyz]\n\tPost Name: " + page[prop]['title']['rendered'] + " [" +  str(count) + " of 40400]\n", Style.RESET_ALL)
                elif (str(r) == "<Response [400]>" or str(r) == "<Response [429]>" or str(r) == "<Response [500]>"):
                    print(Fore.RED, "\n[NewsGram.com] ===============( FAILED )=============== [newsgram.rebelmouse.xyz]\n\tPost Name: " + page[prop]['title']['rendered'] + " [" +  str(count) + " of 40400]\n", Style.RESET_ALL)
                else:
                    print(Fore.YELLOW, "\n[NewsGram.com] xxxxxxxxxxxxxxx( "+str(r)+" )xxxxxxxxxxxxxxx [newsgram.rebelmouse.xyz]\n\tPost Name: " + page[prop]['title']['rendered'] + " [" +  str(count) + " of 40400]\n", Style.RESET_ALL)
        
        # except:
        #     print(Fore.RED, "\n\n\nERROR!\n[FATAL ERROR] Failed to upload Page: " + str(respond) + ", Prop: " + str(prop) + "\n\nResuming\n\n\n" )
        #     with open('failed.csv', 'w', newline='',  encoding='utf-8') as file:
        #         writer = csv.writer(file)
        #         writer.writerows([str(respond), str(prop)])