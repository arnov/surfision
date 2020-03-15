from predict.predict_image import PredictionConfig, load_model
from train.surf_dataset import SurfDataset

import numpy as np
from mrcnn.utils import compute_ap
from mrcnn.model import load_image_gt
from mrcnn.model import mold_image


def evaluate_model(dataset, model, cfg):
    APs = []
    for image_id in dataset.image_ids:
        # load image, bounding boxes and masks for the image id
        image, image_meta, gt_class_id, gt_bbox, gt_mask = load_image_gt(
            dataset, cfg, image_id, use_mini_mask=False)

        # convert pixel values (e.g. center)
        scaled_image = mold_image(image, cfg)
        sample = np.expand_dims(scaled_image, 0)
        # make prediction
        yhat = model.detect(sample, verbose=0)

        for r in yhat:
            AP, _, _, _ = compute_ap(gt_bbox, gt_class_id, gt_mask, r['rois'],
                                     r['class_ids'], r['scores'], r['masks'])
            if not np.isnan(AP):
                APs.append(AP)

    mAP = np.mean(APs)
    return mAP


def evaluate():
    train_set = SurfDataset()
    train_set.load_dataset('data', is_train=True)
    train_set.prepare()
    print('Train: %d' % len(train_set.image_ids))

    # load the test dataset
    test_set = SurfDataset()
    test_set.load_dataset('data', is_train=False)
    test_set.prepare()
    print('Test: %d' % len(test_set.image_ids))

    cfg = PredictionConfig()
    model = load_model(cfg)

    test_mAP = evaluate_model(test_set, model, cfg)
    print('Test mAP: %.3f' % test_mAP)

    train_mAP = evaluate_model(train_set, model, cfg)
    print('Train mAP: %.3f' % train_mAP)


if __name__ == '__main__':
    evaluate()
