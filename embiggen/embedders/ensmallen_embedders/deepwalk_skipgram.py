"""Module providing DeepWalk SkipGram model implementation."""
from typing import Optional, Dict, Any
from embiggen.embedders.ensmallen_embedders.node2vec import Node2VecEnsmallen


class DeepWalkSkipGramEnsmallen(Node2VecEnsmallen):
    """Class providing DeepWalk SkipGram implemeted in Rust from Ensmallen."""

    def __init__(
        self,
        embedding_size: int = 100,
        epochs: int = 10,
        clipping_value: float = 6.0,
        number_of_negative_samples: int = 10,
        walk_length: int = 128,
        iterations: int = 10,
        window_size: int = 10,
        max_neighbours: Optional[int] = 100,
        learning_rate: float = 0.01,
        learning_rate_decay: float = 0.9,
        normalize_by_degree: bool = False,
        stochastic_downsample_by_degree: Optional[bool] = False,
        normalize_learning_rate_by_degree: Optional[bool] = False,
        use_scale_free_distribution: Optional[bool] = True,
        random_state: int = 42,
        enable_cache: bool = False
    ):
        """Create new abstract DeepWalk method.

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
        max_neighbours: Optional[int] = 100
            Number of maximum neighbours to consider when using approximated walks.
            By default, None, we execute exact random walks.
            This is mainly useful for graphs containing nodes with high degrees.
        learning_rate: float = 0.01
            The learning rate to use to train the Node2Vec model. By default 0.01.
        learning_rate_decay: float = 0.9
            Factor to reduce the learning rate for at each epoch. By default 0.9.
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
            model_name="SkipGram",
            embedding_size=embedding_size,
            epochs=epochs,
            clipping_value=clipping_value,
            number_of_negative_samples=number_of_negative_samples,
            walk_length=walk_length,
            iterations=iterations,
            window_size=window_size,
            max_neighbours=max_neighbours,
            learning_rate=learning_rate,
            learning_rate_decay=learning_rate_decay,
            normalize_by_degree=normalize_by_degree,
            stochastic_downsample_by_degree=stochastic_downsample_by_degree,
            normalize_learning_rate_by_degree=normalize_learning_rate_by_degree,
            use_scale_free_distribution=use_scale_free_distribution,
            random_state=random_state,
            enable_cache=enable_cache
        )

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        removed = [
            "return_weight",
            "explore_weight",
            "change_node_type_weight",
            "change_edge_type_weight"
        ]
        return dict(
            **{
                key: value
                for key, value in super().parameters().items()
                if key not in removed
            }
        )
    
    @classmethod
    def model_name(cls) -> str:
        """Returns name of the model."""
        return "DeepWalk SkipGram"

    @classmethod
    def requires_node_types(cls) -> bool:
        return False

    @classmethod
    def requires_edge_types(cls) -> bool:
        return False