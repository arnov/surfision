import os
from collections import Counter
from datetime import datetime

from fetch.fetch_data import fetch_frame
from predict.predict_image import predict_image
from train.surf_dataset import CLASSES

import click
import pandas as pd


def store_predictions(cam, prediction):
    file_path = 'predictions.csv'

    counts = Counter(prediction)
    for c in CLASSES.values():
        if c not in counts:
            counts[c] = 0

    df = pd.DataFrame({col: [count] for col, count in counts.items()})
    df['cam'] = cam
    df['timestamp'] = datetime.now()

    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path)
        df = pd.concat([df_old, df])

    df.to_csv(file_path, index=False)
    print(f'Added predictions to {file_path}')


@click.command()
@click.option('--cam', default='wijk')
def main(cam):
    print(f'{datetime.now()}: Predicting live image for {cam}')

    os.makedirs('data/live', exist_ok=True)
    image_path = fetch_frame(cam)

    prediction = predict_image(image_path, plot=True)
    pred_classes = [CLASSES.get(c) for c in prediction['class_ids']]

    print(f'Predicted: {Counter(pred_classes)}')

    if len([c for c in pred_classes if c in {'supper', 'surfer'}]) > 2:
        print('Found surfer(s), storing image')
    else:
        os.remove(image_path)

    store_predictions(cam, pred_classes)


if __name__ == '__main__':
    main()
