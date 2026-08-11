import os,asyncio,logging
from pyrogram import Client

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger=logging.getLogger(__name__)

app=Client("kurupdevs",api_id=int(os.getenv("API_ID","0")),api_hash=os.getenv("API_HASH",""))

async def main():
 logger.info("Starting KurupDevs...")
 await app.start()
 logger.info("KurupDevs running!")
 await asyncio.Event().wait()

if __name__=="__main__":asyncio.run(main())
