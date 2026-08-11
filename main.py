import os,sys,logging,asyncio
from pyrogram import Client

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger=logging.getLogger(__name__)

APP_NAME="KurupDevs"
API_ID=int(os.getenv("API_ID","0"))
API_HASH=os.getenv("API_HASH","")

app=Client("kurupdevs",api_id=API_ID,api_hash=API_HASH)

async def main():
 logger.info(f"Starting {APP_NAME}...")
 await app.start()
 logger.info(f"{APP_NAME} is running!")
 await asyncio.Event().wait()

if __name__=="__main__":asyncio.run(main())
