#!/bin/sh

/bin/tini /usr/local/bin/docker-entrypoint.sh -- &
/tmp/wait-for-it.sh -t 30 localhost:9200 -- python3 /tmp/create_load_save_es_index.py
while true; do sleep 100; done
