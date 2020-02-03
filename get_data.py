import requests
import re
import os


def store_video(id):
    print(f'Downloading {id}')
    res = requests.get(f'https://59f185ece6219.streamlock.net/aloha/_definst_/aloha.stream/{id}')
    file_path = f'data/{id}'
    with open(file_path, 'wb') as f:
        f.write(res.content)
    return file_path


def extract_frame(video_path, frame_nr):
    print(f'Extracting frame {frame_nr} from {video_path}')
    out_file = f'{video_path}_{frame_nr}.png'

    assert not os.path.exists(out_file), f'{out_file} already exists!'

    os.system(f'ffmpeg -i {video_path} -vf "select=eq(n\,{frame_nr})" -vframes 1 {out_file} -v quiet')
    return out_file


def get_video_ids():
    print('Downloading video list')
    res = requests.get('https://59f185ece6219.streamlock.net/aloha/_definst_/aloha.stream/chunklist_w1062484037.m3u8')

    content = res.content.decode('utf-8')
    return [s for s in content.split('\n') if re.match('^media_.*ts$', s)]


def main():
    files = os.listdir('data')
    print(f'Found {len(files)} existing data files')

    for video_id in get_video_ids():
        video_path = store_video(video_id)
        for fn in [0, 25, 50, 75]:
            extract_frame(video_path, fn)
        os.remove(video_path)


if __name__ == '__main__':
    main()
