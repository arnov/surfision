import pandas as pd
from datetime import datetime, timedelta


def main():
    df = pd.read_csv('predictions.csv')

    one_hour_ago = datetime.now() - timedelta(hours=1)
    df = df[df['timestamp'] > str(one_hour_ago)]

    avg_surfers = df.groupby('cam')['surfer'].mean()
    avg_surfers = avg_surfers[avg_surfers > 3]

    if avg_surfers.empty:
        print('Not enough surfers found!')
        return

    message = 'Ze liggen er in hoor!\n'
    for cam, avg in avg_surfers.to_dict().items():
        message += f'{cam}: ~{round(avg)} surfers\n'
    print(message)


if __name__ == '__main__':
    main()
