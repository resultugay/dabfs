import os
import logging
logger = logging.getLogger(__name__)
import sys 


def read_data(path, g):
    # Read graph data and store in g
    try:
        with open(path, 'r') as f:
            whole_content = [x.strip() for x in f.readlines()]
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        sys.exit(1) 
    
    number_of_nodes = 0
    number_of_edges = 0
    for line in whole_content:
        nodes = line.split(" ")
        node_from = int(nodes[0])
        node_to = int(nodes[1])
        number_of_nodes = max(node_from, node_to, number_of_nodes)  ## find how many nodes we have
        g.add_edge(node_from, node_to)
        # g.addEdge(node_to,node_from) ## if its undirected
        number_of_edges += 1
    g.set_number_of_nodes(number_of_nodes + 1)
    g.set_number_of_edges(number_of_edges)

    return g


def save_compressed_data(path, compressed_graph_list,g):

    os.makedirs("dabfs/output", exist_ok=True)
    path = "dabfs/output/" + path
    new_id_with_scc = {}
    count = 0
    for compressed_set in compressed_graph_list:
        new_id_with_scc[count] = list(compressed_set)
        count += 1

    new_adj_list = {}
    count = 0
    for id,scc in new_id_with_scc.items():
        neighbors = set()
        for each in scc:
            neighbor_list_of_scc = g.get_neighbors(each)
            if neighbor_list_of_scc is not None:
                for each_neighbor in neighbor_list_of_scc:
                    new_neighbor_id = find_corresponding_id(new_id_with_scc,each_neighbor)
                    if new_neighbor_id != id:
                        neighbors.add(new_neighbor_id)
                new_adj_list[id] = neighbors

    count_edges = 0
    with open(path, 'w', encoding='utf-8') as f:
        for id,neihgbor_list in new_adj_list.items():
            for each_neighbor in neihgbor_list:
                f.write(str(id) + " " + str(each_neighbor) + "\n")
                count_edges += 1
    logger.info(f"Saved compressed data {path}")
    return count_edges

def find_corresponding_id(id_with_scc,node):
    for id,scc in id_with_scc.items():
        if node in scc:
            return id