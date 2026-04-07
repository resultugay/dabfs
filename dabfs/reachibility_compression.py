from copy import deepcopy
import time
from data_reader import read_data,save_compressed_data
import time
from graph import Graph
import logging
import sys

sys.setrecursionlimit(10**6)  # 1 million, adjust if needed


logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Dynamic approach
def BFS_dynamic(node, ancestors, visited, g):
    if not visited[node]:
        local_neighbors = deepcopy(g.graph.get(node))
        visited[node] = True
        if local_neighbors is not None:
            while local_neighbors:
                    current_node = local_neighbors.pop()
                    if not visited[current_node]:
                        sub_group = BFS_dynamic(current_node, ancestors, visited,g)
                        ancestors[node].add(current_node)
                        ancestors[node].update(sub_group)
                    else:
                        ancestors[node].add(current_node)
                        ancestors[node].update(ancestors[current_node])
            return sorted(ancestors[node])
        else:
            return [node]
    else:
        return sorted(ancestors[node])


def ancestors_descendants_dynamic(g):
    ancestor_dict = {}
    for i in range(g.get_number_of_nodes()):
        ancestor_dict[i] = set()
    visited = [False] * (g.get_number_of_nodes())

    for i in range(g.get_number_of_nodes()):
        if not visited[i]:
            BFS_dynamic(i, ancestor_dict, visited,g)
    return ancestor_dict


def calculate_compression_graph(original_number_of_nodes,original_number_of_edges,ancestors_of_nodes, descendants_of_nodes,g):
    candidate_list_of_nodes = {}

    start_time = time.time()

    for node_1 in reversed(list(ancestors_of_nodes.keys())):
        if node_1 not in candidate_list_of_nodes:
            candidate_list_of_nodes[node_1] = []
            candidate_list_of_nodes[node_1].append(node_1)
        for node_2 in reversed(list(ancestors_of_nodes.keys())):
            if ancestors_of_nodes.get(node_1) == ancestors_of_nodes.get(node_2) and node_1 != node_2:
                    candidate_list_of_nodes[node_1].append(node_2)
                    del ancestors_of_nodes[node_2]

    logger.info(f"Candidate Generated {(time.time() - start_time):.2f} sec")
    compressed_graph = []
    for node_1 in list(candidate_list_of_nodes.keys()):
        all_candidates = candidate_list_of_nodes.get(node_1)
        if all_candidates is not None:
            compressed_nodes = []
            for candidate in all_candidates:
                descendant_of_node_1 = descendants_of_nodes.get(node_1)
                descendant_of_node_candidate = descendants_of_nodes.get(candidate)
                if descendant_of_node_1 == descendant_of_node_candidate:
                    compressed_nodes.append(candidate)
            for i in compressed_nodes:
                if i != node_1:
                    del candidate_list_of_nodes[i]

            compressed_graph.append(compressed_nodes)

    start_time = time.time()
    g = g.get_transpose()

    total_compressed_number_of_edges = save_compressed_data("reachability_query_compressed.txt", compressed_graph, g)

    total_compressed_node_number = len(compressed_graph)
    compression_factor = 1 - (total_compressed_number_of_edges + total_compressed_node_number) / \
                            (original_number_of_nodes + original_number_of_edges)

    compression_ratio = ((total_compressed_number_of_edges + total_compressed_node_number)) / (original_number_of_nodes + original_number_of_edges)
    logger.info(f"number of nodes: {original_number_of_nodes}")
    logger.info(f"number of edges: {original_number_of_edges}")
    logger.info(f"Compressed number of nodes: {total_compressed_node_number}")
    logger.info(f"Compressed number of edges: {total_compressed_number_of_edges}")
    logger.info(f"Compression ratio: {compression_ratio:.2f} ({(compression_ratio*100):.2f}%)")
    logger.info(f"Compression factor: {compression_factor:.2f} ({compression_factor*100:.2f}%)")

def dabfs_compress(edge_path):
    g = Graph()
    read_data(edge_path,g)
    original_number_of_nodes = g.get_number_of_nodes()
    original_number_of_edges = g.get_number_of_edges()
    start_time = time.time()
    ancestors_of_nodes = ancestors_descendants_dynamic(g)
    logger.info(f"Total dynamic BFS time for finding all ancestors {(time.time() - start_time):.2f} sec")

    start_time = time.time()
    g = g.get_transpose()
    descendants_of_nodes = ancestors_descendants_dynamic(g)
    calculate_compression_graph(original_number_of_nodes,original_number_of_edges,ancestors_of_nodes, descendants_of_nodes,g)