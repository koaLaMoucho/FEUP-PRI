#!/bin/bash
# u might need to run "sed -i -e 's/\r$//' start_semantic.sh" to remove windows line endings and execute the script

# This script expects a container started with the following command in this directory:
# docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d solr:9 solr-precreate simple

# create collections (simple already exists)
docker exec meic_solr bin/solr create -c "complex"
docker exec meic_solr bin/solr create -c "semantic"

# add synonyms for complex and semantic
docker exec meic_solr cp /data/my_synonyms.txt /var/solr/data/complex/conf/
docker exec meic_solr cp /data/my_synonyms.txt /var/solr/data/semantic/conf/

# add schemas
curl -X POST -H 'Content-type:application/json' --data-binary "@./simple_schema.json" http://localhost:8983/solr/simple/schema
curl -X POST -H 'Content-type:application/json' --data-binary "@./complex_schema.json" http://localhost:8983/solr/complex/schema
curl -X POST -H 'Content-type:application/json' --data-binary "@./semantic_schema.json" http://localhost:8983/solr/semantic/schema

# Populate collection using mapped path inside container.
docker exec -it meic_solr bin/post -c simple /data/one_piece_data.json
docker exec -it meic_solr bin/post -c complex /data/one_piece_data.json
docker exec -it meic_solr bin/post -c semantic /data/semantic_one_piece.json
