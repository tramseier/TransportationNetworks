"""QDTA_RC: test network and demand definitions shared by the QDTA and
Route_choice_TR repositories.

All networks used by the test scripts of the QDTA and route_choice
repos are defined here, so that no network definition is duplicated
across the two code repos. The test scripts import their networks from
this package; each module documents for which tests its networks are
used.
"""

from QDTA_RC.netw_loading_test_networks import (
    bidirectional_corridor_network,
    example_1_network,
    simple_merge_network,
    single_path_corridor_network,
    single_path_network,
)
from QDTA_RC.grid_networks import grid_network
from QDTA_RC.qdta_loading_test_networks import two_parallel_routes_network

__all__ = [
    "bidirectional_corridor_network",
    "example_1_network",
    "grid_network",
    "simple_merge_network",
    "single_path_corridor_network",
    "single_path_network",
    "two_parallel_routes_network",
]
