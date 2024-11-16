## Steps to run evals

1. Make sure the neccessary files are present in the config folder and docker/data
    - config folder:
        - query files
        - qrels for each query
    - docker/data:
        - data to populate the solr instance
        - schemas, one simple, another complex

2. Run the following commands in this folder:

``` bash
make down # only necessary to make sure there is no other docker containers
make up # to create the repository with a solr instance
make simpleSchema
make simplePopulate
make complexSchema
make complexPopulate
make run_all_eval
```

## Results

The results are present in the folder */output* in the files eval_*.txt

For example, the eval of the simple schema in the query 1 is in the file *eval_1_simple.txt*