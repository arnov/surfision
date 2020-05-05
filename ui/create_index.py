from fetch.fetch_data import ALL_CAMS
from fetch.cams import ChunkListCam, YoutubeCam
import urllib.parse


for cam_id, cam in ALL_CAMS.items():
    if isinstance(cam, YoutubeCam):
        html = (
            '<div>'
              f'<h1>{cam.name}</h1>'
              f'<iframe id="ytplayer" type="text/html" width="640" height="360" src="{cam.url}"'
            'frameborder="0"></iframe>'
            '</div>'
        )
        print(html)
    elif isinstance(cam, ChunkListCam):
        video_list_url = cam.video_list_url

        if not cam.cors_allowed:
            get_param = urllib.parse.quote(cam.video_list_url)
            video_list_url = f'http://35.196.30.60:8080?url={get_param}'

        html = (
            '<div>'
              f'<h1>{cam.name}</h1>'
              f'<div id="player_{cam_id}"></div>'
              '<script>'
                f'var player_{cam_id} = new Clappr.Player({{source: "{video_list_url}", parentId: "#player_{cam_id}", mimeType: "application/vnd.apple.mpegurl", poster: "https://i.nextmedia.com.au/Utils/ImageResizer.ashx?n=https%3A%2F%2Fi.nextmedia.com.au%2FNews%2F3910a2aa8d732fe98940c5313ce71397.jpg&h=630&w=1120&c=1&s=1"}});'
              '</script>'
            '</div>'
        )
        print(html)
