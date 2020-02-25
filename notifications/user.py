import json
from datetime import date
import dateutil.parser


class User:
    def __init__(self, name, phone, cams, object_class, last_notification_send_at=None):
        self.name = name
        self.phone = phone
        self.cams = cams
        self.object_class = object_class

        if last_notification_send_at:
            last_notification_send_at = dateutil.parser.parse(last_notification_send_at)

        self.last_notification_send_at = last_notification_send_at

    def should_notify(self):
        if not self.phone:
            print('Skipping notification since we have no phone number')
            return False
        if not self.last_notification_send_at:
            return True

        if self.last_notification_send_at.date() == date.today():
            print('Skipping notification since we already notified today')
            return False
        return True

    @staticmethod
    def load_users():
        with open('notifications/config.jsonl') as f:
            lines = f.readlines()

        return [User(**json.loads(line)) for line in lines]

    @staticmethod
    def save_users(users):
        with open('notifications/config.jsonl', 'w') as f:
            for user in users:
                f.write(user.to_json() + '\n')

    def save(self):
        users = self.load_users()
        new_users = []
        for user in users:
            if user.name == self.name:
                new_users.append(self)
            else:
                new_users.append(user)

        self.save_users(new_users)

    def to_json(self):
        ts = None
        if self.last_notification_send_at:
            ts = self.last_notification_send_at.isoformat()
        return json.dumps({'name': self.name,
                           'phone': self.phone,
                           'cams': self.cams,
                           'object_class': self.object_class,
                           'last_notification_send_at': ts})

    def __repr__(self):
        return f'User("{self.name}")'
