from train.surf_dataset import CLASSES

from mrcnn.config import Config
from mrcnn.model import MaskRCNN, mold_image
from numpy import expand_dims
from matplotlib import pyplot
from matplotlib.patches import Rectangle

import click
import skimage
import tensorflow as tf
import logging


class ModelConfig(Config):
    NAME = "surfision_cfg"
    # number of classes (background + surfer/kiter/windsurfer/walker/dog)
    NUM_CLASSES = 1 + len(CLASSES)
    STEPS_PER_EPOCH = 300
    VALIDATION_STEPS = 30


class PredictionConfig(Config):
    NAME = "surf_cfg"
    NUM_CLASSES = ModelConfig.NUM_CLASSES
    DETECTION_MIN_CONFIDENCE = 0.9
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


def load_model(cfg, model_path='mask_rcnn_surfision_cfg_0005_v5.h5'):
    print(f'Loading model: {model_path}')
    model = MaskRCNN(mode='inference', model_dir='./', config=cfg)
    model.load_weights(model_path, by_name=True)

    return model


def plot_prediction(image, prediction, title='Prediction'):
    pyplot.imshow(image)
    pyplot.title(title)
    ax = pyplot.gca()

    for box, class_id in zip(prediction['rois'], prediction['class_ids']):
        y1, x1, y2, x2 = box
        width, height = x2 - x1, y2 - y1
        rect = Rectangle((x1, y1), width, height, fill=False, color='red')

        class_label = CLASSES.get(class_id, '?')
        ax.text(x1, y1 + 8, class_label, color='w', size=11, backgroundcolor="none")
        ax.add_patch(rect)

    pyplot.show()


def predict_image(image_path, plot=True):
    tf.get_logger().setLevel(logging.ERROR)
    cfg = PredictionConfig()

    image = skimage.io.imread(image_path)
    image = image[:, :, 0:3]  # remove alpha

    scaled_image = mold_image(image, cfg)
    sample = expand_dims(scaled_image, 0)

    model = load_model(cfg)

    prediction = model.detect(sample, verbose=0)[0]

    if plot:
        plot_prediction(image, prediction, title=image_path)
    return prediction


@click.command()
@click.argument('image_path', type=click.Path())
def main(image_path):
    predict_image(image_path)


if __name__ == '__main__':
    main()
