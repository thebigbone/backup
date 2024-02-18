import logging
import subprocess
import asyncio
from telegram import Bot
import os
from datetime import datetime

now = datetime.now()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot_token = 'token'
chat_id = 'chat_id'

bot = Bot(token=bot_token)

async def send_notification(success):
    try:
        if success:
            message = f'backup job completed at {now}. \n {success}. \ndoing rsync transfer now.'
        else:
            message = "backup job failed to execute."

        await bot.send_message(chat_id=chat_id, text=message)
        logging.info("notification sent successfully!")

    except Exception as e:
        logging.error(f"failed to send notification: {e}")

async def send_rsync_notification(success):
    try:
        if success:
            message = f'rsync transfer complete to crunchbits server. \n{success}'
        else:
            message = "rsync transfer failed."

        await bot.send_message(chat_id=chat_id, text=message)
        logging.info("notification sent successfully!")

    except Exception as e:
        logging.error(f"failed to send notification: {e}")

async def execute_command():
    try:
        cmd = "sh $HOME/restic.sh"
        result = await asyncio.create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await result.communicate()
        return stdout.decode().strip()
    except Exception as e:
        logging.error(e)
        return None

async def execute_rsync():
    try:
        cmd = "sh $HOME/rsync.sh"
        result = await asyncio.create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await result.communicate()
        return stdout.decode().strip()
    except Exception as e:
        logging.error(e)
        return None

async def main():

    success = await execute_command()

    await send_notification(success)

    rsync_transfer = await execute_rsync()
    
    await send_rsync_notification(rsync_transfer)

if __name__ == "__main__":
    asyncio.run(main())

