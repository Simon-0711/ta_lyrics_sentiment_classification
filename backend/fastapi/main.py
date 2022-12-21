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
    """
        Function that gets song and artist name from frontend in JSON as such:
        {
            "Song": {
                "name": "ABCD"
            },
            "Artist": {
                "name": "Artist_name"
            }
        }
    """
    # search for song here 
    return {"Song": Song, "Artist": Artist}