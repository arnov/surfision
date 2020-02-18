import os
import glob
import json
import random

from numpy import zeros
from numpy import asarray
from mrcnn.utils import Dataset, extract_bboxes
from mrcnn.visualize import display_instances


CLASSES = {1: 'surfer',
           2: 'kiter',
           3: 'windsurfer',
           4: 'walker',
           5: 'dog',
           6: 'supper'}


class SurfDataset(Dataset):
    def __init__(self):
        super().__init__()

        for id, cls in CLASSES.items():
            self.add_class('dataset', id, cls)

    def load_dataset(self, dataset_dir, is_train=True):
        files = sorted(glob.glob(f'{dataset_dir}/*.json'))
        for i, ann_path in enumerate(files):
            # Hacky train test split
            if is_train and i >= 160 or not is_train and i < 160:
                continue

            image_id, ext = ann_path.rsplit('.', 1)
            img_path = f'{image_id}.png'

            assert os.path.exists(img_path), f'{img_path} not found!'

            image_id = image_id.split('/')[1]

            self.add_image('dataset', image_id=image_id, path=img_path, annotation=ann_path)

    def load_mask(self, image_id):
        image_info = self.image_info[image_id]
        with open(image_info['annotation']) as f:
            annotation = json.load(f)

        shapes = annotation['shapes']

        masks = zeros([annotation['imageHeight'], annotation['imageWidth'],
                      len(annotation['shapes'])], dtype='uint8')

        class_ids = list()
        for i, shape in enumerate(shapes):
            row_ind = round(shape['points'][0][1]), round(shape['points'][1][1])
            col_ind = round(shape['points'][0][0]), round(shape['points'][1][0])
            row_s, row_e = min(row_ind), max(row_ind)
            col_s, col_e = min(col_ind), max(col_ind)
            masks[row_s:row_e, col_s:col_e, i] = 1
            class_ids.append(self.class_names.index(shape['label']))
        return masks, asarray(class_ids, dtype='int32')

    def image_reference(self, image_id):
        info = self.image_info[image_id]
        return info['path']


if __name__ == '__main__':
    dataset = SurfDataset()
    dataset.load_dataset('data')
    dataset.prepare()

    for image_id in random.sample(list(dataset.image_ids), 4):
        image = dataset.load_image(image_id)
        mask, class_ids = dataset.load_mask(image_id)
        bbox = extract_bboxes(mask)

        print(f'image {image_id}: {dataset.image_info[image_id]}')
        print(f'image shape: {image.shape}')
        print(f'mask shape: {mask.shape}')
        print(f'bbox shape: {bbox.shape}')

        display_instances(image, bbox, mask, class_ids, dataset.class_names,
                          title=dataset.image_info[image_id]['path'])
