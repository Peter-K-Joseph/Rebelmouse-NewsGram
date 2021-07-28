import time
import simplejson
import hmac
import hashlib
import base64
import requests
from pprint import pprint
import json
import csv

client_id = 'YLsZV1nAUlXi7tEXNJAYECAReOVMjWaL0x93pzTIAzCXTnfG8ddWAgZ96n6pk1KH',
api_secret = 'DHDRFGzobhw0cQHh6lMxIKgmZSyWpxJaFraTj2zXfBX5aCWNUsqtFEeE3Ax7BdKe'

secret_key = 'RVpf026gF2k8ximQeJ2lYaH29LZQ22nJCjUTMdCMmHi6qmnlPTJj01tL6V8PvVSM'
public_key = 'OKeff4rlS47VD1kyqiAcvg1uly2Y0YQNzElKhwlVp3minqOZI6ONiJHYil6vbKrP'

r = requests.get("https://disqus.com/api/3.0/forumCategories/details.json?api_key={}&forumCategory=3614288".format(public_key))
pprint(r.text)
open('data.json', 'wb').write(r.content)