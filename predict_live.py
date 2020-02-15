import os

from fetch.fetch_data import fetch_frame
from predict import predict_image
from surf_dataset import CLASSES

import click


@click.command()
@click.option('--cam', default='wijk')
def main(cam):
    os.makedirs('data/live', exist_ok=True)

    image_path = fetch_frame(cam)

    prediction = predict_image(image_path, plot=True)
    pred_classes = [CLASSES.get(c) for c in prediction['class_ids']]

    print(f'Predicted: {pred_classes}')

    if len([c for c in pred_classes if c not in {'walker', 'dog'}]) > 0:
        print('Found surfer(s), storing image')
    else:
        os.remove(image_path)


if __name__ == '__main__':
    main()
