from elasticsearch import Elasticsearch

# Initialize id counter
id_counter = 0

index_name = "lyrics_mood_classification"


def add_es_document(song_name, artist_name, lyrics, mood):
    # TODO: Edit docstring
    """Scrape lyrcis on Genius and returns the lyrics.

    :param song_name: song name of the lyrics we want to scrape.
    :param artist_name: artist name of the lyrics we want to scrape.

    :return: Lyrics of given song and artist name.
    :rtype: String or None
    """

    # TODO: Add authentication for elasticsearch?
    es_host = "http://localhost:9200"

    es = Elasticsearch(
        hosts=es_host
    )

    # Add document to index
    es.create(index=index_name,
              id=str(id_counter),
              document={
                  "song_name": song_name,
                  "artist_name":  artist_name,
                  "lyrics": lyrics,
                  "mood": mood
              })
    id_counter += 1


def get_stored_mood_of_song(song_name, artist_name):
    # TODO: Edit docstring
    """Search in Elasticsearch index for the song and returns the mood if.

    :param song_name: song name of the lyrics we want to scrape.
    :param artist_name: artist name of the lyrics we want to scrape.

    :return: Lyrics of given song and artist name.
    :rtype: String or None
    """

    # TODO: Add authentication for elasticsearch?
    es_host = "http://localhost:9200"

    es = Elasticsearch(
        hosts=es_host
    )

    # Check index for new song
    # TODO: Could also use match instead of query for better chances to find the document if song_name in es contains, e.g. feat artist in song name
    result = es.search(index=index_name, query={"bool": {"must": [
        {"term": {"song_name": song_name}}, {"term": {"artist_name": artist_name}}]}})

    # TODO: Return the mood from the result
    # return


def get_stored_lyrics_of_song(song_name, artist_name):
    # TODO: Edit docstring
    """Search in Elasticsearch index for the song and returns the mood if.

    :param song_name: song name of the lyrics we want to scrape.
    :param artist_name: artist name of the lyrics we want to scrape.

    :return: Lyrics of given song and artist name.
    :rtype: String or None
    """

    # TODO: Add authentication for elasticsearch?
    es_host = "http://localhost:9200"

    es = Elasticsearch(
        hosts=es_host
    )

    # Check index for new song
    # TODO: Could also use match instead of query for better chances to find the document if song_name in es contains, e.g. feat artist in song name
    result = es.search(index=index_name, query={"bool": {"must": [
        {"term": {"song_name": song_name}}, {"term": {"artist_name": artist_name}}]}})

    # TODO: Return the lyrics from the result
    # return
