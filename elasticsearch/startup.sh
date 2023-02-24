#!/bin/sh

chmod -R 777 /opt/
chown -R elasticsearch:elasticsearch /opt/
/bin/tini /usr/local/bin/docker-entrypoint.sh -- &
/opt/elasticsearch/wait-for-it.sh -t 30 localhost:9200 -- python3 /opt/elasticsearch/create_load_save_es_index.py
while true; do sleep 100; done
