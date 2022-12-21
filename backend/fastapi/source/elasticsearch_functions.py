from elasticsearch import Elasticsearch

# Set Elasticsearch index name
index_name = "lyrics_mood_classification"

# Initialize id counter
id_counter = 0


def add_es_document(song_name, artist_name, lyrics, mood):
    """Add document to Elasticsearch index.

    :param song_name: song name of the document entry.
    :param artist_name: artist name of the document entry.
    :param lyrics: artist name of the document entry.
    :param mood: mood of the document entry.
    """

    global id_counter, index_name

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

    # TODO: Add return with information if adding document worked or not


def get_stored_mood_of_song(song_name, artist_name):
    """Search in Elasticsearch index for the song and return the mood if already stored.

    :param song_name: song name of the document entry.
    :param artist_name: artist name of the document entry.

    :return: Mood of given song and artist name if stored in Elasticsearch index. Else None.
    :rtype: String or None
    """

    global index_name

    # TODO: Add authentication for elasticsearch?
    es_host = "http://localhost:9200"

    es = Elasticsearch(
        hosts=es_host
    )

    # Search for song in es index
    # TODO: Change "match" to "term"?
    result = es.search(index=index_name, query={"bool": {"must": [
        {"match": {"song_name": song_name}}, {"match": {"artist_name": artist_name}}]}})

    # Check if a song has been found
    if result["hits"]["total"]["value"] > 0:
        # TODO: How to handle multiple songs that have been found?
        return result["hits"]["hits"][0]["_source"]["mood"]
    else:
        return None


def get_stored_lyrics_of_song(song_name, artist_name):
    """Search in Elasticsearch index for the song and return the lyrics if already stored.

    :param song_name: song name of the document entry.
    :param artist_name: artist name of the document entry.

    :return: Lyrics of given song and artist name if stored in Elasticsearch index. Else None.
    :rtype: String or None
    """

    global index_name

    # TODO: Add authentication for elasticsearch?
    es_host = "http://localhost:9200"

    es = Elasticsearch(
        hosts=es_host
    )

    # Search for song in es index
    # TODO: Change "match" to "term"?
    result = es.search(index=index_name, query={"bool": {"must": [
        {"match": {"song_name": song_name}}, {"match": {"artist_name": artist_name}}]}})

    # Check if a song has been found
    if result["hits"]["total"]["value"] > 0:
        # TODO: How to handle multiple songs that have been found?
        return result["hits"]["hits"][0]["_source"]["lyrics"]
    else:
        return None
