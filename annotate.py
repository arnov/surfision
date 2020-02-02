import os
import click
from random import shuffle


def annotate(f):
    base, ext = f.rsplit('.', 1)
    output_file = f'{base}.json'

    print(f'Annnotating {f}')
    if not os.path.exists(output_file):
        os.system(f'labelme {f} -O {output_file}')


@click.command()
@click.argument('image_path', type=click.Path(), required=False)
def main(image_path=None):
    if image_path:
        annotate(image_path)
        return

    dir = 'data'
    files = os.listdir(dir)
    shuffle(files)

    for f in files:
        annotate(dir + '/' + f)


if __name__ == '__main__':
    main()
