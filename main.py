from flask import Flask
from flask import request, make_response, jsonify
import scrapetube
from modules.SnapCrap import get_json, profile_metadata
from modules.linkedin_scraper import Person, actions
from undetected_chromedriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def getChannel(query: str):
    videos = scrapetube.get_search(query=query, results_type="channel")
    channel = list(videos)[0]
    """ print(json.dumps(channel, indent=4)) """
    data = {
        "description": channel['descriptionSnippet']['runs'][0]['text'],
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
    options.add_argument("--headless=new")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

    driver = Chrome(options=options, driver_executable_path=ChromeDriverManager(url="https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/", latest_release_url="https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE").install())
    actions.login(driver, cookie=cookie) # if email and password isnt given, it'll prompt in terminal
    person = Person(query, driver=driver)

    return jsonify({
        "name": person.name,
        "profile_image": person.profile_image,
        "query": query
    })
    

if __name__ == '__main__':
    app.run()