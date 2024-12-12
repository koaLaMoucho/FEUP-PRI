# Makefile
SHELL := /bin/bash

.PHONY: help
help:
	@echo "Commands:"
	@echo "style      : runs style formatting."
	@echo "down       : stops all running services, removes containers and volumes."
	@echo "up         : start Docker daemon and Solr."
	@echo "schema     : update schema using docker/data/schema.json."
	@echo "populate   : populate Solr using docker/data/data.json."
	@echo "trec_eval  : download trec_eval source code and compile it."
	@echo "test       : run unit tests."
	@echo "run_eval_complex QUERY_NUM=<number> : run evaluation for complex schema and query number <number>."
	@echo "run_eval_simple QUERY_NUM=<number> : run evaluation for simple schema and query number <number>."
	@echo "run_all_eval : run evaluation for all queries."
	@echo "to run everything: make down ( to clean up) -> make up (to start solr) -> make build_all (to build the schemas) -> make run_all_eval (to run the evaluations) -> make run_plot_all (to plot the PR curves)"

.PHONY: style
style:
	isort src test --atomic
	black -l 100 src test
	flake8 src test

.PHONY: down
down:
	docker compose -f docker/docker-compose.yml down --remove-orphans -v

.PHONY: up
up:
	docker compose -f docker/docker-compose.yml up -d

.PHONY: simpleSchema
simpleSchema:
	docker exec one_piece_solr bin/solr create -c "simpleSchemaColl"
	curl -X POST \
		-H 'Content-type:application/json' \
		--data-binary "@./docker/data/simple_schema.json" \
		http://localhost:8983/solr/simpleSchemaColl/schema

.PHONY: deleteSimpleSchemaCollection
deleteSimpleSchemaCollection:
	docker exec one_piece_solr bin/solr delete -c "simpleSchemaColl"

.PHONY: simplePopulate
simplePopulate:
	docker exec -it one_piece_solr bin/solr post -c simpleSchemaColl /data/one_piece_episodes.json
.PHONY: complexSchema
complexSchema:
	docker exec one_piece_solr bin/solr create -c "complexSchemaColl"
	docker exec one_piece_solr cp /data/my_synonyms.txt /var/solr/data/complexSchemaColl/conf/
	curl -X POST \
		-H 'Content-type:application/json' \
		--data-binary "@./docker/data/complex_schema.json" \
		http://localhost:8983/solr/complexSchemaColl/schema

.PHONY: deleteComplexSchema
deleteComplexSchema:
	docker exec one_piece_solr bin/solr delete -c "complexSchemaColl"

.PHONY: complexPopulate
complexPopulate:
	docker exec -it one_piece_solr bin/solr post -c complexSchemaColl /data/one_piece_episodes.json

.PHONY: trec_eval
trec_eval:
	git clone https://github.com/usnistgov/trec_eval.git src/trec_eval
	cd src/trec_eval && make
	cd ../..

.PHONY: test
test:
	python -m unittest discover -s test -p 'test_*.py'

run_eval_complex:
	@if [ -z "$(QUERY_NUM)" ]; then \
		echo "Error: QUERY_NUM is not set. Use 'make run_eval_complex QUERY_NUM=<number>'"; \
		exit 1; \
	fi
	@python ./scripts/query_solr.py --query ./config/query$(QUERY_NUM).json --collection complexSchemaColl > ./output/result$(QUERY_NUM)_complex.json
	@cat ./output/result$(QUERY_NUM)_complex.json | python ./scripts/solr2trec.py > ./output/result$(QUERY_NUM)_complex.trec
	@cat ./config/qrels$(QUERY_NUM).txt | python ./scripts/qrels2trec.py > ./output/qrels$(QUERY_NUM).trec
	@trec_eval ./output/qrels$(QUERY_NUM).trec ./output/result$(QUERY_NUM)_complex.trec > ./output/eval_$(QUERY_NUM)_complex.txt

run_eval_simple:
	@if [ -z "$(QUERY_NUM)" ]; then \
		echo "Error: QUERY_NUM is not set. Use 'make run_eval_simple QUERY_NUM=<number>'"; \
		exit 1; \
	fi
	@python ./scripts/query_solr.py --query ./config/query$(QUERY_NUM).json --collection simpleSchemaColl > ./output/result$(QUERY_NUM)_simple.json
	@cat ./output/result$(QUERY_NUM)_simple.json | python ./scripts/solr2trec.py > ./output/result$(QUERY_NUM)_simple.trec
	@cat ./config/qrels$(QUERY_NUM).txt | python ./scripts/qrels2trec.py > ./output/qrels$(QUERY_NUM).trec
	@trec_eval ./output/qrels$(QUERY_NUM).trec ./output/result$(QUERY_NUM)_simple.trec > ./output/eval_$(QUERY_NUM)_simple.txt

.PHONY: run_all_eval
run_all_eval:
	@for i in 1 2 3 4 5; do \
		echo "Running evaluations for QUERY_NUM=$$i..."; \
		if $(MAKE) --no-print-directory run_eval_complex QUERY_NUM=$$i && \
		   $(MAKE) --no-print-directory run_eval_simple QUERY_NUM=$$i; then \
			echo "Ran evaluation for query $$i successfully"; \
		else \
			echo "Error occurred while running eval for query $$i"; \
		fi; \
	done

.PHONY: run_plot_all
run_plot_all:
	@for i in 1 2 3 4 5; do \
		echo "Plotting PR Curve for QUERY_NUM=$$i..."; \
		python ./scripts/plot_pr.py --qrels ./output/qrels$$i.trec --simple_pred ./output/result$${i}_simple.trec --complex_pred ./output/result$${i}_complex.trec --output ./output/prec_rec_q$$i.png; \
	done

.PHONY: build_simple
build_simple:
	curl -X POST \
		-H 'Content-type:application/json' \
		--data-binary "@./docker/data/simple_schema.json" \
		http://localhost:8983/solr/simpleSchemaColl/schema
	docker exec -it one_piece_solr bin/solr post -c simpleSchemaColl /data/one_piece_episodes.json

.PHONY: build_complex
build_complex:
	docker exec one_piece_solr bin/solr create -c "complexSchemaColl"
	docker exec one_piece_solr cp /data/my_synonyms.txt /var/solr/data/complexSchemaColl/conf/
	curl -X POST \
		-H 'Content-type:application/json' \
		--data-binary "@./docker/data/complex_schema.json" \
		http://localhost:8983/solr/complexSchemaColl/schema
	docker exec -it one_piece_solr bin/solr post -c complexSchemaColl /data/one_piece_episodes.json

.PHONY: build_all
build_all: build_simple build_complex