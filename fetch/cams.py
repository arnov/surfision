from abc import ABC, abstractmethod
from datetime import datetime
import requests
import re
import os


class Cam:
    @abstractmethod
    def store_live_frame():
        pass

    def generate_image_path(self):
        return (f'data/live/{self.__class__.__name__.lower()}_'
                f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg')

    def extract_frame(self, video_path, frame_nr):
        print(f'Extracting frame {frame_nr} from {video_path}')
        out_file = f'{video_path}_{frame_nr}.png'

        assert not os.path.exists(out_file), f'{out_file} already exists!'

        os.system(f'ffmpeg -i {video_path} -vf "select=eq(n\,{frame_nr})" -vframes 1 {out_file} -v quiet')
        return out_file


class ChunkListCam(Cam):
    def store_live_frame(self):
        for video_id in self.get_video_ids():
            video_path = self.store_video(video_id)
            image_path = self.extract_frame(video_path, 25)

            new_path = self.generate_image_path()
            os.rename(image_path, new_path)

            os.remove(video_path)
            return new_path

    def store_video(self, id):
        print(f'Downloading {id}')
        res = requests.get(f'{self.video_url}/{id}')
        file_path = f'data/{id}'
        with open(file_path, 'wb') as f:
            f.write(res.content)
        return file_path

    def get_video_ids(self):
        print('Downloading video list')
        res = requests.get(self.video_list_url)

        content = res.content.decode('utf-8')
        return [s for s in content.split('\n') if re.match('^media.*\.ts$', s)]


class YoutubeCam(Cam):
    def store_live_frame(self):
        image_path = self.generate_image_path()
        frame_nr = 25
        os.system(f'ffmpeg -i `youtube-dl -g https://youtu.be/QcurPcHwX6U` -t 00:00:02.00 '
                  f'-vf "select=eq(n\,{frame_nr})" -vframes 1 {image_path} -v quiet')
        return image_path


class PettenCam(YoutubeCam):
    name = 'Petten'
    url = 'https://youtu.be/QcurPcHwX6U'


class WijkCam(ChunkListCam):
    name = 'Wijk'
    video_list_url = ('https://59f185ece6219.streamlock.net/aloha/_definst_/'
                      'aloha.stream/chunklist_w1062484037.m3u8')
    video_url = 'https://59f185ece6219.streamlock.net/aloha/_definst_/aloha.stream'


class ScheveningCam(Cam):
    name = 'Scheveningen'
    image_url = 'http://scheveningenlive.nl/cam_1.jpg'

    def store_live_frame(self):
        response = requests.get(self.image_url)
        image_path = self.generate_image_path()

        with open(image_path, 'wb') as f:
            f.write(response.content)

        return image_path


class AnchorPointCam(ChunkListCam):
    name = 'Anchor Point'
    video_list_url = ('https://cams.cdn-surfline.com/cdn-int/'
                      'ma-anchorpoint/chunklist.m3u8')
    video_url = 'https://cams.cdn-surfline.com/cdn-int/ma-anchorpoint'


class SanSebastianCam(ChunkListCam):
    name = 'San Sebastian'
    video_list_url = ('https://cams.cdn-surfline.com/cdn-int/'
                      'es-sansebastianov/chunklist.m3u8')
    video_url = 'https://cams.cdn-surfline.com/cdn-int/es-sansebastianov'


class SouthBeachCam(ChunkListCam):
    name = 'South Beach'
    video_list_url = ('https://cams.cdn-surfline.com/cdn-ec/'
                      'ec-southbeach/chunklist.m3u8')
    video_url = 'https://cams.cdn-surfline.com/cdn-ec/ec-southbeach/'
