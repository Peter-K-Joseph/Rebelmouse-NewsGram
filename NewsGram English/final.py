# PROCEED WITH CAUTION. I, Peter will not be held responsible if this code isnt working
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
import html

header = {
    'X-RMAuth': 'KlCym4YdO1BQrvAWjNkuHBPhaw5OxkS4wENNlQbaKCEhqOpxyewBWVzV4479IpDm', 
    'User-Agent': 'PostmanRuntime/7.28.0', 
    'Accept': '*/*', 
    'Cache-Control': 'no-cache', 
    'Postman-Token': '3381a69f-f418-41b3-89a4-33b1106fd976', 
    'Host': 'newsgram.rebelmouse.dev', 
    'Accept-Encoding': 'gzip%2C deflate%2C br', 
    'Connection': 'keep-alive',
    'Authorization': 'Basic bmV3c2dyYW06bmV3czIwMjE='
    }

# id_connect_old_to_new = []
id_connect_old_to_new = [[64, 552299877], [49578, 552299878], [40275, 552299879], [60502, 552299880], [54639, 552299881], [60256, 552299882], [60503, 552299883], [9, 552299884], [60505, 552299885], [3296, 552299886], [39673, 552299887], [37, 552299888], [41626, 552299889], [60501, 552299890], [41989, 552299891], [6, 552299892], [21127, 552299893], [5, 552299894], [19043, 552299895], [11, 552299896], [41779, 552299897], [60461, 552299898], [19302, 552299899], [7, 552299900], [60504, 552299901], [42415, 552299902], [42225, 552299903], [53347, 552299904], [8, 552299905], [38915, 552299906], [42506, 552299907], [41981, 552299908]]
              
response_log = [["Response Code", "Server URI", "Endpoint" , "Request Sent", "Response Recieved"]]
                    
recieving_server = "https://newsgram.rebelmouse.dev/api/1.3"
requesting_server = "https://www.newsgram.com/wp-json/wp/v2"

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Image Downloader
def ImageDownload(get):
    try: 
        ext = get.split(".")
        ext = ext[-1]
        image = wget.download(get, randomword(25) + '.' + ext)
        print("\n[IMAGE] Image '" + image + "' was downloaded")
    except:
        time.sleep(10)
        ImageDownload(get)
    return image

#   Throttle Connection
no_requests = 0
def throttle():
    global no_requests
    no_requests = no_requests + 1
    if (no_requests == 20):
        print("\n\n\nThrottling Connection!!!\n\n\n")
        time.sleep(0)
        no_requests = 0

def parse_text(content, tag):
    soup = BeautifulSoup(content, features="lxml")
    text = "" 
    for x in soup.find_all(tag):
        if (x.getText() != ""):
            text = text + x.getText()
            
    return "<" + tag + ">" + text + "</" + tag + ">"
    

def find_subtitle(link):
    content = requests.get("https://www.newsgram.com/wp-json/wp/v2/posts/" + str(link))
    content = json.loads(content.text)
    content = requests.get(content['link'])
    content = content.text

    soup = BeautifulSoup(content, features="html.parser")
    text = "" 
    tag = "tdb_single_subtitle"
    for x in soup.find_all("p", class_= tag):
        if (x.getText() != ""):
            text = text + x.getText()
    text = text.replace("\n", "", -1)
    return text

def getImageSubs(link):
    content = requests.get("https://www.newsgram.com/wp-json/wp/v2/posts/" + str(link))
    content = json.loads(content.text)
    content = requests.get(content['link'])
    content = content.text

    soup = BeautifulSoup(content, features="html.parser")
    text = []
    tag = "figcaption" 
    for x in soup.find_all(tag):
        if (x.getText() != ""):
            text.append(x.getText())
    
    return text

def getTags(link):
    tags = []
    content = requests.get(str(link))
    content = json.loads(content.text)
    for prop in range(0, len(content)):
        tags.append(content[prop]["name"])
        
    return tags

# Error Reporting Template
def errorReportingServices(line, text, requestSent, ResponseRecieved):
    print("\n\n\n\n")
    print("ERROR REPORTING SERVICES")
    print("_______________________")
    print("Error State\n\tOrigin: " + str(line) + "\n\tPossible Cause: " + text)
    print("\n\tRequest")
    pprint(requestSent)
    print("\n\n\n\tResponse")
    pprint(ResponseRecieved)    
    try:
        f = open("error service\\s " + str(random.randint(1,9500)*5) + ".txt", "x")
        f.write("nuvie Post Transfer Services\n\nAn Error Occurred at line " + str(line) + " which caused the code to terminate. Possible cause for the error can be " + text + "\n\n\nDiagnostic Information\n\nRequest Sent\n__________________________\n\n" + str(requestSent) + "\n\n\nResponse Recieved\n_________________________________\n\n" + str(ResponseRecieved))
        f.close()
    except:
        print("Error Exporting Data")

