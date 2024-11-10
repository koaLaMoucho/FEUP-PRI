#!/bin/bash

# This script expects a container started with the following command.
#docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d solr:9 solr-precreate priProj

# command to delete a collection
docker exec meic_solr bin/solr delete -c priProj

# command to create a collection
docker exec meic_solr bin/solr create -c "priProj"

# Schema definition via API
curl -X POST -H 'Content-type:application/json' --data-binary "@./onePieceSchema.json" http://localhost:8983/solr/priProj/schema
# curl -X POST -H 'Content-type:application/xml' --data-binary "@./one_piece_schema.xml" http://localhost:8983/solr/priProj/schema

# Populate collection using mapped path inside container.
docker exec -it meic_solr bin/post -c priProj /data/one_piece_data.json