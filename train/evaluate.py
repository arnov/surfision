from collections import defaultdict
from copy import copy

from predict.predict_image import PredictionConfig, load_model
from train.surf_dataset import SurfDataset, CLASSES

import numpy as np
from mrcnn.model import load_image_gt
from mrcnn.model import mold_image


def get_correct(y_true, y_pred):
    y_true = copy(y_true)

    correct = 0
    for pred in y_pred:
        if pred in y_true:
            correct += 1
            y_true.remove(pred)

    return correct


def precision_score(y_true, y_pred, classes=None):
    if classes:
        y_true = [c for c in y_true if c in classes]
        y_pred = [c for c in y_pred if c in classes]

    if not y_pred:
        return np.nan

    return get_correct(y_true, y_pred) / len(y_pred)


def recall_score(y_true, y_pred, classes=None):
    if classes:
        y_true = [c for c in y_true if c in classes]
        y_pred = [c for c in y_pred if c in classes]

    if not y_true:
        return np.nan

    return get_correct(y_true, y_pred) / len(y_true)


def evaluate_model(dataset, model, cfg, verbose=False):
    results = defaultdict(list)

    for image_id in dataset.image_ids:
        # load image, bounding boxes and masks for the image id
        image, image_meta, gt_class_id, gt_bbox, gt_mask = load_image_gt(
            dataset, cfg, image_id, use_mini_mask=False)

        # convert pixel values (e.g. center)
        scaled_image = mold_image(image, cfg)
        sample = np.expand_dims(scaled_image, 0)
        # make prediction
        preds = model.detect(sample, verbose=0)[0]

        y_true = [CLASSES[class_id] for class_id in gt_class_id]
        y_pred = [CLASSES[class_id] for class_id in preds['class_ids']]

        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)

        surf_classes = ['surfer', 'supper']
        precision_surfer = precision_score(y_true, y_pred, surf_classes)
        recall_surfer = recall_score(y_true, y_pred, surf_classes)

        if verbose:
            info = dataset.image_info[image_id]
            print(f'Image_id: {image_id} Path: {info["path"]}')
            print(f'y_true: {y_true}')
            print(f'y_pred: {y_pred}')
            print(f'Precision: {precision}')
            print(f'Recall: {recall}')
            print(f'Precision surfers: {precision_surfer}')
            print(f'Recall surfers: {recall_surfer}')
            print()

        if not np.isnan(precision):
            results['precision'].append(precision)
        if not np.isnan(recall):
            results['recall'].append(recall)
        if not np.isnan(precision_surfer):
            results['precision_surfer'].append(precision_surfer)
        if not np.isnan(recall_surfer):
            results['recall_surfer'].append(recall_surfer)

    print(f'Precision: {np.mean(results["precision"])}')
    print(f'Recall: {np.mean(results["recall"])}')
    print()
    print(f'Precision surfers: {np.mean(results["precision_surfer"])}')
    print(f'Recall surfers: {np.mean(results["recall_surfer"])}')


def evaluate():
    test_set = SurfDataset()
    test_set.load_dataset('data', is_train=False)
    test_set.prepare()
    print('Test: %d' % len(test_set.image_ids))

    cfg = PredictionConfig()

    paths = ['mask_rcnn_surfision_cfg_0005_v2.h5',
             'mask_rcnn_surfision_cfg_0005_v3.h5',
             'mask_rcnn_surfision_cfg_0005_v4.h5',
             'mask_rcnn_surfision_cfg_0005_v5.h5',
             'surfision_cfg20200411T1437/mask_rcnn_surfision_cfg_0005.h5',
             'surfision_cfg20200412T1110/mask_rcnn_surfision_cfg_0006.h5',
             'surfision_cfg20200412T1110/mask_rcnn_surfision_cfg_0007.h5']
    for model_path in paths:
        model = load_model(cfg, model_path)
        evaluate_model(test_set, model, cfg, verbose=False)
        print(f'Done evaluation {model_path}\n')


if __name__ == '__main__':
    evaluate()
