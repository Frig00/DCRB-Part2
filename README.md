
# DCRB Project - Part 2

## Introduction

This project implements an efficient information retrieval system using inverted indexes and B-tree structures to handle various types of search queries on a dataset of movie plots.

## Features

- Inverted index construction
- B-tree implementation for efficient data storage and retrieval
- Support for multiple query types:
  - Single word queries
  - Conjunctive queries
  - Disjunctive queries
  - Prefix queries
  - Suffix queries
  - Wildcard queries

## Project Structure

The project consists of three main Python scripts:

1. `inverted_index.py`: Constructs the inverted index from the dataset.
2. `btree.py`: Implements the B-tree data structure and builds B-trees from the inverted index.
3. `retrieving.py`: Processes queries and retrieves relevant documents.

## Implementation Details

### Inverted Index Construction

- Reads and processes the movie plot dataset
- Removes punctuation and normalizes text
- Excludes stopwords
- Constructs and saves the inverted index and document data

### B-tree Construction and Management

- Defines `Node` and `BTree` classes
- Builds B-trees from the inverted index file
- Supports both normal and inverted B-trees for efficient querying

### Query Processing and Data Retrieval

- Loads B-trees and document data
- Implements various query types:
  - Single word query
  - Conjunctive query
  - Disjunctive query
  - Prefix query
  - Suffix query
  - Wildcard query

## Usage

1. Run `inverted_index.py` to construct the inverted index from your dataset.
2. Run `btree.py` to build the B-trees from the inverted index.
3. Run `retrieving.py` to process queries and retrieve relevant documents.

## Advantages

- Efficient text processing and indexing
- Scalable data storage using B-trees
- Fast retrieval for various query types
- Flexible query handling

## Requirements

- Python 3.x
- pandas (for data processing)