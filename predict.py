from train import ModelConfig
from surf_dataset import CLASSES

from mrcnn.config import Config
from mrcnn.model import MaskRCNN, mold_image
from numpy import expand_dims
from matplotlib import pyplot
from matplotlib.patches import Rectangle

import click
import skimage


class PredictionConfig(Config):
    NAME = "surf_cfg"
    NUM_CLASSES = ModelConfig.NUM_CLASSES
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


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
    cfg = PredictionConfig()

    image = skimage.io.imread(image_path)
    image = image[:, :, 0:3]  # remove alpha

    scaled_image = mold_image(image, cfg)
    sample = expand_dims(scaled_image, 0)

    model = MaskRCNN(mode='inference', model_dir='./', config=cfg)
    model_path = 'mask_rcnn_surfision_cfg_0005_v2.h5'
    model.load_weights(model_path, by_name=True)

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
