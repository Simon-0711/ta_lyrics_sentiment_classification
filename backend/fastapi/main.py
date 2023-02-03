from configuration import config
from configuration.config import app as app
from pydantic import BaseModel
import lyricsgenius as genius  # https://github.com/johnwmillr/LyricsGenius
from data_processing.preprocessing import processing_pipeline
from fastapi import FastAPI, HTTPException
import source.elasticsearch_functions as ef
import utils as utils

CNN_MODEL = './cnn_model_v1'
TOKENIZER = './data_processing/tokenizer.pickle'
LABELENCODER = './data_processing/label_encoder.npy'

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

    song = body.song_name.lower()
    artist = body.artist_name.lower()

    song_lyrics = ef.get_stored_lyrics_of_song(song, artist)

    if song_lyrics is None:
        print("The song was not found ... fetching")
        api = genius.Genius(api_token)
        try:
            lyrics = api.search_song(song, artist)
        except:
            raise HTTPException(
                status_code=500, detail="Error during scraping of the lyrics")

        # return 404 if song not found
        if lyrics is None:
            raise HTTPException(
                status_code=404, detail="Lyrics for Song not found")

        # Classify the mood 
        print(lyrics.artist.lower())
        print("#####################################")
        print(lyrics.title.lower())
        # set the artist and song name to the found one, 
        # since genius package can search on only a substring and this would lead to errors in the end
        song = lyrics.title.lower()
        artist = lyrics.artist.lower()
        lyrics.lyrics = utils.chorus_normalization(lyrics.lyrics.lower())
        song_dictionary = {"Song": song, "Artist": artist, "Lyrics": lyrics.lyrics, "Mood": "none"}
        mood = classify(song_dictionary)

        # Send to elastic search
        # TODO which lyrics to save ? Whole lyrics or the preprocessed ones ?
        # When preprocessed the else block does not need a preprocessing 
        ef.add_es_document(song, artist, lyrics.lyrics, mood)
    else:
        print("The song was found")
        mood = ef.get_stored_mood_of_song(song, artist)
        song_dictionary = {"Song": song, "Artist": artist, "Lyrics": song_lyrics.lower(), "Mood": mood}

    # search similar songs
    # get_similar()
    # debug log
    print(f"The song: {song_dictionary['Song']} was labeled: {song_dictionary['Mood']}")
    return song_dictionary


def get_similar():
    return 0

def classify(song_dictionary):
    import tensorflow as tf
    import pickle
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from sklearn import preprocessing
    import numpy

    # preprocess the song
    preprocessed_lyrics = processing_pipeline(song_dictionary)

    #load the tokenizer
    with open(TOKENIZER, 'rb') as handle:
        tokenizer = pickle.load(handle)
    # tokenize
    text = tokenizer.texts_to_sequences([preprocessed_lyrics["Lyrics"]])
    text = pad_sequences(text, 180)
    # predict the mood
    model = tf.keras.models.load_model(CNN_MODEL)
    prediction = model.predict(text)
    predicted_mood=numpy.argmax(prediction,axis=1)

    # load the label encoder
    encoder = preprocessing.LabelEncoder()
    encoder.classes_ = numpy.load(LABELENCODER, allow_pickle=True)
    # transform the prediciton to an actual mood
    mood = encoder.inverse_transform(predicted_mood)[0]
    song_dictionary["Mood"] = mood
    return mood

    