from dotenv import load_dotenv
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl import functions
from telethon import TelegramClient
import os
import asyncio
from flask import Flask, request, jsonify
from functools import wraps
app = Flask(__name__)


load_dotenv()


api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
title = os.getenv('TITLE')
bot_token = os.getenv('BOT_TOKEN')


async def check_with_bot(client, username, group):
    try:
        if(not username.isnumberic()):

            result = await client(functions.channels.GetParticipantRequest(
                channel=group,
                participant=username
            ))
        else:
            _user = await client(GetFullUserRequest(int(username)))
            result = await client(functions.channels.GetParticipantRequest(
                channel=group,
                participant=_user.user.username
            ))
        if not result.participant:
            return False

        return True
    except Exception as e:
        return False


async def check(client, username, group):
    try:
        if not username.isnumeric():
            print(username)
            result = await client(functions.channels.GetParticipantRequest(
                channel=group,
                participant=username
            ))
        else:
            _user = await client(GetFullUserRequest(int(username)))
            result = await client(functions.channels.GetParticipantRequest(
                channel=group,
                participant=_user.user.username
            ))

        if not result.participant:
            return False

        return True
    except Exception as e:
        bot = await TelegramClient('epicwar_bot', api_id, api_hash).start(bot_token=bot_token)
        async with bot:
            data = await check_with_bot(bot, username, group)

        return data


def async_action(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapped


@app.route('/api/v1/telegram', methods=['POST'])
@async_action
async def checkJoinTelegram():
   

    try:
        data = request.json
        pattern = r't.me/'
        data['username'] = data['username'].split(pattern)[-1]
        bot = await TelegramClient('epicwar_bot', api_id, api_hash).start(bot_token=bot_token)
        async with bot:
            data = await check(bot, data['username'], data['channel'])

        return jsonify({'code': 0, 'data': data})
    except Exception:
        return jsonify({'code': 0, 'data': False})


app.run(host='127.0.0.1', port=8888, debug=True)
