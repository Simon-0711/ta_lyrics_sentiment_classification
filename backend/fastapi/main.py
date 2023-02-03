from configuration import config
from configuration.config import app as app
from pydantic import BaseModel
import lyricsgenius as genius  # https://github.com/johnwmillr/LyricsGenius
from data_processing.preprocessing import processing_pipeline
from fastapi import FastAPI, HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

import source.elasticsearch_functions as ef
import utils as utils

CNN_MODEL = "./cnn_model_v1"
TOKENIZER = "./data_processing/tokenizer.pickle"
LABELENCODER = "./data_processing/label_encoder.npy"


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
    with open("secrets/genius_api_secret", "r") as file:
        api_token = file.read()

    song = body.song_name.lower()
    artist = body.artist_name.lower()

    # song_lyrics = ef.get_stored_lyrics_of_song(song, artist)
    song_lyrics = "Not None"

    if song_lyrics is None:
        print("The song was not found ... fetching")
        api = genius.Genius(api_token)
        try:
            lyrics = api.search_song(song, artist)
        except:
            raise HTTPException(
                status_code=500, detail="Error during scraping of the lyrics"
            )

        # return 404 if song not found
        if lyrics is None:
            raise HTTPException(status_code=404, detail="Lyrics for Song not found")

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

        # TODO: Search top 3 similar songs based on mood and lyrics and return in the followin structure:
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
    # TODO: Replace fixed dict with variable song_dictionary
    return {
        "similar_songs": {
            "similar_song_1": {
                "Song": "Like Toy Soldiers",
                "Artist": "Eminem",
            },
            "similar_song_2": {
                "Song": "Ass Like That",
                "Artist": "Eminem",
            },
            "similar_song_3": {
                "Song": "More Ass Like That",
                "Artist": "Eminem",
            },
        },
        "mood": "sad",
    }


def sklearn_cosine(x: np.array, y: np.array) -> int:
    """is a function that takes in two arguments, x and y,
    and returns the cosine similarity between them as calculated by
    the cosine_similarity function from the scikit-learn library.

    :param x: first vector
    :type x: np.array
    :param y: second vector
    :type y: np.array
    :return: scalar similarity value
    :rtype: int
    """
    return cosine_similarity([x], [y])


def get_top_n_similar(
    song_to_compare: dict, songs_to_compare_to: dict, top_n_simlar: int = 3
) -> list:
    """This function takes in three parameters: song_to_compare, songs_to_compare_to, and top_n_similar,
    and returns a list of top n most similar songs based on the cosine similarity score between their vectorized lyrics.
    The function first calculates the cosine similarity score between the vectorized lyric of song_to_compare and each of
    the songs in songs_to_compare_to using the sklearn_cosine function.
    It then filters out any scores equal to 1 (which would mean that the same song was found in songs_to_compare_to).
    The indexes of the top n scores are then found and the corresponding song information (song name and artist name)
    is returned in the form of a list.

    :param song_to_compare: lyric to find similar songs for
    :type song_to_compare: dict
    :param songs_to_compare_to: lyrics of songs to compare to song_to_compare
    :type songs_to_compare_to: dict
    :param top_n_simlar: number of most similar songs to return
    :type top_n_simlar: int
    :return: list of top n most similar songs containing song name and artist name
    :rtype: list
    """
    cosine_similarity_scores = []

    # calculate similarity score for each passed vectorized lyrics with gold_song
    for key, value in songs_to_compare_to.items():
        # calculate similarity score
        similarity_score = sklearn_cosine(
            song_to_compare["Vectorized_lyric"], value["Vectorized_lyric"]
        )[0][0]
        # filter similarity score = 1
        # this would mean, that somehow, the same song was found in the songs to compare
        if similarity_score == 1:
            similarity_score = 0
        # Add score to list of all scores
        cosine_similarity_scores.append(similarity_score)
    cosine_similarity_scores = np.array(cosine_similarity_scores)

    # get indexes of top n values
    indexes_top_n = np.argsort(cosine_similarity_scores)[::-1][:top_n_simlar]
    # get top n dictionary keys
    top_n_keys = np.array(list(songs_to_compare_to))[indexes_top_n]
    # get top n dict entries
    top_n_dict = {key: songs_to_compare_to[key] for key in top_n_keys}
    # remove lyrics from dict
    top_n_songs_no_lyrics = {
        key: {"Song": value["Song"], "Artist": value["Artist"]}
        for key, value in top_n_dict.items()
    }

    return top_n_songs_no_lyrics


