#!/usr/bin/python3
__author__ = "https://codeberg.org/allendema"
import json
import sys
from bs4 import BeautifulSoup
import requests


YELLOW = "\033[1;32;40m"
RED = "\033[31m"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/103.0.2'}

base_url = "https://story.snapchat.com/@"

def get_json(username):
	"""Get json from the website"""

	r = requests.get(f'{base_url}{username}', headers=headers)

	if r.ok:
		#print(f"{YELLOW} Snapchat site is Responding :)  \n")
		pass

	else:
		sys.exit(f"{RED} Oh Snap! No connection with Snap!")

	soup = BeautifulSoup(r.content, "html.parser")

	# Find the script with the JSON data on the site
	snaps = soup.find(id="__NEXT_DATA__").string.strip()

	#print("The script exists. \n")
	data = json.loads(snaps)

	return data


def profile_metadata(jsondata):
    data = {
        "bitmoji": "",
        "bio": ""
    }
  
    try:
        bitmoji = jsondata["props"]["pageProps"]["userProfile"]["publicProfileInfo"]["snapcodeImageUrl"]
        bio = jsondata["props"]["pageProps"]["userProfile"]["publicProfileInfo"]["bio"]
        
        data['bio'] = bio
        data['bitmoji'] = bitmoji
        
    except KeyError:
        bitmoji = jsondata["props"]["pageProps"]["userProfile"]["userInfo"]["snapcodeImageUrl"]
        bio = jsondata["props"]["pageProps"]["userProfile"]["userInfo"]["displayName"]
        
        data['bio'] = bio
        data['bitmoji'] = bitmoji
    
    return data