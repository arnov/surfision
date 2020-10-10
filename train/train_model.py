from predict.predict_image import ModelConfig, PredictionConfig

import click
from mrcnn.model import MaskRCNN
from train.surf_dataset import SurfDataset
from train.evaluate import evaluate_model


@click.option('--continue_training', default=False)
def main(continue_training=False):
    # prepare train set
    train_set = SurfDataset()
    train_set.load_dataset('data', is_train=True)
    train_set.prepare()
    print('Train: %d' % len(train_set.image_ids))

    # prepare test/val set
    test_set = SurfDataset()
    test_set.load_dataset('data', is_train=False)
    test_set.prepare()
    print('Test: %d' % len(test_set.image_ids))

    # Make sure there is no overlap
    train_ids = {i['id'] for i in train_set.image_info}
    test_ids = {i['id'] for i in test_set.image_info}
    assert len(train_ids & test_ids) == 0

    # prepare config
    config = ModelConfig()
    config.display()

    # define the model
    model = MaskRCNN(mode='training', model_dir='./', config=config)
    model.keras_model.metrics_tensors = []

    # load weights (mscoco) and exclude the output layers
    if continue_training:
        model.load_weights(
            'mask_rcnn_surfision_cfg_0005_v5.h5', by_name=True)
    else:
        model.load_weights(
            'mask_rcnn_coco.h5', by_name=True,
            exclude=["mrcnn_class_logits", "mrcnn_bbox_fc",  "mrcnn_bbox", "mrcnn_mask"])

    # train weights (output layers or 'heads')
    model.train(train_set, test_set, learning_rate=config.LEARNING_RATE, epochs=8, layers='heads')

    cfg = PredictionConfig()
    test_mAP = evaluate_model(test_set, model, cfg)
    print('Test mAP: %.3f' % test_mAP)


if __name__ == '__main__':
    main()
