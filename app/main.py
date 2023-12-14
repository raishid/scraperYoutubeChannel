from flask import Flask
from flask import request, make_response, jsonify
import scrapetube
from modules.SnapCrap import get_json, profile_metadata
from modules.linkedin_scraper import Person, actions
from undetected_chromedriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from modules.tweety.src.tweety import Twitter
from modules.pytok.tiktok import PyTok
import requests
import base64
from urllib.request import urlopen
import numpy as np
from dotenv import load_dotenv
import json
import os
from concurrent.futures import ThreadPoolExecutor
import asyncio

app = Flask(__name__)
executor = ThreadPoolExecutor()

def getChannel(query: str):
    videos = scrapetube.get_search(query=query, results_type="channel")
    channel = list(videos)[0]
    try:
        description = channel['descriptionSnippet']['runs'][0]['text']
    except:
        description = None
    data = {
        "description": description,
        "channelId": channel['channelId'],
        "title": channel['title']['simpleText'],
        "thumbail": f"https:{channel['thumbnail']['thumbnails'][-1]['url']}",
        "sucribers": channel['videoCountText']['simpleText'],
    }
    
    return data

@app.route('/api/channel')
def api_channel():
    query = request.args.get('query')
    if query is None:
        res = jsonify({"error": "query is required"})
        return make_response(res, 400)
    
    data = getChannel(query)
    
    return jsonify(data)

@app.route('/api/snaptchat')
def api_snaptchat():
    query = request.args.get('query')
    if query is None:
        res = jsonify({"error": "query is required"})
        return make_response(res, 400)

    data_profile = get_json(query)
    data = profile_metadata(data_profile)

    return jsonify(data)

@app.route('/api/linkedin')
def api_linkedin():
    query = request.args.get('query')
    if query is None:
        res = jsonify({"error": "query is required"})
        return make_response(res, 400)


    rs = requests.get(f'{os.environ.get("API_URL")}/socials/accounts/linkedin', headers={
        "X-Encryption-Key": os.environ.get("APP_KEY"),
    })
    
    data = rs.json()
    
    #select random data
    data = np.random.choice(data)
    
    cookies = json.loads(data['cookies'])
    
    cookie = None

    for cookie in cookies:
        if cookie['name'] == 'li_at':
            cookie = cookie['value']
            break

    options = ChromeOptions()
    options.add_argument("--headless=chrome")
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64; Ubuntu 22.04) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    chromemanager = ChromeDriverManager(url="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/", latest_release_url="https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE").install()
    print(chromemanager)
    driver = Chrome(options=options, driver_executable_path=chromemanager)
    actions.login(driver, cookie=cookie) # if email and password isnt given, it'll prompt in terminal
    person = Person(query, driver=driver)

    driver.quit()

    return jsonify({
        "name": person.name,
        "profile_image": person.profile_image,
        "query": query
    })

@app.route('/api/twitter')
def api_twitter():
    query = request.args.get('query')
    if query is None:
        res = jsonify({"error": "query is required"})
        return make_response(res, 400)
    
    tw = Twitter('bth')
    uinfo = tw.get_user_info(query)
    return jsonify({
        "id": uinfo.id,
        "name": uinfo.name,
        "profile_image": uinfo.profile_image_url_https,
        "followers": uinfo.followers_count,
        "following": uinfo.friends_count,
        "tweets": uinfo.statuses_count,
    })

@app.route('/api/tiktok')
def api_tiktok():
    query = request.args.get('query')
    if query is None:
        res = jsonify({"error": "query is required"})
        return make_response(res, 400)
    
    query = query.replace("@", "")

    res = executor.submit(executeTiktok, query)

    user_data = res.result()

    return jsonify(user_data)
    
    

