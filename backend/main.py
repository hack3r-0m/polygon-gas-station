import os
import redis
import requests
import threading
import multiprocessing as mp
import caching
from fastapi import FastAPI
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
r = redis.Redis(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), password=os.getenv('DB_PASSWORD'),
    decode_responses=True)
s = requests.Session()

cron = mp.Process(target=caching.set_last_block, daemon=True)
cron.start()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/gas_overview")
async def fetch_from_oracle():
    return s.get("https://gasstation-mainnet.matic.network").json()

@app.get("/last_block")
async def last_block():
    return r.get("last_included_block")

@app.get("/debug")
async def check():
    return cron.pid
