#!/bin/bash
# u might need to run "sed -i -e 's/\r$//' ourStartup.sh" to remove windows line endings and execute the script

# This script expects a container started with the following command.
# docker run -p 8983:8983 --name meic_solr -v ${PWD}:/data -d solr:9 solr-precreate priProj

# command to delete a collection
docker exec meic_solr bin/solr delete -c priProj

# command to create a collection
docker exec meic_solr bin/solr create -c "priProj"

# add synonyms file to solr config folder to be retrieved by schema
# the first path depends on what folder is mounted to the container
docker exec meic_solr cp /data/my_synonyms.txt /var/solr/data/priProj/conf/

# Schema definition via API
# Entrar no cd solrData
#curl -X POST -H 'Content-type:application/json' --data-binary "@./onePieceSchema.json" http://localhost:8983/solr/priProj/schema
curl -X POST -H 'Content-type:application/json' --data-binary "@./new_schema.json" http://localhost:8983/solr/priProj/schema

#sair do cd solrData
# Populate collection using mapped path inside container.
docker exec -it meic_solr bin/post -c priProj /data/one_piece_data.json


## unrelated commands

# get the details of a field
# curl -X GET http://localhost:8983/solr/courses/schema/fields/title

# get information about the field type
# curl -X GET http://localhost:8983/solr/courses/schema/fieldtypes/<fieldType>

# get query response
# python ./scripts/query_solr.py --query config/query_sys1.json --uri http://localhost:8983/solr --collection courses > config/query_sys1_response.json
# convert it to TREC 
# cat config/query_sys1_response.json | python ./scripts/solr2trec.py > results_sys1_trec.txt
# or do a single command to get the query response and convert it to TREC
# python ./scripts/query_solr.py --query config/query_sys1.json --uri http://localhost:8983/solr --collection courses | python ./scripts/solr2trec.py > results_sys1_trec.txt
# 

# convert qrels to TREc
# cat config/qrels.txt | ./scripts/qrels2trec.py > qrels_trec.txt

# get evaluation
# trec_eval qrels_trec.txt results_sys1_trec.txt