@app.route('/api/creacionesmarfeluis')
def getMarfeluis():
    r = requests.get('https://www.instagram.com/api/v1/users/web_profile_info/?username=creacionesmarfeluis.oficial', headers={
        "X-Ig-App-Id": "936619743392459",
        "cookie": 'datr=V5NRZSbOam8-Xirtaa1z8d70;ig_nrcb=1;ds_user_id=635313269;ig_did=3D073320-75ED-4F7A-A586-F327D63898E3;mid=ZVGTWAALAAF_pqsbxCesHe5C8PRn;sessionid=635313269%3AOxBYa3x4agCJbh%3A11%3AAYfNnGZzzfEDTQuO3AAUC3O1n7WJQYZIFal1zUk6tw;fbm_124024574287414=base_domain=.instagram.com;fbsr_124024574287414=wskWLEFjKd1ZszTa8q0WVH4qErx1mh-dIo0yJxhuG8Q.eyJ1c2VyX2lkIjoiMTQ5NzM0NTg5MCIsImNvZGUiOiJBUUFSa1FINDBaVUVRU1BuQ3hVZVJwOGVPSHl0MEFlYnBxaVZqM1J5cGwxY2M5Y01KaDcxMFB4UGZJMHFRNGpnODZKaDdjbGxIWWk5cFZNX2tNOGlGUmpmTWRwenliZE9IR3I2ZDhxOEs1OEo3QW1nSkd0eVRNcVVCUkhsd2c5aFk1VmlfSVdFb1NFMUk2UjJ2ZGFJWGloN3hQOVFWY1JMYzlhd0hoVGFmVm0yVmFYZnF4MGNfSzdKX01GZzF0eVNVa3QtVGFVWGNGeHRCZTl1b05ydXg0VWVlN3BLZDdOeDhXbWJMMS1PYmk3T3dVU3lVMGRUQVYwTlh3TE4zMzlldzJVd1ItTzR5MjB6Y2xLZktBUXg1dmhDaVA4QnZ1d1Y5bGpXamRndVRIZmg3NWdPR1V2R2VxNm16dUlRdFNmWks0USIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQk8zUVVpalN2Q3pPSlRaQmliVFVaQ1BDY1RhR3A3UlpDbDk0MUF6WkEwMHZ0MDU2OWh4ZjRXZXVQU3hLSG9sbUNzS0Jzb0ZSdHRJNlRLbnQwcXBtMHNhbzFmeDBVQ0IxMkdRZzlTTWFvSG9XU1FaQ1RKWkEwV3NFV3lpQlhyTEZka3cyRHZaQ0FwWkJkOUpzaFJnMkpweVpCMWtsWTdpZzJSVjB0V2h4MkhwSTBhYkhxWkExeEdmbU5FTCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNzAwMjc1NTk3fQ;fbsr_124024574287414=wskWLEFjKd1ZszTa8q0WVH4qErx1mh-dIo0yJxhuG8Q.eyJ1c2VyX2lkIjoiMTQ5NzM0NTg5MCIsImNvZGUiOiJBUUFSa1FINDBaVUVRU1BuQ3hVZVJwOGVPSHl0MEFlYnBxaVZqM1J5cGwxY2M5Y01KaDcxMFB4UGZJMHFRNGpnODZKaDdjbGxIWWk5cFZNX2tNOGlGUmpmTWRwenliZE9IR3I2ZDhxOEs1OEo3QW1nSkd0eVRNcVVCUkhsd2c5aFk1VmlfSVdFb1NFMUk2UjJ2ZGFJWGloN3hQOVFWY1JMYzlhd0hoVGFmVm0yVmFYZnF4MGNfSzdKX01GZzF0eVNVa3QtVGFVWGNGeHRCZTl1b05ydXg0VWVlN3BLZDdOeDhXbWJMMS1PYmk3T3dVU3lVMGRUQVYwTlh3TE4zMzlldzJVd1ItTzR5MjB6Y2xLZktBUXg1dmhDaVA4QnZ1d1Y5bGpXamRndVRIZmg3NWdPR1V2R2VxNm16dUlRdFNmWks0USIsIm9hdXRoX3Rva2VuIjoiRUFBQnd6TGl4bmpZQk8zUVVpalN2Q3pPSlRaQmliVFVaQ1BDY1RhR3A3UlpDbDk0MUF6WkEwMHZ0MDU2OWh4ZjRXZXVQU3hLSG9sbUNzS0Jzb0ZSdHRJNlRLbnQwcXBtMHNhbzFmeDBVQ0IxMkdRZzlTTWFvSG9XU1FaQ1RKWkEwV3NFV3lpQlhyTEZka3cyRHZaQ0FwWkJkOUpzaFJnMkpweVpCMWtsWTdpZzJSVjB0V2h4MkhwSTBhYkhxWkExeEdmbU5FTCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNzAwMjc1NTk3fQ;'
    })

    data = r.json()

    posts = []

    edges = data["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

    for post in edges:
        imageuri = base64.b64encode(urlopen(post['node']['thumbnail_src']).read()).decode('utf-8')
        posts.append({
            "url_encode": f"data:image/jpeg;base64,{imageuri}",
            "url_post": f"https://www.instagram.com/p/{post['node']['shortcode']}"
        })

    return make_response(posts)

def executeTiktok(user: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    user_data = loop.run_until_complete(getUserTikTok(user))
    loop.close()
    return user_data

async def getUserTikTok(user: str):
    async with PyTok(headless=True) as api:
            user = api.user(username=user)
            user_data = await user.info()
    
    return user_data


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    #app.run(async_mode='gevent_uwsgi')