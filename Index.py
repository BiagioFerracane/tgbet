import os
import time
import pytz
from datetime import datetime, time as dtime
from telethon import TelegramClient, events

# ================= CONFIG =================
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

SESSION = "sessione"

GRUPPO_ID = [int(x.strip()) for x in os.environ["GRUPPO_ID"].split(",")]
DESTINATARIO = int(os.environ["DESTINATARIO"])

WAIT_TIME = 600  # 10 minuti
TIMEZONE = pytz.timezone("Europe/Rome")

START_TIME = dtime(8, 0)
END_TIME   = dtime(23, 59)
# =========================================

last_photo_time = {}

def bot_should_run():
    now = datetime.now(TIMEZONE).time()
    return START_TIME <= now <= END_TIME

client = TelegramClient(SESSION, API_ID, API_HASH)

@client.on(events.NewMessage(chats=GRUPPO_ID))
async def handler(event):
    if not bot_should_run():
        return

    msg = event.message
    chat_id = event.chat_id
    now = time.time()

    if msg.photo:
        await client.forward_messages(DESTINATARIO, msg)
        last_photo_time[chat_id] = now
        print("📸 Foto inoltrata")
        return

    if msg.text and chat_id in last_photo_time:
        if now - last_photo_time[chat_id] <= WAIT_TIME:
            await client.send_message(DESTINATARIO, msg.text)
            print("📝 Testo successivo inoltrato")

async def main():
    await client.start()
    print("🤖 Userbot avviato")
    await client.run_until_disconnected()

import asyncio
asyncio.run(main())
