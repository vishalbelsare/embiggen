"""Module providing WalkletsEnsmallen model implementation."""
from typing import Optional, Dict, Any
from embiggen.embedders.ensmallen_embedders.node2vec import Node2VecEnsmallen
from embiggen.utils.abstract_models.abstract_model import abstract_class

@abstract_class
class WalkletsEnsmallen(Node2VecEnsmallen):
    """Class providing WalkletsEnsmallen implemeted in Rust from Ensmallen."""
    
    def __init__(
        self,
        embedding_size: int = 100,
        epochs: int = 10,
        clipping_value: float = 6.0,
        number_of_negative_samples: int = 10,
        walk_length: int = 128,
        iterations: int = 10,
        window_size: int = 10,
        return_weight: float = 1.0,
        explore_weight: float = 1.0,
        max_neighbours: Optional[int] = 100,
        learning_rate: float = 0.05,
        learning_rate_decay: float = 0.9,
        alpha: float = 0.75,
        normalize_by_degree: bool = False,
        stochastic_downsample_by_degree: Optional[bool] = False,
        normalize_learning_rate_by_degree: Optional[bool] = False,
        use_scale_free_distribution: Optional[bool] = True,
        random_state: int = 42,
        enable_cache: bool = False
    ):
        """Create new abstract Node2Vec method.

        Parameters
        --------------------------
        embedding_size: int = 100
            Dimension of the embedding.
        epochs: int = 10
            Number of epochs to train the model for.
        clipping_value: float = 6.0
            Value at which we clip the dot product, mostly for numerical stability issues.
            By default, `6.0`, where the loss is already close to zero.
        number_of_negative_samples: int = 10
            The number of negative classes to randomly sample per batch.
            This single sample of negative classes is evaluated for each element in the batch.
        walk_length: int = 128
            Maximal length of the walks.
        iterations: int = 10
            Number of iterations of the single walks.
        window_size: int = 10
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
        max_neighbours: Optional[int] = 100
            Number of maximum neighbours to consider when using approximated walks.
            By default, None, we execute exact random walks.
            This is mainly useful for graphs containing nodes with high degrees.
        learning_rate: float = 0.05
            The learning rate to use to train the Node2Vec model. By default 0.01.
        learning_rate_decay: float = 0.9
            Factor to reduce the learning rate for at each epoch. By default 0.9.
        alpha: float = 0.75
            Alpha parameter for GloVe's loss.
        normalize_by_degree: bool = False
            Whether to normalize the random walk by the node degree
            of the destination node degrees.
        stochastic_downsample_by_degree: Optional[bool] = False
            Randomly skip samples with probability proportional to the degree of the central node. By default false.
        normalize_learning_rate_by_degree: Optional[bool] = False
            Divide the learning rate by the degree of the central node. By default false.
        use_scale_free_distribution: Optional[bool] = True
            Sample negatives proportionally to their degree. By default true.
        random_state: int = 42
            The random state to reproduce the training sequence.
        enable_cache: bool = False
            Whether to enable the cache, that is to
            store the computed embedding.
        """
        super().__init__(
            embedding_size=embedding_size // window_size,
            epochs=epochs,
            clipping_value=clipping_value,
            number_of_negative_samples=number_of_negative_samples,
            walk_length=walk_length,
            iterations=iterations,
            window_size=window_size,
            return_weight=return_weight,
            explore_weight=explore_weight,
            max_neighbours=max_neighbours,
            learning_rate=learning_rate,
            learning_rate_decay=learning_rate_decay,
            alpha=alpha,
            normalize_by_degree=normalize_by_degree,
            stochastic_downsample_by_degree=stochastic_downsample_by_degree,
            normalize_learning_rate_by_degree=normalize_learning_rate_by_degree,
            use_scale_free_distribution=use_scale_free_distribution,
            random_state=random_state,
            enable_cache=enable_cache
        )
    
    def parameters(self) -> Dict[str, Any]:
        """Returns parameters of the model."""
        parameters = super().parameters()
        parameters["embedding_size"] = parameters["embedding_size"] * parameters["window_size"]
        return parameters

    @classmethod
    def requires_node_types(cls) -> bool:
        return False

    @classmethod
    def requires_edge_types(cls) -> bool:
        return False