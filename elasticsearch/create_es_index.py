from elasticsearch import Elasticsearch

# TODO: Add authentication for elasticsearch?
es_host = "http://localhost:9200"

es = Elasticsearch(
    hosts=es_host
)

index_name = "lyrics_mood_classification"
es.indices.create(index=index_name,
                  mappings={
                      "dynamic": "strict",
                      "properties": {
                          "song_name":    {"type": "text"},
                          "artist_name":  {"type": "text"},
                          "lyrics":   {"type": "text"},
                          "mood":   {"type": "text"}
                      }
                  })
