#!/usr/bin/env python3

import sys


def qrels_to_trec(qrels: list) -> None:
    """
    Converts qrels (query relevance judgments) to TREC evaluation format.

    Arguments:
    - qrels: A list of qrel lines (document IDs) from standard input.
    """
    for line in qrels:
        doc_id = line.strip()
        # remove space after "Episode" by replacing "Episode " with "Episode"
        doc_id = doc_id.replace("Episode ", "Episode")
        print(f"0 0 {doc_id} 1")


if __name__ == "__main__":
    """
    Read qrels from stdin and output them in TREC format.
    """
    qrels = sys.stdin.readlines()
    qrels_to_trec(qrels)
