from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import httpx
from models import Player
from tasks import parse_player_data
from cslog import logger
import uvicorn

from fake_useragent import UserAgent

app = FastAPI()
URL = "https://csstats.gg/player"

# Fake User Agent
ua = UserAgent()
header = {"User-Agent": ua.random}


async def fetch_player_data(player_id: str, retries=5) -> Player:
    async with httpx.AsyncClient() as client:
        for attempt in range(retries + 1):
            resp = await client.get(f"{URL}/{player_id}", headers=header, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, "lxml")
                data = await parse_player_data(soup)
                return data
            elif attempt < retries:
                logger.warning(f"Attempt {
                    attempt + 1} failed with status code {resp.status_code}, retrying...")
        logger.error(f"Status Code: {resp.status_code}")
        raise HTTPException(status_code=resp.status_code,
                            detail="Player Not found")


@app.get("/players/{player_id}")
async def get_csstats(player_id):
    rank = await fetch_player_data(player_id)
    return rank

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)
