from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters

import asyncio
import aiohttp
import os
import aiofiles
import json

api_id = (2906995)
api_hash = "(0d5b69b23b2482aa8164b2e4b86be577)"

app = Client('session', api_id, api_hash, bot_token="1530382898:AAFnBO73Zz-xcTXRKQ9AvAw85o1NuehEb2w")

@app.on_message(filters.command('start') & filters.private)
async def start_command(client, message):
    await client.send_message(chat_id=message.chat.id, text=f"(Ciao!) {message.from_user.first_name}")

async def job():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://fortnite-api.com/v2/shop/br/combined') as resp:
            if resp.status == 200:
                data = await resp.json()
                if os.path.isfile('shop.json') is False:
                    async with aiofiles.open('shop.json', 'w+') as f:
                        await f.write(json.dumps(data))
                    return 0
                async with aiofiles.open('shop.json') as f:
                    old = json.loads(await f.read())

                if data != old:
                    # avviare itemshop.py -> subprocess.call('python itemshop.py', shell=True) / asyncio Thread o Subprocess
                    await app.send_photo(chat_id=(-1001414754637), photo='Athena-FNAPI.com-main/itemshop.jpeg', caption='')
                    async with aiofiles.open('shop.py', 'w+') as f:
                        await f.write(json.dumps(data))


scheduler = AsyncIOScheduler()
scheduler.add_job(job, "cron", hour=(1), minute=(0), second=(0))

scheduler.start()
app.run()
