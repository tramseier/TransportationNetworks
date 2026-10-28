"""Test network for the QDTA + route choice integration test.

Used by:
- Route_choice_TR / test_qdta_loading.py.

Two parallel routes R -> {B, C} -> D -> S (integer node ids 0..4, as
QDTA requires): the routes split at the ORIGIN, so a queue on the
bottleneck link 2 (R -> C) increases the travel time of route 2 only
and the re-assignment on the current times shifts flow to route 1.
Route 1: links 1, 3, 5; route 2: links 2, 4, 5.
"""

import pandas as pd

from QDTA.network import Network

# Nodes of the two-route toy network (integer ids, as QDTA requires)
R, B, C, D, S = range(5)

# OD pair and demand of the two-route toy network
ORIGIN, DESTINATION = R, S
DEMAND = 2000.0

# Node positions for plotting the two-route toy network
NODE_POS = {R: (0, 0), B: (1, 1), C: (1, -1), D: (2, 0), S: (3, 0)}


def two_parallel_routes_network() -> Network:
    """The two-route toy network as a QDTA network: two parallel routes
    R -> {B, C} -> D -> S sharing only the last link, with link 2 (R -> C)
    as the bottleneck (capacity 900 < demand 2000), so a loading shifts
    the MNL assignment towards route 1 (links 1, 3, 5)."""
    links = pd.DataFrame([
        [1, R, B, 1000, 5.0, 5.0 / 50, 1],
        [2, R, C, 900, 5.0, 5.0 / 50, 1],    # bottleneck
        [3, B, D, 1000, 5.0, 5.0 / 50, 1],
        [4, C, D, 1000, 5.0, 5.0 / 50, 1],
        [5, D, S, 3000, 5.0, 5.0 / 50, 1],
    ], columns=["link_id", "a_node", "b_node", "capacity", "length",
                "free_flow_time", "b"]).set_index("link_id")
    demand = pd.DataFrame([[R, S, DEMAND]], columns=["O", "D", "demand"])
    net = Network(links, demand)
    net.node_positions = NODE_POS       # for the plots
    return net
