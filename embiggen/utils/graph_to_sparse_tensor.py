"""Submodule with utility to convert graph to sparse tensor."""
import tensorflow as tf
from ensmallen_graph import EnsmallenGraph


def graph_to_sparse_tensor(
    graph: EnsmallenGraph,
    use_weights: bool
) -> tf.SparseTensor:
    """Returns provided graph as sparse Tensor.

    Parameters
    -------------------
    graph: EnsmallenGraph,
        The graph to convert.
    use_weights: bool,
        Whether to load the graph weights.

    Raises
    -------------------
    ValueError,
        If the weights are requested but the graph does not contain any.
    ValueError,
        If the graph contains singletons.
    ValueError,
        If the graph is a multigraph.

    Returns
    -------------------
    SparseTensor with (weighted) adjacency matrix.
    """
    if use_weights and not graph.has_edge_weights():
        raise ValueError(
            "Weighted were requested but the provided graph "
            "does not contain any edge weight."
        )

    if graph.has_singleton_nodes():
        raise ValueError(
            "The GCN model does not support operations on graph containing "
            "singletons. You need to either drop the singleton nodes or "
            "add to them a singleton."
        )

    if graph.is_multigraph():
        raise ValueError(
            "The GCN model does not support operations on a multigraph. "
            "You need to drop the parallel edges in order to execute this "
            "model."
        )

    return tf.SparseTensor(
        graph.get_edge_node_ids(directed=True),
        (
            graph.get_edge_weights()
            if use_weights
            else tf.ones(graph.get_directed_edges_number())
        ),
        (graph.get_nodes_number(), graph.get_nodes_number()),
    )