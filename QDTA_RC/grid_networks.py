"""Grid test networks.

Used by:
- QDTA / tests / test_flow_assignment.py (4x4 grid with fixed OD pairs),
- QDTA / tests / test_plotting.py,
- Route_choice_TR / test_purc.py (grid_example, 8x8 grid),
- QDTA / Tests / test_netw_loading.py (via QDTA_RC import).
"""

import random
from typing import Optional

import pandas as pd

from QDTA.network import Network


def grid_network(
    N: int, 
    M: int, 
    num_od_pairs: int = 1,
    compute_paths: bool = True,
    demand_min: Optional[float] = None,
    demand_max: Optional[float] = None,
    demand_mean: Optional[float] = None,
    demand_std: Optional[float] = None,
    demand_df: Optional[pd.DataFrame] = None,
    capacity: float = 1000,
    ff_time_variation: float = 0.0
) -> Network:
    """
    Create a NxM grid network.
    
    Network structure:
    - N rows and M columns of nodes
    - Each node (i,j) is numbered as i*M + j (row-major order)
    - Horizontal links connect (i,j) -> (i,j+1)
    - Vertical links connect (i,j) -> (i+1,j)
    
    Parameters:
    - N: Number of rows
    - M: Number of columns
    - num_od_pairs: Number of OD pairs to generate (default: 1)
    - compute_paths: kept for backward compatibility; if True, the network is
      returned without paths and the caller runs a FlowAssignment
      (all-or-nothing on shortest paths) before the network loading
    - demand_min: Minimum demand value for capped Gaussian distribution (default: None)
    - demand_max: Maximum demand value for capped Gaussian distribution (default: None)
    - demand_mean: Mean of Gaussian distribution for demand (default: None)
    - demand_std: Standard deviation of Gaussian distribution for demand (default: None)
    - ff_time_variation: if > 0, each free-flow time is drawn uniform in
      [(1 - ff_time_variation)/50, 1/50] h, breaking the symmetry of the
      uniform grid (used e.g. by the PURC tests of Route_choice_TR);
      0 (default) keeps all free-flow times at 1/50 h.
    
    Returns:
    - Network object with random demand between OD pairs
    
    Note:
    - If demand_min, demand_max, demand_mean, demand_std are all provided,
      demand values are drawn from a Gaussian distribution N(demand_mean, demand_std)
      and capped to [demand_min, demand_max].
    - If not provided, a fixed demand of 1000 is used for all OD pairs.
    """
    links = []
    
    # Free-flow time of one link: 1/50 h, optionally randomized within
    # [(1 - ff_time_variation)/50, 1/50] to break the grid symmetry
    def ff_time() -> float:
        if ff_time_variation > 0:
            return 1.0 / 50 * random.uniform(1 - ff_time_variation, 1.0)
        return 1.0 / 50
    
    # Create horizontal links (left to right)
    for i in range(N):
        for j in range(M - 1):
            node_a = i * M + j
            node_b = i * M + (j + 1)
            links.append([node_a, node_b, capacity, 1.0, ff_time(), 0])
    
    # Create vertical links (top to bottom)
    for i in range(N - 1):
        for j in range(M):
            node_a = i * M + j
            node_b = (i + 1) * M + j
            links.append([node_a, node_b, capacity, 1.0, ff_time(), 0])
    
    network_df = pd.DataFrame(links, columns=['a_node', 'b_node', 'capacity', 'length', 'free_flow_time', 'b'])
    
    # Generate OD pairs and demand
    all_nodes = list(range(N * M))
    demand_rows = []
    if demand_df is None:
        for _ in range(num_od_pairs):
            # Randomly select two distinct nodes for OD pair
            origin, destination = random.sample(all_nodes, 2)
            
            # Generate demand
            if demand_min is not None and demand_max is not None and demand_mean is not None and demand_std is not None:
                # Draw from Gaussian distribution and cap
                demand = random.gauss(demand_mean, demand_std)
                demand = max(demand_min, min(demand_max, demand))
            else:
                demand = 1000
            
            demand_rows.append([origin, destination, demand])        
    
        demand_df = pd.DataFrame(demand_rows, columns=['O', 'D', 'demand'])
    
    network = Network(network_df, demand_df)
    
    # Add node positions for plotting
    network.node_positions = {}
    for i in range(N):
        for j in range(M):
            node = i * M + j
            network.node_positions[node] = (j, -i)  # x = column, y = -row (so row 0 is at top)
    
    return network
