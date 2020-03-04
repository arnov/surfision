import random
import pandas as pd
from datetime import datetime, timedelta

from notifications.sms import send_sms
from notifications.user import User
from fetch.fetch_data import get_cam


MESSAGES = ['Ze liggen er in hoor!',
            'Gaan als ze staan!',
            'It\'s on!',
            'Surf\'s up!',
            'Ik zou me ziek melden!',
            'Waarom lig jij er niet in?!',
            'Hey ho! Let\'s go!',
            'Er zijn surfers gevonden.',
            'Waves!',
            'Spullen pakken!',
            'Wetsuit aan!',
            'Waxen!',
            'Maak ff je agenda snel leeg!']


def get_avg_objects(object_class, cams, hours_ago=1):
    df = pd.read_csv('predictions.csv')

    one_hour_ago = datetime.now() - timedelta(hours=hours_ago)
    df = df[(df['timestamp'] > str(one_hour_ago)) & df['cam'].isin(cams)]

    return df.groupby('cam')[object_class].mean()


def notify(user):
    print(f'Checking if we should notify user {user.name}')
    avg_objects = get_avg_objects(user.object_class, user.cams)
    avg_objects = avg_objects[avg_objects > user.threshold]

    if avg_objects.empty:
        print('Not enough surfers found!')
        return

    message = random.sample(MESSAGES, 1)[0] + '\n'
    for cam_id, avg in avg_objects.to_dict().items():
        cam = get_cam(cam_id)
        message += f'{cam.name}: ~{round(avg)} {user.object_class}s\n'

    if user.should_notify():
        print('Sending message')
        user.last_notification_send_at = datetime.now()
        send_sms(message, user.phone)
        user.save()


if __name__ == '__main__':
    for user in User.load_users():
        notify(user)
