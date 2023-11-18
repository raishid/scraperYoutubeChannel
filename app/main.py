from flask import Flask
from flask import request, make_response, jsonify
import scrapetube
from modules.SnapCrap import get_json, profile_metadata
from modules.linkedin_scraper import Person, actions
from undetected_chromedriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from modules.tweety.src.tweety import Twitter
import json
import requests

app = Flask(__name__)

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


    cookie = open('cookies.linkedin.txt', 'r').read()

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

@app.route('/api/creacionesmarfeluis')
def getMarfeluis():
    r = requests.get('https://www.instagram.com/api/v1/users/web_profile_info/?username=creacionesmarfeluis.oficial', headers={
        "X-Ig-App-Id": "936619743392459"
    })

    data = r.json()

    return make_response(data)


if __name__ == '__main__':
    app.run(async_mode='gevent_uwsgi')