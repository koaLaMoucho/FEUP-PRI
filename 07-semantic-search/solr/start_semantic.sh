#!/bin/bash
# u might need to run "sed -i -e 's/\r$//' ourStartup.sh" to remove windows line endings and execute the script

# This script expects a container started with the following command.
# docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d solr:9 solr-precreate priProj

# command to delete a collection
docker exec meic_solr bin/solr delete -c priProj

# command to create a collection
docker exec meic_solr bin/solr create -c "priProj"

# add synonyms file to solr config folder to be retrieved by schema
docker exec meic_solr cp /data/my_synonyms.txt /var/solr/data/priProj/conf/

# Schema definition via API
curl -X POST -H 'Content-type:application/json' --data-binary "@./semantic_schema.json" http://localhost:8983/solr/priProj/schema

# Populate collection using mapped path inside container.
docker exec -it meic_solr bin/post -c priProj /data/semantic_one_piece.json
