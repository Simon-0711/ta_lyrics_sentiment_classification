from elasticsearch import Elasticsearch

# Set Elasticsearch index name
index_name = "lyrics_mood_classification"


def add_es_document(song_name, artist_name, lyrics, mood):
    """Add document to Elasticsearch index.

    :param song_name: song name of the document entry.
    :param artist_name: artist name of the document entry.
    :param lyrics: artist name of the document entry.
    :param mood: mood of the document entry.
    """

    global index_name

    es_host = "http://elasticsearch:9200"

    es = Elasticsearch(hosts=es_host)
    # Add document to index
    es.index(
        index=index_name,
        document={
            "song_name": song_name,
            "artist_name": artist_name,
            "lyrics": lyrics,
            "mood": mood,
        },
    )
    es.close()


def get_stored_mood_of_song(song_name, artist_name):
    """Search in Elasticsearch index for the song and return the mood if already stored.

    :param song_name: song name of the document entry.
    :param artist_name: artist name of the document entry.

    :return: Mood of given song and artist name if stored in Elasticsearch index. Else None.
    :rtype: String or None
    """

    global index_name

    es_host = "http://elasticsearch:9200"

    es = Elasticsearch(hosts=es_host)

    # Search for song in es index (use match instead of term query to handle typos)
    result = es.search(
        index=index_name,
        query={
            "bool": {
                "must": [
                    {"match": {"song_name": song_name}},
                    {"match": {"artist_name": artist_name}},
                ]
            }
        },
    )

    # Check if a song has been found
    es.close()
    if result["hits"]["total"]["value"] > 0:
        # Take most relevant result
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

    es_host = "http://elasticsearch:9200"

    es = Elasticsearch(hosts=es_host)

    # Search for song in es index (use match instead of term query to handle typos)
    result = es.search(
        index=index_name,
        query={
            "bool": {
                "must": [
                    {"match": {"song_name": song_name}},
                    {"match": {"artist_name": artist_name}},
                ]
            }
        },
    )
    # Check if a song has been found
    es.close()
    if result["hits"]["total"]["value"] > 0:
        # Take most relevant result
        return result["hits"]["hits"][0]["_source"]["lyrics"]
    else:
        return None


def get_all_documents_of_mood(mood):
    """
    Function that returns all the documents of a certain mood.

    :param mood: mood of the document entry.

    :return: dict of documents of the given mood.
    :rtype: dict
    """

    global index_name

    es_host = "http://elasticsearch:9200"
    es = Elasticsearch(hosts=es_host)

    # search for all document of given mood (set size to 10000 to get all documents, as it is max number of documents that can be found at once and there are less than 10000 documents in the index for each mood)
    results = es.search(index=index_name, size=10000, query={"match": {"mood": mood}})
    es.close()

    # check if given mood has songs in the index
    if results["hits"]["total"]["value"] == 0:
        raise Exception(f"No songs found for mood: {mood}.")

    # save all lyrics of the songs with the given mood
    song_same_mood_dict = {}
    for result in results["hits"]["hits"]:
        song = result["_source"]["song_name"]
        artist = result["_source"]["artist_name"]
        lyrics = result["_source"]["lyrics"]
        document_dict = {"Song": song, "Artist": artist, "Lyrics": lyrics}

        # add document to song_same_mood_dict
        song_same_mood_dict[f"{song}_{artist}"] = document_dict

    return song_same_mood_dict
