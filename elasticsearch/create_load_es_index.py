import os
import json
import time

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import pandas as pd


def create_es_index():
    # TODO: Add docstring

    DATA_FILE_PATH = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "data_exploration",
            "data",
            "song-data-labels-cleaned.csv",
        )
    )

    # check if the file with ground truth labels is found
    if not os.path.isfile(DATA_FILE_PATH):
        raise Exception(
            "'../data_exploration/data/song-data-labels-cleaned.csv' not found"
        )

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
        f"elasticdump --input={es_host}/{index_name} --output={index_file}"
    )  # --type=data


# TODO: Add function for loading the elasticsearch index from the saved json file
def load_es_index():
    # TODO: Add docstring

    index_name = "lyrics_mood_classification"
    DATA_FILE_PATH = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data_exploration",
        "data",
        f"{index_name}.json",
    )

    # check if the file with ground truth labels is found
    if not os.path.isfile(DATA_FILE_PATH):
        raise Exception(f"'../data_exploration/data/{index_name}.json' not found")

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

    # TODO: check if it works
    # create documents from json file

    # Open the JSON file
    with open("file.json", "r") as json_file:
        # Load the JSON data from the file
        json_data_dict = json.load(json_file)

    new_documents = []
    for id, document in enumerate(json_data_dict):
        new_documents.append(
            {
                "_index": index_name,
                "_type": "_doc",
                "_id": f"{id}",
                "_source": {
                    "song_name": document["SName"],
                    "artist_name": document["Artist"],
                    "lyrics": document["Lyric"],
                    "mood": document["Mood"],
                },
            }
        )
    successful_operations, errors = helpers.bulk(es, new_documents)
    print(f"Successful operations: {successful_operations}")
    print(f"Errors: {errors}")


if __name__ == "__main__":
    print(create_es_index())
