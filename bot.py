import discord
import logging
from creds import settings_first_run, setup_settings, change_settings
import json
from authflow import print_auth_url
from login import login
from discord.ext import tasks, commands
import os
from ssoresponse import handle_sso_token_response
from tokenrefresh import revoke_refresh_token
from commands import wallet, get_skills, get_standings, parse_broker, parse_corp, parse_faction, brokerfee, trade

intents = discord.Intents.default()
intents.members = True
intents.messages = True

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

with open('discord.json', 'r') as g:
    g_load = json.load(g)
    bot_token = g_load['bot_token']

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    get_skills()
    get_standings()
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.reply('Hello!', mention_author = True)

    if message.content.startswith('!setup'):
        settings_first_run() 
    
    if message.content.startswith('!settings'):
        with open('settings.json', 'r') as f:
            d = json.loads(f.read())
            settings = d['settings'][0]["client_id"], d['settings'][0]["client_secret"], d['settings'][0]["callback_url"]
        await message.reply(settings, mention_author = True)
        
    if message.content.startswith('!login'):
        res = print_auth_url()
        await message.reply(res, mention_author = True)
        m = await client.wait_for('message', check=None, timeout=30)
        auth_code = m.content
        red = login(auth_code)
        await message.channel.send(red)
        await message.channel.send('Logged in!')
        refreshtoken.start()

    if message.content.startswith('!refreshtoken'):
        with open('token.json', 'r') as r:
            h = json.loads(r.read())
            refresh_token = h['refresh_token']
        with open('settings.json', 'r') as a:
            b = json.load(a)
            client_id = b['settings'][0]["client_id"]
            client_secret = b['settings'][0]["client_secret"]
        rem = revoke_refresh_token(refresh_token=refresh_token, client_id=client_id, client_secret=client_secret)
        await message.channel.send(rem)

    if message.content.startswith('!balance'):
        res = wallet()
        await message.channel.send(res)

    if message.content.startswith('!skills'):
        res = get_skills()
        await message.channel.send(res)

    if message.content.startswith('!standings'):
        res = get_standings()
        await message.channel.send(res)

    if message.content.startswith('!broker'):
        res = brokerfee()
        await message.channel.send(res)

    if message.content.startswith('!'):
        await message.channel.send("Buy:")
        buy = await client.wait_for('message', check=None, timeout=30)
        await message.channel.send("Sell:")
        sell = await client.wait_for('message', check=None, timeout=30)
        buyint = float(buy.content)
        sellint = float(sell.content)
        trading = trade(buy=buyint, sell=sellint)
        if trading > 0:
            await message.channel.send("`\U0001F44D Your profit is: {}`".format(f"{trading:,}"))
        else:
            await message.channel.send("`\U0001F6D1 Your loss is: {}`".format(f"{trading:,}"))

@tasks.loop(minutes=18)
async def refreshtoken():
    with open('token.json', 'r') as r:
            h = json.loads(r.read())
            refresh_token = h['refresh_token']
    with open('settings.json', 'r') as a:
            b = json.load(a)
            client_id = b['settings'][0]["client_id"]
            client_secret = b['settings'][0]["client_secret"]
    rem = revoke_refresh_token(refresh_token=refresh_token, client_id=client_id, client_secret=client_secret)
    print(rem)


client.run(bot_token)