#HELPS KNOW CONNECTION STATUS
print("Starting Transfer Sequence...\n\nChecking Connection...")
print("Connection to NewsGram Services...")
response = requests.get(requesting_server + '/posts')
if str(response) == '<Response [403]>' or str(response) == '<Response [500]>':
    errorReportingServices(51, "Server Authentication Failed to NewsGram", str(response), response.text)
else:
    print(response)
    print("AUTHORISED! Administrative Privilages Granted")
    
print("\n\nConnection to RebelMouse Services...")
response = requests.get(recieving_server + '/posts', headers=header)
throttle()
if str(response) == '<Response [403]>' or str(response) == '<Response [404]>' or str(response) == '<Response [401]>':
    errorReportingServices(51, "Server Authentication Failed to RebelMouse", str(response), response.text)
else:
    print(response)
    print("AUTHORISED! Administrative Privilages Granted")
    
print("AUTH Success!")

# Upload Categories as Sections
consent = input("Upload Category data? Press 1 if Yes: ")
if (consent == '1'):
    print("Staring Category Transfer")
    page = requests.get(requesting_server + "/categories?per_page=100")
    response_log.append([str(page), requesting_server, "categories", "[GET] => " + requesting_server + "/categories?per_page=100", str(page.text)])
    page = json.loads(page.text)
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
            
            # Check Response. TRY => Upload | EXCEPT => Exists
            try:
                id_connect_old_to_new.append([page[prop]['id'], json.loads(r.text)['id']])
                print("Uploaded " + jsonData["url"])
            except:
                errorReportingServices(101, "Appending the ID of the Category on an existing category is impossible", jsonData, r.text)
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
                        print("Uploaded " + jsonData["url"])
                    except:
                        errorReportingServices(130, "Appending the ID of the Category on an existing category is impossible", jsonData, r.text)
    print(id_connect_old_to_new)
else:
    print("Aborting Category Transfer")
                    
#________________________________________________________END OF CATEGORY___________________START OF POSTS_______________________________________________________

count = 0

