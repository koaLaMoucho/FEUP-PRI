
# convert query results
cat ./query5_results_basic.json | python3 ../../06-evaluation/scripts/solr2trec.py | python3 ./fixID.py > ./temp/results5_basic_trec.txt
#cat ./query5_results.json | python3 ../../06-evaluation/scripts/solr2trec.py | python3 ./fixID.py > ./temp/results5_complex_trec.txt

# convert qrels
#cat ./qrels5.txt | python3 ../../06-evaluation/scripts/qrels2trec.py | python ./fixID.py > ./temp/qrels5_trec.txt

# get evaluation
#trec_eval ./temp/qrels5_trec.txt ./temp/results5_basic_trec.txt > ./temp/eval5_basic.txt
