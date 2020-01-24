import requests
import re
import os


def store_video(id):
    print(f'Downloading {id}')
    res = requests.get(f'https://59f185ece6219.streamlock.net/aloha/_definst_/aloha.stream/{id}')
    with open(f'data/{id}', 'wb') as f:
        f.write(res.content)


def extract_frame(id, frame_nr):
    print(f'Extracting frame {frame_nr} from {id}')
    os.system(f'ffmpeg -i data/{id} -vf "select=eq(n\,{frame_nr})" -vframes 1 data/{id}_{frame_nr}.png -v quiet')


def main():
    files = os.listdir('data')
    print(f'Found {len(files)} existing data files')

    res = requests.get('https://59f185ece6219.streamlock.net/aloha/_definst_/aloha.stream/chunklist_w1062484037.m3u8')

    content = res.content.decode('utf-8')
    videos = [s for s in content.split('\n') if re.match('^media_.*ts$', s)]
    for video in videos:
        store_video(video)
        for fn in [0, 25, 50, 75]:
            extract_frame(video, fn)
        os.remove(f'data/{video}')


if __name__ == '__main__':
    main()
