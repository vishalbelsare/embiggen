"""Module providing abstract Node2Vec implementation."""
from typing import Optional
from ensmallen import Graph
from .ensmallen_embedder import EnsmallenEmbedder


class Node2Vec(EnsmallenEmbedder):
    """Abstract class for Node2Vec algorithms."""

    def __init__(
        self,
        embedding_size: int = 100,
        epochs: int = 10,
        number_of_negative_samples: int = 5,
        walk_length: int = 128,
        iterations: int = 1,
        window_size: int = 4,
        return_weight: float = 1.0,
        explore_weight: float = 1.0,
        change_node_type_weight: float = 1.0,
        change_edge_type_weight: float = 1.0,
        max_neighbours: Optional[int] = 100,
        learning_rate: float = 0.025,
        normalize_by_degree: bool = False,
        random_state: int = 42,
        verbose: bool = True
    ):
        """Create new abstract Node2Vec method.
        
        Parameters
        --------------------------
        embedding_size: int = 100
            Dimension of the embedding.
        epochs: int = 10
            Number of epochs to train the model for.
        window_size: int = 4
            Window size for the local context.
            On the borders the window size is trimmed.
        number_of_negative_samples: int = 5
            The number of negative classes to randomly sample per batch.
            This single sample of negative classes is evaluated for each element in the batch.
        walk_length: int = 128
            Maximal length of the walks.
        iterations: int = 1
            Number of iterations of the single walks.
        window_size: int = 4
            Window size for the local context.
            On the borders the window size is trimmed.
        return_weight: float = 1.0
            Weight on the probability of returning to the same node the walk just came from
            Having this higher tends the walks to be
            more like a Breadth-First Search.
            Having this very high  (> 2) makes search very local.
            Equal to the inverse of p in the Node2Vec paper.
        explore_weight: float = 1.0
            Weight on the probability of visiting a neighbor node
            to the one we're coming from in the random walk
            Having this higher tends the walks to be
            more like a Depth-First Search.
            Having this very high makes search more outward.
            Having this very low makes search very local.
            Equal to the inverse of q in the Node2Vec paper.
        change_node_type_weight: float = 1.0
            Weight on the probability of visiting a neighbor node of a
            different type than the previous node. This only applies to
            colored graphs, otherwise it has no impact.
        change_edge_type_weight: float = 1.0
            Weight on the probability of visiting a neighbor edge of a
            different type than the previous edge. This only applies to
            multigraphs, otherwise it has no impact.
        max_neighbours: Optional[int] = 100
            Number of maximum neighbours to consider when using approximated walks.
            By default, None, we execute exact random walks.
            This is mainly useful for graphs containing nodes with high degrees.
        learning_rate: float = 0.025
            The learning rate to use to train the Node2Vec model.
        normalize_by_degree: bool = False
            Whether to normalize the random walk by the node degree
            of the destination node degrees.
        random_state: int = 42
            The random state to reproduce the training sequence.
        verbose: bool = True
            Whether to show loading bars
        """
        self._epochs = epochs
        self._number_of_negative_samples = number_of_negative_samples
        self._walk_length = walk_length
        self._iterations = iterations
        self._window_size = window_size
        self._return_weight = return_weight
        self._explore_weight = explore_weight
        self._change_node_type_weight = change_node_type_weight
        self._change_edge_type_weight = change_edge_type_weight
        self._max_neighbours = max_neighbours
        self._learning_rate = learning_rate
        self._normalize_by_degree = normalize_by_degree
        self._random_state = random_state
        
        super().__init__(
            embedding_size=embedding_size,
            verbose=verbose
        )