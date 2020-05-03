from fetch.fetch_data import ALL_CAMS
from fetch.cams import ChunkListCam, YoutubeCam


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
        html = (
            '<div>'
              f'<h1>{cam.name}</h1>'
              f'<div id="player_{cam_id}"></div>'
              '<script>'
                f'var player2 = new Clappr.Player({{source: "{cam.video_list_url}", parentId: "#player_{cam_id}"}});'
              '</script>'
            '</div>'
        )
        print(html)
