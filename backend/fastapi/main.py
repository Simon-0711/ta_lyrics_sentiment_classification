from configuration import config
from configuration.config import app as app
from pydantic import BaseModel
import lyricsgenius as genius  # https://github.com/johnwmillr/LyricsGenius
from fastapi import FastAPI, HTTPException



@app.get("/dummy-endpoint")
async def root():
    return {"message": "Hello from the fastAPI backend!"}


class Body(BaseModel):
    song_name: str
    artist_name: str
    


@app.post("/search")
async def search(body: Body):
    """
        Function that gets song and artist name from frontend in JSON as such:
        {
            song_name: "songname",
            artist_name: "artist"
        }
    """
    # read in the api key after it has been encrypted by you
    with open('secrets/genius_api_secret', 'r') as file:
        api_token = file.read()

    song = body.song_name
    artist = body.artist_name

    api = genius.Genius(api_token)
    try:
        lyrics = api.search_song(song, artist)
    except:
        raise HTTPException(status_code=500, detail="Error during scraping of the lyrics")

    # return 404 if song not found
    if lyrics is None:
        raise HTTPException(status_code=404, detail="Lyrics for Song not found")

    
    # TODO: Send to elastic search
    return {"Song": song, "Artist": artist, "Lyrics": lyrics.lyrics}