for respond in range(1, 2):
    
    # Send a requet to collect the data from POSTS API
    # 406 IN THE FOR LOOP WAS TESTED AND WRITTEN
    
    # LAST KNOWN CHECK IS 274 414 => 84
    
    page = requests.get(requesting_server + "/posts/?page=" + str(respond) + "&per_page=100")
    response_log.append([str(page), requesting_server, "posts", requesting_server + "/posts/?page=" + str(respond) + "&per_page=100", "Too Many Data"])
    print("[GET] A GET request was sent to " + requesting_server + "/posts/?page=" + str(respond) + "&per_page=100")
    page = json.loads(page.text)
    
    # Get Features Media data and download it. Then Prepare to upload the data to server
    for prop in range(5, 16):
        try:
            # Will contain the Category ID of the recieving API Client for their respective ID in requested API
            temp = []
            
            # Gets the Cat ID
            for getIDOne in range(0, len(page[prop]['categories'])):
                for prop_scan in range(0, len(id_connect_old_to_new)):
                    if (page[prop]['categories'][getIDOne] == id_connect_old_to_new[prop_scan][0]):
                        temp.append(id_connect_old_to_new[prop_scan][1])
                        print("Category Information Added")
            
            # Send a request to the requesting API to collect Featured Media info and then download them
            r = requests.get(requesting_server + '/media/' + str(page[prop]['featured_media']))
            response_log.append([str(r), requesting_server, "media", "[GET] => " + requesting_server + '/media/' + str(page[prop]['featured_media']), str(json.loads(r.text))])
            r = json.loads(r.text)
            
            accessTags = getTags(page[prop]['_links']['wp:term'][1]['href'])
            imageCaption = getImageSubs(page[prop]['id'])
            
            throttle()
            image = ImageDownload(str(r['guid']['rendered']))
            
            img = Image.open("./" + image)
  
            # get width and height
            width = img.width
            height = img.height

            # Creates JSON File to be uploading to the recieving API. Modify accordingly
            create_media = {
                'file': open(image, 'rb'),
                'title': r['title']['rendered'],
                'description': parse_text(str(r['description']['rendered']), 'p'),
                'alt': r['alt_text'],
                'caption': r['caption']['rendered']
            }
            
            # Deploy Request to send the respective data to the recieving API
            try:
                r = requests.post(recieving_server + '/images', headers = header, files=create_media)
                response_log.append([str(r), recieving_server, "images", "[POST] => " + str(create_media), str(r.text)])
                print("[POST] Post request sent to " + recieving_server +  "/images. Feature Image Uplaoding")
                code = str(r)
                r = json.loads(r.text)
                f_id = r["id"]
            except:
                errorReportingServices(219, "Error occurred while uploading lead media to " + recieving_server, create_media, r.text)
                response_log.append([code, recieving_server, "images", "[POST] => " + str(create_media), str(r)])
                continue
                
            content = str(page[prop]['content']['rendered']).replace("\n", "")
            content = content.replace("""\\""","")
            
            soup = BeautifulSoup(content, features="lxml")
            print("[UPDATE] Images Parsed from HTML Page. System preparing to upload " + str(len(soup.find_all('figure'))) + " images")
            if (len(soup.find_all('figure')) != 0):
                image_cap_track = 1
                for link in soup.find_all('figure'):
                    throttle()
                    r = requests.get(requesting_server + "/media/" + link.get("id").replace("attachment_", ""))
                    r = json.loads(r.text)
                    name = ImageDownload(r["guid"]["rendered"])
                    
                    create_media = {
                        'file': open(name, 'rb'),
                        'title': r['title']['rendered'],
                        'alt': parse_text(r['alt_text'], "p"),
                        'caption': parse_text(r['caption']['rendered'], 'p')
                    }
                    
                    link['style'] = ""

                    throttle()
                    try:
                        r = requests.post(recieving_server + '/images', headers = header, files=create_media)
                        code = str(r)
                        response_log.append([code, recieving_server, "images", "[POST] => " + str(create_media), str(r.text)])
                        r = json.loads(r.text)
                        if (len(soup.find_all('figure')) == len(imageCaption)-1):
                            r = "<div style=\"width: 100%\"><center>" + r["shortcode"].replace("\n", "").replace("\\", "") + "</center><br><p style=\"color: grey;padding: 0;margin: 0;font-size: 1rem; text-align:right\">" + imageCaption[image_cap_track] + "</p></div>"
                        else:
                            r = "<div style=\"width: 100%\"><center>" + r["shortcode"].replace("\n", "").replace("\\", "") + "</center><br></div>"
                        image_cap_track = image_cap_track + 1
                        link.clear()
                        link.append(BeautifulSoup(r, 'html.parser'))
                        print("[NOTIFY] A Media file upload request was sent and the server returned a " + code)
                    except:
                        print(str(link.get("id")) + " enountered an error")
                        errorReportingServices(67, "An error occurred while replacing images" , create_media, r.text)
                        response_log.append([code, recieving_server, "images", "[POST] => " + str(create_media), str(r.text)])
                        continue
                        
                    print("[NOTIFY] All Images where uplaoded successfully!")
            content = str(soup).replace("<html><body>", "").replace("</body></html>", "").replace(u'\xa0', u' ')
            print("[NOTIFY] HTML Code prepared successfully. Preparing to upload POST")
                        
            # Prepare JSON to be send to the recieving server
            dt_obj = datetime.strptime(str(page[prop]['date_gmt']).replace("T", " "), '%Y-%m-%d %H:%M:%S')
            dt_obj = int(dt_obj.timestamp())
            try:
                get_subtitle = find_subtitle(page[prop]['id'])
            except:
                get_subtitle = ""
            
            content = content.replace("https://www.newsgram.com/","https://newsgram.rebelmouse.dev/", -1)
            
            try:
                try: 
                    post = {
                        "headline": html.unescape(page[prop]["title"]["rendered"]),
                        "created_ts": dt_obj,
                        "page_title": html.unescape(page[prop]["title"]["rendered"]),
                        "body": content,
                        "sections": temp,
                        'action': 'publish',
                        "image_id": f_id,
                        'image_size': '{}x{}'.format(width, height),
                        'subheadline': get_subtitle,
                        'manual_basename': str(page[prop]['slug']),
                        'type': 'page',
                        'tags': accessTags,
                        'photo_caption': imageCaption[0]
                    }
                except:
                    print("!>> [ERROR] EXCEPTION FOUND. NO FEATURE ID")
                    post = {
                        "headline": html.unescape(page[prop]["title"]["rendered"]),
                        "created_ts": dt_obj,
                        "page_title": html.unescape(page[prop]["title"]["rendered"]),
                        "body": content,
                        "sections": temp,   
                        'action': 'publish',
                        'subheadline': get_subtitle,
                        'manual_basename': str(page[prop]['slug']),
                        'type': 'page',
                        'tags': accessTags
                    }
            except:
                print("[ERROR] EMERGENCY TERMINATION!")
                exit() 

            # Send the post data to the server
            throttle()
            # print(post)
            
            r = requests.post(recieving_server + '/posts?limit=1&offset=0&shortcodes_mode=feeds', headers=header, json=post)
            response_log.append([str(r), recieving_server, "/posts?limit=1&offset=0&shortcodes_mode=feeds", "[POST] => " + str(post), str(r.text)])
            
			#Just a random counting thing.
            count = count + 1
            
            # Check the Response
            if (str(r) == "<Response [400]>" or str(r) == "<Response [429]>" or str(r) == "<Response [500]>"):
                print("Upload Failed! Retrying...")
                r = requests.post(recieving_server + '/posts?limit=1&offset=0&shortcodes_mode=feeds', headers=header, json=post)
                response_log.append([str(r), recieving_server, "/posts?limit=1&offset=0&shortcodes_mode=feeds", "[RETRY][POST] => " + str(post), str(r.text)])
                
                # Retry is response is 400 or 429 or even 500
                if (str(r) == "<Response [400]>" or str(r) == "<Response [429]>" or str(r) == "<Response [500]>"):
                    print("Upload Failed... Abort with code returned " + str(r) )
                    errorReportingServices(253, "Server responded 429/400. \nIndex :" + str(page) + "\n Prop: " + str(prop), str(post), r.text)
                    response_log.append([str(r), recieving_server, "posts", "[RETRY][POST] => " + str(post), str(r.text)])
                    print("\n[NewsGram.com] xxxxxxxxxxxxxxx( FAILED )xxxxxxxxxxxxxxx [newsgram.rebelmouse.xyz]\n\tPost Name: " + page[prop]['title']['rendered'] + " [" +  str(count) + " of 40400]\n")
                    
            elif (str(r) == "<Response [200]>"):
                
                # Hurray! Thats done
	            print("\n[NewsGram.com] ===============(100%)=============== [newsgram.rebelmouse.xyz]\n\tPost Name: " + page[prop]['title']['rendered'] + " [" +  str(count) + " of 40400]\n")
                        
            else:
                post = {
                        "headline": str(page[prop]['title']['rendered']),
                        "created_ts": dt_obj,
                        "page_title": str(page[prop]['title']['rendered']),
                        "body": content,
                        "sections": temp,   
                        "image_id": f_id,
                        'action': 'publish'
                }
                r = requests.post(recieving_server + '/posts?limit=1&offset=0&shortcodes_mode=feeds', headers=header, json=post)
                print("\n\n[WARNING] Unable to Verify Upload status. Server responded with code " + str(r) + "\nLoggerMod\n" + str(r.text))
                if (str(r) == "<Response [400]>" or str(r) == "<Response [429]>" or str(r) == "<Response [500]>"):
                    print("\n[NewsGram.com] ===============(100%)=============== [newsgram.rebelmouse.xyz]\n\tPost Name: " + page[prop]['title']['rendered'] + " [" +  str(count) + " of 40400]\n")
                elif (str(r) == "<Response [400]>" or str(r) == "<Response [429]>" or str(r) == "<Response [500]>"):
                    print("\n[NewsGram.com] ===============( FAILED )=============== [newsgram.rebelmouse.xyz]\n\tPost Name: " + page[prop]['title']['rendered'] + " [" +  str(count) + " of 40400]\n")
                else:
                    print("\n[NewsGram.com] xxxxxxxxxxxxxxx( UNKNOWN )xxxxxxxxxxxxxxx [newsgram.rebelmouse.xyz]\n\tPost Name: " + page[prop]['title']['rendered'] + " [" +  str(count) + " of 40400]\n")
                
            with open('transfer_log.csv', 'w', newline='',  encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(response_log)
        
        except:
            print("\n\n\nERROR!\n[FATAL ERROR] Failed to upload Page: " + str(respond) + ", Prop: " + str(prop) + "\n\nResuming\n\n\n" )
            errorReportingServices(267, "An Error has occured for upload data Page: " + str(respond) + ", Prop: " + str(prop), "", str(r) )
            with open('failed.csv', 'w', newline='',  encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows([str(respond), str(prop)])
            with open('transfer_log.csv', 'w', newline='',  encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(response_log)