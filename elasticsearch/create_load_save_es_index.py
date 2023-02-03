import os
import json
import time

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd


def create_es_index():
    """Create elasticsearch index for our lyrics mood classification using the saved ground truth data in '../data_exploration/data/song-data-labels-cleaned.csv'."""

    DATA_FILE_PATH = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "data_exploration",
            "data",
            "song-data-labels-cleaned.csv",
        )
    )

    # check for the file with the ground truth mood labels
    if not os.path.isfile(DATA_FILE_PATH):
        raise Exception(
            "'../data_exploration/data/song-data-labels-cleaned.csv' not found"
        )

    # initialize elasticsearch client
    es_host = "http://localhost:9200"
    es = Elasticsearch(hosts=es_host)

    # create empty index
    index_name = "lyrics_mood_classification"
    es.indices.create(
        index=index_name,
        mappings={
            "dynamic": "strict",
            "properties": {
                "song_name": {"type": "text"},
                "artist_name": {"type": "text"},
                "lyrics": {"type": "text"},
                "mood": {"type": "text"},
            },
        },
    )

    # load the document with the ground truth labels
    ground_truth_df = pd.read_csv(DATA_FILE_PATH)
    ground_truth_df = ground_truth_df[["SName", "Artist", "Lyric", "Mood"]]

    # create documents from df rows
    df_iter = ground_truth_df.iterrows()
    new_documents = []
    for id, document in df_iter:
        new_documents.append(
            {
                "_index": index_name,
                "_type": "_doc",
                "_id": f"{id}",
                "_source": {
                    "song_name": str(document["SName"]),
                    "artist_name": str(document["Artist"]),
                    "lyrics": str(document["Lyric"]),
                    "mood": str(document["Mood"]),
                },
            }
        )
    successful_operations, errors = helpers.bulk(es, new_documents)
    print(f"Successful operations: {successful_operations}")
    print(f"Errors: {errors}")

    # wait till documents are saved in elasticsearch
    while True:
        if es.count(index=index_name)["count"] < len(ground_truth_df):
            time.sleep(1)
            print("Waiting one second for documents to be saved in elasticsearch..")
            break

    # save elasticsearch index via elasticdump
    index_file = os.path.abspath(
        os.path.join(DATA_FILE_PATH, "..", f"{index_name}_index.json")
    )
    os.system(
        f"elasticdump --input={es_host}/{index_name} --output={index_file} --type=data"
    )


def load_es_index():
    """Load the most current elasticsearch index from the '../data_exploration/data/lyrics_mood_classification.json' file."""

    index_name = "lyrics_mood_classification"
    INDEX_FILE_PATH = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "data_exploration",
            "data",
            f"{index_name}_index.json",
        )
    )

    # check for the json file
    if not os.path.isfile(INDEX_FILE_PATH):
        raise Exception(f"'../data_exploration/data/{index_name}.json' not found")

    # initialize elasticsearch client
    es_host = "http://localhost:9200"
    es = Elasticsearch(hosts=es_host)

    # create empty index
    es.indices.create(
        index=index_name,
        mappings={
            "dynamic": "strict",
            "properties": {
                "song_name": {"type": "text"},
                "artist_name": {"type": "text"},
                "lyrics": {"type": "text"},
                "mood": {"type": "text"},
            },
        },
    )

    # load last state from index via the json file
    new_documents = []
    with open(INDEX_FILE_PATH, "r") as json_file:
        # load the documents from the json file
        for line in json_file:
            document = json.loads(line)
            new_documents.append(document)
    successful_operations, errors = helpers.bulk(es, new_documents)
    print(f"Successful operations: {successful_operations}")
    print(f"Errors: {errors}")


def save_es_index():
    """Save the most current elasticsearch index at '../data_exploration/data/lyrics_mood_classification.json'."""

    # save elasticsearch index via elasticdump
    es_host = "http://localhost:9200"
    index_name = "lyrics_mood_classification"
    INDEX_FILE_PATH = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "data_exploration",
            "data",
            f"{index_name}_index.json",
        )
    )
    os.system(
        f"elasticdump --input={es_host}/{index_name} --output={INDEX_FILE_PATH} --type=data"
    )


if __name__ == "__main__":
    # create_es_index()  # create the elasticsearch index
    load_es_index()  # load the elasticsearch index
    # save_es_index()  # save the elasticsearch index
