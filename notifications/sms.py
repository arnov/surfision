import os
import messagebird

MESSAGEBIRD_KEY = os.getenv('MESSAGEBIRD_KEY')
ORIGINATOR = os.getenv('FROM_PHONE_NUMBER')


client = messagebird.Client(MESSAGEBIRD_KEY)


def send_sms(content, recipient):
    client.message_create(
      ORIGINATOR,
      recipient,
      content,
      {'reference': 'Foobar'}
    )


if __name__ == '__main__':
    send_sms('It\'s on!!!', ORIGINATOR)
