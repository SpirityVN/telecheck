import os
from telethon import TelegramClient
from telethon.tl import functions
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.users import GetFullUserRequest, GetUsersRequest
from dotenv import load_dotenv
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

load_dotenv()


api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
title = os.getenv('TITLE')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('spirity', api_id=api_id, api_hash=api_hash)

bot = TelegramClient('spirity_bot', api_id=api_id,
                     api_hash=api_hash).start(bot_token=bot_token)


async def check_with_bot(client, username, group):
    try:
        result = await client(functions.channels.GetParticipantRequest(
            channel=group,
            participant=username
        ))
        if not result.participant:
            return False

        return True
    except Exception as e:
        return False


async def check(client, username, group):
    try:
        result = await client(functions.channels.GetParticipantRequest(
            channel=group,
            participant=username
        ))

        if not result.participant:
            return False

        return True
    except Exception as e:
        bot = await TelegramClient('epicwar_bot', api_id, api_hash).start(bot_token=bot_token)
        async with bot:
            data = await check_with_bot(bot, username, group)

        return data

# https://t.me/EpicWarAnnouncement
async def main():
    channelName = 'epicwarglobal'
    # userName = '1775398111'
    userName=1173630950
    channel = await bot(ResolveUsernameRequest(channelName))
    users = await bot(GetFullUserRequest(userName))
    print(users.user.username)
    # print(channel)
    data = await check(bot, userName, channel)
    print(channel.peer.channel_id)
    print(data)
    print(users.user.id)
    # if(data):
    #     key = 'telegram' + ':' + str(channel.peer.channel_id) + ':' + str(users.user.id)
    #     r.set(key, 1) # TODO: 1 = timestamp
with bot:
    bot.loop.run_until_complete(main())
