#!/usr/bin/env python3

import argparse
import sys

import matplotlib.pyplot as plt
import numpy as np


def main(qrels_file: str, simple_pred: str, complex_pred: str, output_file: str):
    """
    Read predicted document IDs from two stdin inputs and qrels (ground truth IDs) from a file,
    Plot precision-recall curve and save it to a .PNG file.

    Arguments:
        qrels_file -- Path to the qrels file containing ground truth document IDs in TREC format.
        predictions_file1 -- Path to the first predictions file in TREC format.
        predictions_file2 -- Path to the second predictions file in TREC format.
        output_file -- Name of the output PNG file where the precision-recall curve will be saved.
    """

    # Read qrels (ground truth) from the specified file in TREC format
    with open(qrels_file, "r") as f:
        y_true = {
            line.strip().split()[2] for line in f
        }  # Use a set for fast lookup of relevant document IDs

    # Read predicted document IDs from files in TREC format
    with open(simple_pred, "r") as f1, open(complex_pred, "r") as f2:
        y_pred1 = [line.strip().split()[2] for line in f1]  # Extract document IDs from first file
        y_pred2 = [line.strip().split()[2] for line in f2]  # Extract document IDs from second file

    # Edge case: Handle empty inputs
    if not y_pred1 or not y_pred2 or not y_true:
        print("Error: No predictions or qrels found. Please provide valid input.")
        sys.exit(1)

    # Calculate precision, recall, and keep track of relevant ranks for MAP calculation for both prediction files
    def calculate_metrics(y_pred):
        precision = []
        recall = []
        relevant_ranks = []  # To hold precision values at ranks where relevant documents are retrieved
        relevant_count = 0

        for i in range(1, len(y_pred) + 1):
            # Check how many predicted documents so far are relevant
            if y_pred[i - 1] in y_true:
                relevant_count += 1
                relevant_ranks.append(relevant_count / i)  # Precision at this rank (relevant document)

            # Precision: relevant docs so far / total docs retrieved so far
            precision.append(relevant_count / i)

            # Recall: relevant docs so far / total relevant docs in qrels
            recall.append(relevant_count / len(y_true))

        return precision, recall, relevant_ranks

    # Calculate metrics for both prediction files
    precision1, recall1, relevant_ranks1 = calculate_metrics(y_pred1)
    precision2, recall2, relevant_ranks2 = calculate_metrics(y_pred2)

    # Compute Mean Average Precision (MAP) for both
    map_score1 = np.sum(relevant_ranks1) / len(y_true) if relevant_ranks1 else 0
    map_score2 = np.sum(relevant_ranks2) / len(y_true) if relevant_ranks2 else 0

    # Compute the 11-point interpolated precision-recall curve for both
    recall_levels = np.linspace(0.0, 1.0, 11)
    
    interpolated_precision1 = [
        max([p for p, r in zip(precision1, recall1) if r >= r_level], default=0)
        for r_level in recall_levels
    ]
    
    interpolated_precision2 = [
        max([p for p, r in zip(precision2, recall2) if r >= r_level], default=0)
        for r_level in recall_levels
    ]

    # Compute the Area Under Curve (AUC) for both precision-recall curves
    auc_score1 = np.trapz(interpolated_precision1, recall_levels)
    auc_score2 = np.trapz(interpolated_precision2, recall_levels)

    # Plot the 11-point interpolated precision-recall curves
    plt.figure(figsize=(10, 6))
    
    plt.plot(
        recall_levels,
        interpolated_precision1,
        drawstyle="steps-post",
        label=f"Simple Curve - MAP: {map_score1:.4f}, AUC: {auc_score1:.4f}",
        linewidth=1,
    )
    
    plt.plot(
        recall_levels,
        interpolated_precision2,
        drawstyle="steps-post",
        label=f"Complex Curve - MAP: {map_score2:.4f}, AUC: {auc_score2:.4f}",
        linewidth=1,
    )

    # Customize plot appearance
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.legend(loc="lower left", prop={"size": 10})
    plt.title("Precision-Recall Curve")
    plt.grid(True, linestyle='--', linewidth=0.5)

    # Save the plot to the specified output PNG file
    plt.savefig(output_file, format="png", dpi=300)
    print(f"Precision-Recall plot saved to {output_file}")


if __name__ == "__main__":
    # Argument parser to handle the qrels file, two prediction files, and output file as command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate a Precision-Recall curve from two Solr results (in TREC format) and qrels."
    )
    parser.add_argument(
        "--qrels",
        type=str,
        required=True,
        help="Path to the qrels file (ground truth document IDs in TREC format)",
    )
    parser.add_argument(
        "--simple_pred",
        type=str,
        required=True,
        help="Path to the simple predictions file in TREC format"
    )
    parser.add_argument(
        "--complex_pred",
        type=str,
        required=True,
        help="Path to the complex predictions file in TREC format"
    )
    parser.add_argument("--output", type=str, required=True, help="Path to the output PNG file")
    args = parser.parse_args()

    # Run the main function with the provided qrels file, prediction files, and output file
    main(args.qrels, args.simple_pred, args.complex_pred, args.output)