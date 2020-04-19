import os
import glob
import click
from random import shuffle


def annotate(f):
    base, ext = f.rsplit('.', 1)
    output_file = f'{base}.json'

    if not os.path.exists(output_file):
        print(f'Annnotating {f}')
        os.system(f'labelme {f} -O {output_file}')


@click.command()
@click.argument('image_path', type=click.Path(), required=False)
def main(image_path=None):
    if image_path:
        annotate(image_path)
        return

    dir = 'data'
    files = glob.glob(f'{dir}/*.png') + glob.glob(f'{dir}/train/*.jpg')
    shuffle(files)

    for f in files:
        annotate(f)


if __name__ == '__main__':
    main()
