"""Test network for the PURC (Perturbed Utility Route Choice) tests.

Used by:
- Route_choice_TR / test_purc.py.

The toy network of Fig. 1 / Section 3.1 of Fosgerau, Paulsen &
Rasmussen (2022), built directly as a QDTA-style network_df and
enhanced in place with exogenous link utilities.
"""

import numpy as np
import pandas as pd

from QDTA.network import Network

# Nodes of the toy network: O, M, D (0-based node ids as in QDTA)
ORIGIN, MIDDLE, DESTINATION = 0, 1, 2


def toy_network(u: dict[int, float] | None = None,
                l: dict[int, float] | None = None) -> Network:
    """The toy network of Fig. 1 / Section 3.1 as a QDTA network.

    Links (1-based link number: a_node, b_node, length, utility rate):
        1: O -> D, l=2, u=-1      (direct route)
        2: O -> M, l=1, u=-1      (shared by routes 2-3 and 2-4)
        3: M -> D, l=1, u=-1
        4: M -> D, l=1, u=-1
        5: M -> O, l=1, u=-1      (opposite of link 2; allows loops)
        6: O -> D, l=2, u=-2      (direct, twice as costly)
    Keys are 1-based link numbers as in the paper.
    """
    default_u = {1: -1.0, 2: -1.0, 3: -1.0, 4: -1.0, 5: -1.0, 6: -2.0}
    default_l = {1: 2.0, 2: 1.0, 3: 1.0, 4: 1.0, 5: 1.0, 6: 2.0}
    u = {**default_u, **(u or {})}
    l = {**default_l, **(l or {})}

    spec = pd.DataFrame([
        (0, 2, l[1]),   # link 1: O -> D
        (0, 1, l[2]),   # link 2: O -> M
        (1, 2, l[3]),   # link 3: M -> D
        (1, 2, l[4]),   # link 4: M -> D
        (1, 0, l[5]),   # link 5: M -> O (loop link)
        (0, 2, l[6]),   # link 6: O -> D
    ], columns=["a_node", "b_node", "length"])
    # complete to the QDTA network_df format. Length and free-flow time are
    # separate attributes; the paper's l_e is the link length, the
    # perturbation's cost base. A free-flow time in the same numbers keeps
    # the toy comparable with the paper's Table 1 (units of the paper).
    spec["free_flow_time"] = spec["length"] / 50.0   # 50 km/h
    spec["capacity"] = np.inf
    spec["b"] = 1          # unidirectional links, as in TNTP networks
    net = Network(spec)

    # exogenous link utilities: the paper's rates u_e = rate_e * l_e,
    # set in the 'utilities' column read by route_choice
    # (same as route_choice.common.set_utility_rates, without the import)
    rates = np.array([u[1], u[2], u[3], u[4], u[5], u[6]])
    net.network_df["utilities"] = rates * net.network_df["length"].astype(float).to_numpy()
    return net
