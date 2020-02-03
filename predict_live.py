import os

from get_data import get_video_ids, store_video, extract_frame
from predict import predict_image
from surf_dataset import CLASSES


def main():
    video_id = get_video_ids()[0]
    video_path = store_video(video_id)
    for fn in [0, 75]:
        file = extract_frame(video_path, fn)

        prediction = predict_image(file, plot=False)
        print([CLASSES.get(c) for c in prediction['class_ids']])

        os.remove(file)
    os.remove(video_path)


if __name__ == '__main__':
    main()
