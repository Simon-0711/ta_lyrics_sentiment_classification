from configuration import config
from configuration.config import app as app
from pydantic import BaseModel
import lyricsgenius as genius  # https://github.com/johnwmillr/LyricsGenius


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
    # read in the api key after it has been encrypted by you
    with open('secrets/genius_api_secret', 'r') as file:
        api_token = file.read()

    api = genius.Genius(api_token)
    try:
        lyrics = api.search_song(Song.name, Artist.name)
    except:
        raise HTTPException(status_code=500, detail="Error during scraping of the lyrics")

    # return 404 if song not found
    if lyrics is None:
        raise HTTPException(status_code=404, detail="Lyrics for Song not found")


    # TODO: Send to elastic search
    return {"Song": Song, "Artist": Artist, "Lyrics": lyrics.lyrics}


