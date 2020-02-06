import os

from get_data import get_video_ids, store_video, extract_frame
from predict import predict_image
from surf_dataset import CLASSES


def main():
    os.makedirs('data/live', exist_ok=True)

    video_id = get_video_ids()[0]
    video_path = store_video(video_id)
    for fn in [0, 75]:
        file = extract_frame(video_path, fn)

        prediction = predict_image(file, plot=True)
        pred_classes = [CLASSES.get(c) for c in prediction['class_ids']]

        print(f'Predicted: {pred_classes}')

        if len([c for c in pred_classes if c not in {'walker', 'dog'}]) > 0:
            print('Found more surfer(s), storing image')
            new_path = file.replace('data/', 'data/live/')
            os.rename(file, new_path)
    os.remove(video_path)


if __name__ == '__main__':
    main()
