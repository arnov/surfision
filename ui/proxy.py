from flask import Flask, Response, request, abort
import requests
import urllib.parse

from fetch.cams import ChunkListCam

app = Flask(__name__)

URL_LOOKUP = {}
ALLOWED_HOSTS = {'cams.cdn-surfline.com'}


@app.route('/index.html')
def index():
    with open('ui/index.html') as f:
        return ''.join(f.readlines())


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def proxy(u_path):
    url = request.args.get('url')

    if not url:
        vid_id = u_path.strip('/')
        url = URL_LOOKUP.get(vid_id)
        if not url:
            abort(404)

    netloc = urllib.parse.urlparse(url).netloc

    if netloc in ALLOWED_HOSTS:
        res = requests.get(url)

    if '.m3u8' in url:
        video_ids = ChunkListCam.parse_video_list(res)
        base_url = url.rsplit('/', 1)[0]
        for vid_id in video_ids:
            URL_LOOKUP[vid_id] = f'{base_url}/{vid_id}'

    return Response(res.content, headers=dict(res.headers))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
