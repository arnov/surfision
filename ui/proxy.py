from flask import Flask, Response, request
import requests

from fetch.cams import ChunkListCam

app = Flask(__name__)

URL_LOOKUP = {}


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def proxy(u_path):
    url = request.args.get('url')

    if not url:
        vid_id = u_path.strip('/')
        url = URL_LOOKUP[vid_id]

    res = requests.get(url)

    if '.m3u8' in url:
        video_ids = ChunkListCam.parse_video_list(res)
        base_url = url.rsplit('/', 1)[0]
        for vid_id in video_ids:
            URL_LOOKUP[vid_id] = f'{base_url}/{vid_id}'

    return Response(res.content, headers=dict(res.headers))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
