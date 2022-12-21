from configuration import config
from configuration.config import app as app
from pydantic import BaseModel


@app.get("/dummy-endpoint")
async def root():
    return {"message": "Hello from the fastAPI backend!"}


class Artist(BaseModel):
    name: str

class Song(BaseModel):
    name: str


@app.post("/search")
async def search(Song: Song, Artist: Artist):
    # search for song here 
    return {"Song": Song, "Artist": Artist}