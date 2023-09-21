from flask import Flask
from flask import request, make_response, jsonify
import scrapetube
import json

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
    

if __name__ == '__main__':
    app.run()