import os
from random import shuffle


def main():
    dir = 'data'
    files = os.listdir(dir)
    shuffle(files)

    for f in files:
        base, ext = f.rsplit('.', 1)
        input_file = f'{dir}/{f}'
        output_file = f'{dir}/{base}.json'

        print(f'Annnotating {input_file}')
        if not os.path.exists(output_file):
            os.system(f'labelme {input_file} -O {output_file}')


if __name__ == '__main__':
    main()
