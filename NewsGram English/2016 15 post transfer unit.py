import PIL
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

Image.MAX_IMAGE_PIXELS = None

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

header_wp = {
    'X-RMAuth': 'KlCym4YdO1BQrvAWjNkuHBPhaw5OxkS4wENNlQbaKCEhqOpxyewBWVzV4479IpDm',
    'User-Agent': 'PostmanRuntime/7.28.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Postman-Token': '3381a69f-f418-41b3-89a4-33b1106fd976',
    'Host': 'newsgram.rebelmouse.dev',
    'Accept-Encoding': 'gzip%2C deflate%2C br',
    'Connection': 'keep-alive',
    'Authorization': 'Basic bmV3c2luZGlhOmEzTkFlaGNLQVNTeCV4I14pKUFzMVgzdw=='
    
}

id_connect_old_to_new = [[64, 552299877], [49578, 552299878], [40275, 552299879], [60502, 552299880], [54639, 552299881], [60256, 552299882], [60503, 552299883], [9, 552299884], [60505, 552299885], [3296, 552299886], [39673, 552299887], [37, 552299888], [41626, 552299889], [60501, 552299890], [41989, 552299891], [
    6, 552299892], [21127, 552299893], [5, 552299894], [19043, 552299895], [11, 552299896], [41779, 552299897], [60461, 552299898], [19302, 552299899], [7, 552299900], [60504, 552299901], [42415, 552299902], [42225, 552299903], [53347, 552299904], [8, 552299905], [38915, 552299906], [42506, 552299907], [41981, 552299908]]

recieving_server = "https://newsgram.rebelmouse.dev/api/1.3"
requesting_server = "https://www.newsgram.com/wp-json/wp/v2"

_8127quotation = []


# JUST SOME RANDOM FILE NAMES
def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# IMAGE DOWNLOADER


def ImageDownload(get):
    get = get.replace("https://i0.wp.com/", "")
    try:
        try:
            image = wget.download(get)
        except:
            print("MEDIA OVERRIDE\n______________\nTarget Destination: " + get)
            print("Error Downloading. Permission Denied by HOST Machine")
        print("\n[IMAGE] Image '" + image + "' was downloaded from " + get)
        ext = image.split(".")
        ext = ext[-1]
        __temp = Image.open(image)
        # print(__temp)
        width, height = __temp.size
        print([width, height])
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
            print("[IMAGINENGINE (IMAGE PROCESSOR)] Resizing Image")
            try:
                im = im.resize((round(width*0.7), round(height*0.7)))
                im.show()
                print("[IMAGINENGINE (IMAGE PROCESSOR)] Image Resize operation complete")
                filename = randomword(25) + '.jpg'
                im.save(filename, 'jpeg')
                return filename
            except:
                print("[ERROR REPORTING SERVICES] Image Resize operation failed!")
                print("[ERROR REPORTING SERVICES] Returning Original Image Data")
                return image
        else:
            return image
    except:
        print("MEDIA OVERRIDE\n______________\nTarget Destination: " + get)
        print("[ERROR REPORTING SERVICES] ImagesEngine Encountered an Error")


# PARSE A SPECIFIED TEXT FROM A SELECTOR
def parse_text(content, tag):
    soup = BeautifulSoup(content, features="lxml")
    text = ""
    for x in soup.find_all(tag):
        if (x.getText() != ""):
            text = text + x.getText()

    return "<" + tag + ">" + text + "</" + tag + ">"


# FIND IMAGE SUBTITLES
def find_subtitle(link):
    global header_wp
    content = requests.get("https://www.newsgram.com/wp-json/wp/v2/posts/" + str(link), headers=header_wp)
    content = json.loads(content.text)
    content = requests.get(content['link'], headers=header_wp)
    content = content.text

    soup = BeautifulSoup(content, features="html.parser")
    text = ""
    tag = "tdb_single_subtitle"
    for x in soup.find_all("p", class_=tag):
        if (x.getText() != ""):
            text = text + x.getText()
    text = text.replace("\n", "", -1)
    return text

# GET IMAGE SUBTITLES


def getImageSubs(link):
    global header_wp
    content = requests.get("https://www.newsgram.com/wp-json/wp/v2/posts/" + str(link), headers=header_wp)
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

# LITERALLY NO IDEA :}


def getTags(link):
    global header_wp
    tags = []
    content = requests.get(str(link), headers=header_wp)
    content = json.loads(content.text)
    for prop in range(0, len(content)):
        tags.append(content[prop]["name"])

    return tags


failed = [245931]
failed_again = []