def get_tf_idf_vectorized_lyrics(song_to_compare: dict, mood: str) -> tuple[dict, dict]:
    """Function that returns the tf-idf vectors for given lyrics.

    :param song_to_compare: dict with song name, artist name and lyrics for song to compare with.
    :param mood: mood of the song to compare with. # TODO: Add mood to first input parameter?

    :return: dict for the song we want to compare each lyrics of certain mood with. It contains information on the song name, artist name, lyrics and vectorized lyric.
    :rtype: dict
    :return: dict with dicts that contain song name, artist name, lyrics and vectorized lyrics for each song of given mood (except of the song to compare with).
    :rtype: dict
    """

    # get documents with songs that have the same mood
    song_same_mood_dict = ef.get_all_documents_of_mood(mood)

    # check if song to compare with is within the song_same_mood_dict. If not add it for tf-idf vectorization
    song_to_compare_key = f'{song_to_compare["Song"]}_{song_to_compare["Artist"]}'
    if song_to_compare_key not in song_same_mood_dict.keys():
        song_same_mood_dict[song_to_compare_key] = song_to_compare

    # get list of all lyrics of songs with same mood
    lyrics_list = [document["Lyrics"] for document in song_same_mood_dict.values()]

    # initialize TfidfVectorizer # TODO: Maybe add more parameters or adjust current ones
    tfidf_vectorizer = TfidfVectorizer(
        analyzer="word", lowercase=True, stop_words="english", min_df=5
    )
    # generate tdf-idf scores
    lyrics_tf_idf = tfidf_vectorizer.fit_transform(lyrics_list)

    # reduce the dimensionality of the tf-idf vectors
    SVD = TruncatedSVD(
        n_components=300, random_state=42  # number of output dimensionalities
    )
    vectorized_lyrics = SVD.fit_transform(
        lyrics_tf_idf
    )  # TODO: check the dimension. Should be (#documents, 300)

    for key, vectorized_lyric in zip(
        list(song_same_mood_dict.keys()), vectorized_lyrics
    ):  # TODO: check if I am adding the rows instead of the columns of vectorized_lyrics
        song_same_mood_dict[key]["Vectorized_lyric"] = vectorized_lyric

    song_to_compare = song_same_mood_dict.pop(song_to_compare_key)

    return song_to_compare, song_same_mood_dict


def get_similar(song_to_compare: dict, mood: str) -> dict:
    """This function gets top n similar song names and artist names based on passed
    song_to_compare and mood.
    First it searches all songs with the same mood and vectorizes their lyrics with TD-IDF.
    After that, the top n similar songs are filtered using TD-IDF.

    :param song_to_compare: Song to find similar songs for
    :type song_to_compare: dict
    :param mood: mood of song to find dimilar songs for
    :type mood: str
    :return: Dictionary containing top n similar songs
    :rtype: tuple[dict, dict]
    """

    # Get all songs with same mood and vectorize all song lyrics with TD-IDF
    song_to_compare, songs_to_compare_to = get_tf_idf_vectorized_lyrics(
        song_to_compare=song_to_compare, mood=mood
    )

    # Get top n most similar song names and artist names based on cosine similarity
    top_n_songs_no_lyrics = get_top_n_similar(
        song_to_compare=song_to_compare, songs_to_compare_to=songs_to_compare_to
    )

    # Add mood to dictionary
    similar_songs = {"similar_songs": top_n_songs_no_lyrics, "mood": mood}

    return similar_songs


def classify(song_dictionary):
    import tensorflow as tf
    import pickle
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from sklearn import preprocessing
    import numpy

    # preprocess the song
    preprocessed_lyrics = processing_pipeline(song_dictionary)

    # load the tokenizer
    with open(TOKENIZER, "rb") as handle:
        tokenizer = pickle.load(handle)
    # tokenize
    text = tokenizer.texts_to_sequences([preprocessed_lyrics["Lyrics"]])
    text = pad_sequences(text, 180)
    # predict the mood
    model = tf.keras.models.load_model(CNN_MODEL)
    prediction = model.predict(text)
    predicted_mood = numpy.argmax(prediction, axis=1)

    # load the label encoder
    encoder = preprocessing.LabelEncoder()
    encoder.classes_ = numpy.load(LABELENCODER, allow_pickle=True)
    # transform the prediciton to an actual mood
    mood = encoder.inverse_transform(predicted_mood)[0]
    song_dictionary["Mood"] = mood
    return mood
