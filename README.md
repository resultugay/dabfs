# DABFS

**DABFS** (Dynamic Approach with BFS) is a Python package for query-preserving graph compression. It efficiently compresses directed graphs while preserving reachability queries, enabling scalable query processing on large graphs.

---

## Installation

```bash
pip install dabfs

Or, install locally from the repository:

git clone https://github.com/resultugay/dabfs.git
```

## Usage
```python
from dabfs import dabfs_compress
# Call DABFS with your edge list file
dabfs_compress("dabfs/data/simple_graph.txt")
```
## Example Input
A text file containing the edge list of the graph.
Each row represents an edge with two columns: source_node and target_node.
Example of simple_graph.txt:
```
1 2
2 3
3 4
4 1
5 6
```
## Example Output
```
After running dabfs_compress("dabfs/data/wiki.txt"):
2026-04-07 13:49:02,384 - INFO - Total dynamic BFS time for finding all ancestors 7.14 sec
2026-04-07 13:49:13,670 - INFO - Candidate Generated 3.22 sec
2026-04-07 13:49:30,034 - INFO - Saved compressed data dabfs/output/reachibility_query_compressed.txt
2026-04-07 13:49:30,037 - INFO - number of nodes: 7115
2026-04-07 13:49:30,037 - INFO - number of edges: 103689
2026-04-07 13:49:30,037 - INFO - Compressed number of nodes: 3289
2026-04-07 13:49:30,037 - INFO - Compressed number of edges: 77846
2026-04-07 13:49:30,037 - INFO - Compression ratio: 0.73 (73.22%)
2026-04-07 13:49:30,037 - INFO - Compression factor: 0.27 (26.78%)
```
## Basic Example
```python
from dabfs import dabfs_compress
# Compress the graph and save outputs
dabfs_compress("dabfs/data/simple_graph.txt")
```
Using Compressed Graphs
```python
from graph import Graph
from data_reader import read_data
g = Graph()
compressed_graph = read_data("dabfs/output/reachability_query_compressed.txt",g)
```
You can now run reachability queries directly on reachability_query_compressed.