for respond in failed:
    page = requests.get("https://www.newsgram.com/wp-json/wp/v2/posts/" + str(respond), headers=header_wp)
    page = json.loads(page.text)
    print(len(page))

    print("[" + str(respond)+"] Getting data from newsgram server")
    try:
        updateId = requests.get("https://newsgram.rebelmouse.dev/api/1.3/posts/basename?basename={}".format(str(page['slug']).replace("%", "")), headers=header)
        updateId.raise_for_status()
        updateId = json.loads(updateId.text)
        try:
            post_rebel = requests.delete(
                "https://newsgram.rebelmouse.dev/api/1.3/posts/{}".format(updateId[0]["id"]), headers=header)
            print("DELETE RESPONDED WITH " + str(post_rebel))
        except:
            print("["+str(respond)+"] Server Couldn't Delete Specified data")

            # __________________________________________________________________________________________________________________________________
            # RESET AND START POST UPLOAD SEQUENCE
        this_contains_category = []

        for getIDOne in range(0, len(page['categories'])):
            for prop_scan in range(0, len(id_connect_old_to_new)):
                if (page['categories'][getIDOne] == id_connect_old_to_new[prop_scan][0]):
                    this_contains_category.append(
                        id_connect_old_to_new[prop_scan][1])

        print("["+str(respond)+"] Category Data Added")
        # __________________________________________________________________________________________________________________________________
        # GETS THE LEAD IMAGE FROM THE SERVER
        if(page['featured_media'] != 0):
            try:
                nolead = False
                print("["+str(respond)+"] Downloading Image from " +requesting_server + '/media/' + str(page['featured_media']))
                data_from_the_image_scan_request = requests.get(requesting_server + '/media/' + str(page['featured_media']), headers=header_wp)
                data_from_the_image_scan_request = json.loads(
                    data_from_the_image_scan_request.text)
                lead_image_name = ImageDownload(
                    str(data_from_the_image_scan_request['guid']['rendered']))
                PIL.show("./lead_image_name")
                lead_image_dt = Image.open("./" + lead_image_name)
                print(
                    "["+str(respond)+"] Getting width and height of image - " + lead_image_name)

                width_of_lead_image = lead_image_dt.width
                height_of_lead_image = lead_image_dt.height

                print("["+str(respond)+"] Uploading Lead Image " +
                    requesting_server + '/media/' + str(page['featured_media']))
                try:
                    lead_image_data = {
                        'file': open(lead_image_name, 'rb'),
                        'title': data_from_the_image_scan_request['title']['rendered'],
                        'description': parse_text(str(data_from_the_image_scan_request['description']['rendered']), 'p'),
                        'alt': data_from_the_image_scan_request['alt_text'],
                        'caption': data_from_the_image_scan_request['caption']['rendered']
                    }
                except:
                    lead_image_data = {
                        'file': open(lead_image_name, 'rb'),
                        'title': data_from_the_image_scan_request['title']['rendered']
                    }
                print("["+str(respond)+"] Lead Image Prepared")

                upload_lead_image = None
                
                try:
                    upload_lead_image = requests.post(recieving_server + '/images', headers=header, files=lead_image_data)
                    pprint(str(upload_lead_image))
                    upload_lead_image = json.loads(upload_lead_image.text)
                    upload_lead_image = upload_lead_image["id"]
                    print("["+str(respond)+"] Rebelmouse Returned ID: " + str(upload_lead_image))
                except:
                    print("["+str(respond)+"] An Error Occurred while uploading lead data")
            except:
                print("[ERROR REPORTING SERVICES] A FATAL ERROR OCCURRED WHILE DOWNLOADING IMAGES: <RESPONSE:404> FILE DOES NOT EXIXT")
                nolead = True
        else:
            print("[ERROR REPORTING SERVICES] Newsgram Server dont have a lead image tag or the tag has an invalid character")
        # __________________________________________________________________________________________________________________________________
        # NO CLUSE WHY THESE ARE HERE
        try:
            accessTags = getTags(page['_links']['wp:term'][1]['href'])
            imageCaption = getImageSubs(page['id'])
        except:
            print("[ERROR REPORTING SERVICES] Service failure for accessTags and imageCation")
            try:
                imageCaption = getImageSubs(page['id'])
            except:
                print("[ERROR REPORTING SERVICES] imageCaption continues to fail! Aborting....")
        # __________________________________________________________________________________________________________________________________
        # GETTING THE CONTENT
        content = str(page['content']['rendered']).replace("\n", "")
        content = content.replace("""\\""", "")
        # __________________________________________________________________________________________________________________________________
        # CONTENT IMAGES UPLOAD
        try:
            soup = BeautifulSoup(content, features="lxml")
            print("[UPDATE] Images Parsed from HTML Page. System preparing to upload " + str(len(soup.find_all('figure'))) + " images")
            if (len(soup.find_all('figure')) != 0):
                image_cap_track = 1
                for link in soup.find_all('figure'):
                    print(link)
                    try:
                        r = requests.get(requesting_server + "/media/" + link.get("id").replace("attachment_", ""), headers=header_wp)
                        print("[UPDATE] Sending GET request to {}".format(requesting_server + "/media/" + link.get("id").replace("attachment_", "")))
                        r = json.loads(r.text)
                        name = ImageDownload(r["guid"]["rendered"])

                        create_media = {
                            'file': open(name, 'rb'),
                            'title': r['title']['rendered'],
                            'alt': parse_text(r['alt_text'], "p"),
                            'caption': parse_text(r['caption']['rendered'], 'p')
                        }
                        
                        try:
                            r = requests.post(recieving_server + '/images', headers=header, files=create_media)
                            code = str(r)
                            r = json.loads(r.text)
                            if (len(soup.find_all('figure')) == len(imageCaption)-1):
                                r = "<div style=\"width: 100%\"><center>" + r["shortcode"].replace("\n", "").replace("\\", "") + "</center><p style=\"color: grey;padding: 0;margin: 0;font-size: 1rem; text-align:right\">" + imageCaption[image_cap_track] + "</p></div><br>"
                            else:
                                r = "<div style=\"width: 100%\"><center>" + r["shortcode"].replace("\n", "").replace("\\", "") + "</center><br></div>"
                            image_cap_track = image_cap_track + 1
                            link.clear()
                            link.append(BeautifulSoup(r, 'html.parser'))
                            print(
                                "[NOTIFY] A Media file upload request was sent and the server returned a " + code)
                        except:
                            print(str(link.get("id")) + " enountered an error")
                    
                    except:
                        try:
                            print("[ERROR REPORTING SERVICES] IMAGE UPLOADING ENCOUNTERED AND ERROR USING API. PARSING FROM CURR_VAL")
                            dataset = BeautifulSoup(str(link), features="lxml")
                            imageGet = dataset.find("img")
                            name = ImageDownload(imageGet["src"])
                            
                            create_media = {
                                'file': open(name, 'rb'),
                                'title': imageGet['alt'],
                                'alt': imageGet['alt'],
                            }
                            
                            try:
                                r = requests.post(recieving_server + '/images', headers=header, files=create_media)
                                code = str(r)
                                r = json.loads(r.text)
                                if (len(soup.find_all('figure')) == len(imageCaption)-1):
                                    r = "<div style=\"width: 100%\"><center>" + r["shortcode"].replace("\n", "").replace("\\", "") + "</center><p style=\"color: grey;padding: 0;margin: 0;font-size: 1rem; text-align:right\">" + imageCaption[image_cap_track] + "</p></div><br>"
                                else:
                                    r = "<div style=\"width: 100%\"><center>" + r["shortcode"].replace("\n", "").replace("\\", "") + "</center><br></div>"
                                image_cap_track = image_cap_track + 1
                                link.clear()
                                link.append(BeautifulSoup(r, 'html.parser'))
                                print(
                                    "[NOTIFY] A Media file upload request was sent and the server returned a " + code)
                            except:
                                print(str(link.get("id")) + " enountered an error")
                        except:
                            dataset = BeautifulSoup(str(link), features="lxml")
                            imageGet = dataset.find("img")
                            if ("https://www.newsgram.com" in imageGet["src"]):
                                print("[ERROR REPORTING SERVICES] Failed uploading imgage hosted on target machine")
                            else:
                                print("[ERROR REPORTING SERVICES] Contining data from {} as per 'as it is' method".format(imageGet["src"]) )

                    link['style'] = ""

            
            content = str(soup).replace("<html><body>", "").replace("</body></html>", "").replace(u'\xa0', u' ')
        except:
            print("[ERROR REPORTING SERVICES] System Malfunction Detected. ImageParser Failed")
        # soup = BeautifulSoup(content, features="lxml")
        # print("["+str(respond)+"] System Found " +
        #       str(len(soup.find_all('img'))) + " images")
        # if (len(soup.find_all('img')) == 0):
        #     print("["+str(respond)+"] Checking Alertnative Images")
        # image_cap_track = 1
        # if (len(soup.find_all('img')) != 0):
        #     image_cap_track = 1
        #     for link in soup.find_all('img'):
        #         try:
        #             r = requests.get(
        #                 requesting_server + "/media/" + link.get("id").replace("attachment_", ""))
        #             r = json.loads(r.text)
        #             name = ImageDownload(r["guid"]["rendered"])
        #             create_media = {
        #                 'file': open(name, 'rb'),
        #                 'title': r['title']['rendered'],
        #                 'alt': parse_text(r['alt_text'], "p"),
        #                 'caption': parse_text(r['caption']['rendered'], 'p')
        #             }
        #         except:
        #             name = ImageDownload(link.get("src"))
        #             create_media = {
        #                 'file': open(name, 'rb')
        #             }

        #         link['style'] = ""

        #         try:
        #             r = requests.post(recieving_server + '/images',
        #                               headers=header, files=create_media)
        #             code = str(r)
        #             r = json.loads(r.text)
        #             if (len(soup.find_all('img')) == len(imageCaption)-1):
        #                 r = "<div style=\"max-width: 100%\"><center>" + r["shortcode"].replace("\n", "").replace("\\", "") + "</center><p style=\"color: grey;padding: 0;margin: 0;font-size: 1rem; text-align:right\">" + imageCaption[image_cap_track] + "</p></div><br>"
        #             else:
        #                 r = "<div style=\"max-width: 100%\"><center>" + r["shortcode"].replace("\n", "").replace("\\", "") + "</center><br></div>"
        #             image_cap_track = image_cap_track + 1
        #             link.clear()
        #             link.append(BeautifulSoup(r, 'html.parser'))
        #             print(
        #                 "[NOTIFY] A Media file upload request was sent and the server returned a " + code)
        #         except:
        #             print("AN ERROR ENCOUNTERED WHILE UPLOADING AN IMAGE")
        #             link.clear()
        #             print(
        #                 "[NOTIFY] A Media file upload request was sent and the server returned a " + code)

        #         print("[NOTIFY] All Images where uplaoded successfully!")

        # # __________________________________________________________________________________________________________________________________
        # # GETTING READY TO UPLOAD and SOME FINAL DATA COLLECTION
        # content = str(soup).replace("<html><body>", "").replace( "</body></html>", "").replace(u'\xa0', u' ')
        dt_obj = datetime.strptime(
            str(page['date_gmt']).replace("T", " "), '%Y-%m-%d %H:%M:%S')
        dt_obj = int(dt_obj.timestamp())
        content = content.replace(
            "https://www.newsgram.com/", "https://newsgram.rebelmouse.dev/", -1)

        # __________________________________________________________________________________________________________________________________
        # GETTING PAGE SUBTITLES
        try:
            get_subtitle = find_subtitle(page['id'])
        except:
            get_subtitle = ""

        soup = BeautifulSoup(content, 'html.parser')
        try:
            for y in soup.find_all('img'):
                y.clear()
        except:
            print("")
        content = str(soup).replace("<html><body>", "").replace(
            "</body></html>", "").replace(u'\xa0', u' ')
        
        try:    
            if (nolead == "8465123168645312"):
                post = {
                        "headline": html.unescape(page["title"]["rendered"]),
                        "created_ts": dt_obj,
                        "page_title": html.unescape(page["title"]["rendered"]),
                        "body": content,
                        "sections": this_contains_category,
                        'action': 'publish',
                        'subheadline': get_subtitle,
                        'manual_basename': str(page['slug']).replace("%", ""),
                        'type': 'page',
                        'tags': accessTags,
                    }
                post_rep = {
                        "headline": html.unescape(page["title"]["rendered"]),
                        "created_ts": dt_obj,
                        "page_title": html.unescape(page["title"]["rendered"]),
                        "sections": this_contains_category,
                        'action': 'publish',
                        'subheadline': get_subtitle,
                        'manual_basename': str(page['slug']).replace("%", ""),
                        'type': 'page',
                        'tags': accessTags,
                }
            else:
                try:
                    post = {
                        "headline": html.unescape(page["title"]["rendered"]),
                        "created_ts": dt_obj,
                        "page_title": html.unescape(page["title"]["rendered"]),
                        "body": content,
                        "sections": this_contains_category,
                        'action': 'publish',
                        "image_id": upload_lead_image,
                        'image_size': '{}x{}'.format(width_of_lead_image, height_of_lead_image),
                        'subheadline': get_subtitle,
                        'manual_basename': str(page['slug']).replace("%", ""),
                        'type': 'page',
                        # 'tags': accessTags,
                        'photo_caption': imageCaption[0]
                    }
                    
                    post_rep = {
                        "headline": html.unescape(page["title"]["rendered"]),
                        "created_ts": dt_obj,
                        "page_title": html.unescape(page["title"]["rendered"]),
                        "sections": this_contains_category,
                        'action': 'publish',
                        "image_id": upload_lead_image,
                        'image_size': '{}x{}'.format(width_of_lead_image, height_of_lead_image),
                        'subheadline': get_subtitle,
                        'manual_basename': str(page['slug']).replace("%", ""),
                        'type': 'page',
                        # 'tags': accessTags,
                        'photo_caption': imageCaption[0]
                    }
                    
                except:
                    try:
                        print("!>> [ERROR] EXCEPTION FOUND. NO FEATURE ID")
                        post = {
                            "headline": html.unescape(page["title"]["rendered"]),
                            "created_ts": dt_obj,
                            "page_title": html.unescape(page["title"]["rendered"]),
                            "body": content,
                            "sections": this_contains_category,
                            'action': 'publish',
                            "image_id": upload_lead_image,
                            'subheadline': get_subtitle,
                            'manual_basename': str(page['slug']).replace("%", ""),
                            'type': 'page',
                            # 'tags': accessTags,
                        }
                        
                        post_rep = {
                            "headline": html.unescape(page["title"]["rendered"]),
                            "created_ts": dt_obj,
                            "page_title": html.unescape(page["title"]["rendered"]),
                            "sections": this_contains_category,
                            'action': 'publish',
                            "image_id": upload_lead_image,
                            'subheadline': get_subtitle,
                            'manual_basename': str(page['slug']).replace("%", ""),
                            'type': 'page',
                            # 'tags': accessTags,
                        }
                    except:
                        print("!>> [ERROR] EXCEPTION FOUND. NO LEAD IMAGE")
                        post = {
                            "headline": html.unescape(page["title"]["rendered"]),
                            "created_ts": dt_obj,
                            "page_title": html.unescape(page["title"]["rendered"]),
                            "body": content,
                            "sections": this_contains_category,
                            'action': 'publish',
                            'subheadline': get_subtitle,
                            'manual_basename': str(page['slug']).replace("%", ""),
                            'type': 'page'
                        }
                        
                        post_rep = {
                            "headline": html.unescape(page["title"]["rendered"]),
                            "created_ts": dt_obj,
                            "page_title": html.unescape(page["title"]["rendered"]),
                            "sections": this_contains_category,
                            'action': 'publish',
                            'subheadline': get_subtitle,
                            'manual_basename': str(page['slug']).replace("%", ""),
                            'type': 'page'
                        }
        except:
            pprint(post_rep)

        post_rebel = requests.post(
            "https://newsgram.rebelmouse.dev/api/1.3/posts", headers=header, json=post)
        if (str(post_rebel) == "<Response [400]>" or str(post_rebel) == "<Response [429]>" or str(post_rebel) == "<Response [500]>"):
            try:
                post_rebel = requests.post(
                    "https://newsgram.rebelmouse.dev/api/1.3/posts", headers=header, json=post)
            except:
                continue
        elif (str(post_rebel) == "<Response [200]>"):
            # Hurray! Thats done
            print("\n[NewsGram.com] ===============(100%)=============== [newsgram.rebelmouse.xyz]\n\tPost Name: " +
                  page['title']['rendered'])

        post_rebel.raise_for_status()
        draft_api_response = post_rebel.json()
        print(draft_api_response['post_url'])
        print("SEREVR RESPONDED WITH " + str(post_rebel) + "\n\n")
        x= input("Resume Operation?: ")
    except:
        print("\n\n\n[BACKUP SERVICES] ONE OR MORE SERVICES HAS FAILED. ERROR REPORTING SERVICES ARE IN EFFECT\n[FAILED] POST TRANSFER FAILED: https://newsgram.rebelmouse.dev/{}\n\n\n".format(page["slug"]))
        print("[ERROR REPORTING SERVICES] Going to last known state. Error recovery services initiated\n[ERROR REPORTING SERVICES] Force resuming last known operation.\n[ERROR REPORTING SERVICES] State operations resumued. Code Recovered from last known Error")
        print("____________________________________________________________________________________________________________________________________________________________________\n____________________________________________________________________________________________________________________________________________________________________\n____________________________________________________________________________________________________________________________________________________________________\n____________________________________________________________________________________________________________________________________________________________________\n____________________________________________________________________________________________________________________________________________________________________\n")
        failed_again.append(respond)
        x = input("Load next:" )

print(failed_again)