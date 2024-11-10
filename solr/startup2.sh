#!/bin/bash

# This script expects a container started with the following command. (execute once, uncomment then comment)
 #docker run -p 8983:8983 --name ntsa_solr -v ${PWD}:/data -d solr:9 solr-precreate courses

#Execute
docker start ntsa_solr


# Clean the courses collection
curl "http://localhost:8983/solr/courses/update?commit=true" -H "Content-Type: text/xml" --data-binary '<delete><query>*:*</query></delete>'
curl "http://localhost:8983/solr/courses/update?commit=true"


curl -X POST -H 'Content-type:application/json' \
--data-binary "simple_schema.json" \
http://localhost:8983/solr/courses/schema



# Populate collection using mapped path inside container.
docker exec -it ntsa_solr bin/post -c courses /data/all_episodes.json