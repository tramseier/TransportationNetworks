"""Test networks for the QDTA network loading tests.

Used by:
- QDTA / Tests / test_netw_loading.py (all networks below),
- QDTA / Tests / test_travel_times.py (single_path_corridor_network),
- QDTA / tests / test_plotting.py (bidirectional_corridor_network,
  single_path_corridor_network).

Each network is documented with its structure and the analytical
solution it allows to check (flow acceptance factors alpha).
"""

import pandas as pd

from QDTA.network import Network


def example_1_network() -> Network:
    """
    Create the network from Example 1 in the paper (Fig. 6).
    
    Network structure:
    A --1--> B --2--> C --3--> A'
              |
              +--4--> D --5--> E --6--> B'
    
    Two parallel paths:
    - Path 1: 1 -> 2 -> 3 with demand 1000 veh/h
    - Path 2: 4 -> 5 -> 6 with demand 1000 veh/h
        
    Integer node mapping:
    A: 0, B: 1, C: 2, D: 3, E: 4, B': 5, A': 6, 
    B_intermediate: 7, A_intermediate: 8, B_start: 9, A_start: 10
    """
    # Define network as pandas DataFrame
    network_df = pd.DataFrame([
        # Original link "1": A -> B
        [0, 1, 2000, 1.0, 1.0/50, 1],
        # Original link "2": B -> B_intermediate  
        [1, 7, 250, 1.0, 1.0/50, 1],
        # Original link "3": B -> C
        [1, 2, 2000, 1.0, 1.0/50, 1],
        # Original link "4": C -> D
        [2, 3, 2000, 1.0, 1.0/50, 1],
        # Original link "5": D -> A_intermediate
        [3, 8, 250, 1.0, 1.0/50, 1],
        # Original link "6": D -> A
        [3, 0, 2000, 1.0, 1.0/50, 1],
        # Original link "7": B_intermediate -> B'
        [7, 5, 1e5, 1.0, 1.0/50, 1],
        # Original link "8": A_intermediate -> A'
        [8, 6, 1e5, 1.0, 1.0/50, 1],
        # Original link "9": A_start -> A
        [10, 0, 1e5, 1.0, 1.0/50, 1],
        # Original link "10": B_start -> C
        [9, 2, 1e5, 1.0, 1.0/50, 1],
    ], columns=['a_node', 'b_node', 'capacity', 'length', 'free_flow_time', 'b'])
    
    # Define demand as pandas DataFrame
    demand_df = pd.DataFrame([
        [10, 6, 1000],  # A_start (10) -> A' (6) with demand 1000
        [9, 5, 1000],   # B_start (9) -> B' (5) with demand 1000
    ], columns=['O', 'D', 'demand'])
    
    network = Network(network_df, demand_df)
    
    # Add node positions for plotting (optional)
    network.node_positions = {
        0: (-1, 5),      # A
        1: (1, 5),       # B  
        2: (1, 0),       # C
        3: (-1, 0),      # D
        5: (6, 5),       # B'
        6: (-6, 0),      # A'
        7: (2.8, 5),     # B_intermediate
        8: (-2.8, 0),    # A_intermediate
        9: (4, 0),       # B_start
        10: (-4, 5)      # A_start
    }

    return network


def simple_merge_network() -> Network:
    """
    Create a simple merge network for testing.
    
    Network structure:
    A --1--> C --3--> D
    B --2--> 
    
    Paths:
    - A->C->D with demand 500
    - B->C->D with demand 500
    
    Link 3 has capacity 500 (bottleneck).
    """
    # Integer node mapping: A: 0, B: 1, C: 2, D: 3
    network_df = pd.DataFrame([
        [0, 2, 1000, 1.0, 1.0/50, 1],  # A -> C (original link "1")
        [1, 2, 1000, 1.0, 1.0/50, 1],  # B -> C (original link "2")
        [2, 3, 500, 1.0, 1.0/50, 1],   # C -> D (original link "3")
    ], columns=['a_node', 'b_node', 'capacity', 'length', 'free_flow_time', 'b'])
    
    demand_df = pd.DataFrame([
        [0, 3, 500],  # A -> D with demand 500
        [1, 3, 500],  # B -> D with demand 500
    ], columns=['O', 'D', 'demand'])
    
    network = Network(network_df, demand_df)
    
    return network


def single_path_network() -> Network:
    """
    Create a simple single path network with a bottleneck.
    
    Network: A --1--> B --2--> C
    Path: A->B->C with demand 3000
    Link 2 has capacity 2000.
    """
    # Integer node mapping: A: 0, B: 1, C: 2
    network_df = pd.DataFrame([
        [0, 1, 4000, 1.0, 1.0/50, 1],  # A -> B (original link "1")
        [1, 2, 2000, 1.0, 1.0/50, 1],  # B -> C (original link "2")
    ], columns=['a_node', 'b_node', 'capacity', 'length', 'free_flow_time', 'b'])
    
    demand_df = pd.DataFrame([
        [0, 2, 3000],  # A -> C with demand 3000
    ], columns=['O', 'D', 'demand'])
    
    network = Network(network_df, demand_df)
    
    return network


def single_path_corridor_network() -> Network:
    """
    Create a simple single path network corridor with multiple bottlenecks.
    """
    # Integer node mapping: A: 0, B: 1, C: 2, D: 3, E: 4
    network_df = pd.DataFrame([
        [0, 1, 3 * 1800, 1.0, 1.0/50, 1],  # A -> B (original link "1")
        [1, 2, 3 * 1800, 1.0, 1.0/50, 1],  # B -> C (original link "2")
        [2, 3, 2 * 1800, 1.0, 1.0/50, 1],  # C -> D (original link "3")
        [3, 4, 1 * 1800, 1.0, 1.0/50, 1],  # D -> E (original link "4")
    ], columns=['a_node', 'b_node', 'capacity', 'length', 'free_flow_time', 'b'])


    
    demand_df = pd.DataFrame([
        [0, 4, 4000],  # A -> E with demand 4000
    ], columns=['O', 'D', 'demand'])

    # Add node positions for plotting (optional)
    network = Network(network_df, demand_df)
    network.node_positions = {
        0: (0, 0),
        1: (2, 0),
        2: (4, 0),
        3: (6, 0),
        4: (8, 0)
    }
    return network


def bidirectional_corridor_network() -> Network:
    """
    Create a simple bidirectional corridor network with multiple bottlenecks.
    """
    # Integer node mapping: A: 0, B: 1, C: 2, D: 3, E: 4
    network_df = pd.DataFrame([
        [0, 1, 2 * 1000, 1.0, 1.0/50, 0],  # A -> B (original link "1")
        [1, 2, 2 * 1000, 1.0, 1.0/50, 0],  # B -> C (original link "2")
        [2, 3, 2 * 1000, 1.0, 1.0/50, 0],  # C -> D (original link "3")
        [3, 4, 1000, 1.0, 1.0/50, 0],  # D -> E (original link "4")
    ], columns=['a_node', 'b_node', 'capacity', 'length', 'free_flow_time', 'b'])

    demand_df = pd.DataFrame([
        [0, 3, 500],   # A -> E with demand
        [0, 4, 1500],   # A -> E with demand
        [4, 0, 500]    # E -> A with demand
    ], columns=['O', 'D', 'demand'])

    network = Network(network_df, demand_df)
    network.node_positions = {
        0: (0, 0),
        1: (2, 0),
        2: (4, 0),
        3: (6, 0),
        4: (8, 0)
    }
    return network
