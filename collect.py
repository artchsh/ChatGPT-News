import json
from datetime import datetime
import config
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)

# some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


# Setting configuration values
api_id = config.TELEGRAM_API_ID
api_hash = config.TELEGRAM_API_HASH
phone = config.TELEGRAM_PHONE
username = config.TELEGRAM_USERNAME
channel_url = username = config.TELEGRAM_CHANNEL_URLS[0]

# Create the client and connect
client = TelegramClient("./src/anon", api_id=api_id, api_hash=api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    # user_input_channel = input('enter entity(telegram URL or entity id):')
    user_input_channel = channel_url

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 50

    while True:
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            dict_message = message.to_dict()
            dict_message["message"].encode('utf-8')
            all_messages.append(dict_message)
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    print(f'Total collected messages: {total_messages}')

    with open('./src/channel_messages.json', 'w', encoding="utf-8") as outfile:
        json.dump(all_messages, outfile, cls=DateTimeEncoder)


def start():
    """Start to collect messages"""
    print("Starting Telegram Client")
    with client:
        client.loop.run_until_complete(main(phone))

start()