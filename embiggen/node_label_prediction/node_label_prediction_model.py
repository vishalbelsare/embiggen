"""Module providing abstract node label prediction model."""
from typing import Optional, Union, List, Dict, Any, Tuple
import pandas as pd
import numpy as np
import warnings
from ensmallen import Graph
from ..utils import AbstractClassifierModel, AbstractEmbeddingModel, abstract_class, format_list


@abstract_class
class AbstractNodeLabelPredictionModel(AbstractClassifierModel):
    """Class defining an abstract node label prediction model."""

    def __init__(self):
        self._is_binary_prediction_task = None
        self._is_multilabel_prediction_task = None
        super().__init__()

    @staticmethod
    def requires_node_types() -> bool:
        """Returns whether this method requires node types."""
        return True

    @staticmethod
    def task_name() -> str:
        """Returns name of the task this model is used for."""
        return "Node Label Prediction"

    @staticmethod
    def is_topological() -> bool:
        return False

    def get_available_evaluation_schemas(self) -> List[str]:
        """Returns available evaluation schemas for this task."""
        return [
            "Stratified Monte Carlo",
            "Monte Carlo",
            "Stratified Kfold",
            "Kfold"
        ]

    def is_binary_prediction_task(self) -> bool:
        """Returns whether the model was fit on a binary prediction task."""
        return self._is_binary_prediction_task

    def is_multilabel_prediction_task(self) -> bool:
        """Returns whether the model was fit on a multilabel prediction task."""
        return self._is_multilabel_prediction_task

    @classmethod
    def split_graph_following_evaluation_schema(
        cls,
        graph: Graph,
        evaluation_schema: str,
        random_state: int,
        holdout_number: int,
        **holdouts_kwargs: Dict
    ) -> Tuple[Graph]:
        """Return train and test graphs tuple following the provided evaluation schema.

        Parameters
        ----------------------
        graph: Graph
            The graph to split.
        evaluation_schema: str
            The evaluation schema to follow.
        random_state: int
            The random state for the evaluation
        holdout_number: int
            The current holdout number.
        holdouts_kwargs: Dict[str, Any]
            The kwargs to be forwarded to the holdout method.
        """
        if evaluation_schema in ("Stratified Monte Carlo", "Monte Carlo"):
            return graph.get_node_label_holdout_graphs(
                **holdouts_kwargs,
                use_stratification="Stratified" in evaluation_schema,
                random_state=random_state+holdout_number,
            )
        if evaluation_schema in ("Kfold", "Stratified Kfold"):
            return graph.get_node_label_kfold(
                **holdouts_kwargs,
                k_index=holdout_number,
                use_stratification="Stratified" in evaluation_schema,
                random_state=random_state,
            )
        raise ValueError(
            f"The requested evaluation schema `{evaluation_schema}` "
            "is not available. The available evaluation schemas "
            f"are: {format_list(cls.get_available_evaluation_schemas())}."
        )

    @classmethod
    def _prepare_evaluation(
        cls,
        graph: Graph,
        train: Graph,
        test: Graph,
        support: Optional[Graph] = None,
        subgraph_of_interest: Optional[Graph] = None,
        random_state: int = 42,
        verbose: bool = True,
        **kwargs: Dict
    ) -> Dict[str, Any]:
        """Return additional custom parameters for the current holdout."""
        return {}

    def _evaluate(
        self,
        graph: Graph,
        train: Graph,
        test: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]] = None,
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]] = None,
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[str, pd.DataFrame, np.ndarray]]]] = None,
        subgraph_of_interest: Optional[Graph] = None,
        random_state: int = 42,
        verbose: bool = True,
    ) -> List[Dict[str, Any]]:
        """Return model evaluation on the provided graphs."""
        train_size = train.get_known_node_types_number() / graph.get_known_node_types_number()

        if self.is_multilabel_prediction_task():
            labels = graph.get_one_hot_encoded_node_types()
        elif self.is_binary_prediction_task():
            labels = graph.get_boolean_node_type_ids()
        else:
            labels = graph.get_single_label_node_type_ids()

        performance = []
        for evaluation_mode, evaluation_graph in (
            ("train", train),
            ("test", test),
        ):
            prediction_probabilities = self.predict_proba(
                evaluation_graph,
                support=support,
                node_features=node_features,
                node_type_features=node_type_features,
                edge_features=edge_features
            )

            if self.is_binary_prediction_task():
                predictions = prediction_probabilities
            elif self.is_multilabel_prediction_task():
                predictions = prediction_probabilities > 0.5
            else:
                predictions = prediction_probabilities.argmax(axis=-1)

            mask = evaluation_graph.get_known_node_types_mask()
            prediction_probabilities = prediction_probabilities[mask]
            predictions = predictions[mask]
            labels_subset = labels[mask]

            performance.append({
                "evaluation_mode": evaluation_mode,
                "train_size": train_size,
                "known_nodes_number": evaluation_graph.get_known_node_types_number(),
                **self.evaluate_predictions(
                    labels_subset,
                    predictions,
                ),
                **self.evaluate_prediction_probabilities(
                    labels_subset,
                    prediction_probabilities,
                ),
            })

        return performance

    def predict(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
    ) -> np.ndarray:
        """Execute predictions on the provided graph.

        Parameters
        --------------------
        graph: Graph
            The graph to run predictions on.
        support: Optional[Graph] = None
            The graph describiding the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological classifiers
            such as Graph Convolutional Networks.
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node features to use.
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node type features to use.
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge features to use.
        """
        if edge_features is not None:
            raise NotImplementedError(
                "Currently edge features are not supported in node-label prediction models."
            )

        if node_type_features is not None:
            raise NotImplementedError(
                "Support for node type features is not currently available for any "
                "of the node-label prediction models."
            )

        return super().predict(graph, support=support, node_features=node_features)

    def predict_proba(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
    ) -> np.ndarray:
        """Execute predictions on the provided graph.

        Parameters
        --------------------
        graph: Graph
            The graph to run predictions on.
        support: Optional[Graph] = None
            The graph describiding the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological classifiers
            such as Graph Convolutional Networks.
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node features to use.
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node type features to use.
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge features to use.
        """
        if edge_features is not None:
            raise NotImplementedError(
                "Currently edge features are not supported in node-label prediction models."
            )

        if node_type_features is not None:
            raise NotImplementedError(
                "Support for node type features is not currently available for any "
                "of the node-label prediction models."
            )

        return super().predict_proba(graph, support=support, node_features=node_features)

    def fit(
        self,
        graph: Graph,
        support: Optional[Graph] = None,
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        node_type_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None,
    ):
        """Execute predictions on the provided graph.

        Parameters
        --------------------
        graph: Graph
            The graph to run predictions on.
        support: Optional[Graph] = None
            The graph describiding the topological structure that
            includes also the above graph. This parameter
            is mostly useful for topological classifiers
            such as Graph Convolutional Networks.
        node_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The node features to use.
        node_type_features: Optional[Union[str, pd.DataFrame, np.ndarray, AbstractEmbeddingModel, List[Union[str, pd.DataFrame, np.ndarray, AbstractEmbeddingModel]]]] = None
            The node type features to use.
        edge_features: Optional[Union[pd.DataFrame, np.ndarray, List[Union[pd.DataFrame, np.ndarray]]]] = None
            The edge features to use.
        """
        if edge_features is not None:
            raise NotImplementedError(
                "Currently edge features are not supported in node-label prediction models."
            )

        if node_type_features is not None:
            raise NotImplementedError(
                "Support for node type features is not currently available for any "
                "of the node-label prediction models."
            )

        self._is_binary_prediction_task = graph.get_node_types_number() == 2
        self._is_multilabel_prediction_task = graph.has_multilabel_node_types()

        node_type_counts = graph.get_node_type_names_counts_hashmap()
        most_common_node_type_name, most_common_count = max(
            node_type_counts.items(),
            key=lambda x: x[1]
        )
        least_common_node_type_name, least_common_count = min(
            node_type_counts.items(),
            key=lambda x: x[1]
        )

        if most_common_count > least_common_count * 20:
            warnings.warn(
                (
                    "Please do be advised that this graph defines "
                    "an unbalanced node-label prediction task, with the "
                    "most common node type `{}` appearing {} times, "
                    "while the least common one, `{}`, appears only `{}` times. "
                    "Do take this into account when designing the node-label prediction model."
                ).format(
                    most_common_node_type_name, most_common_count,
                    least_common_node_type_name, least_common_count
                )
            )

        super().fit(
            graph=graph,
            support=support,
            node_features=node_features,
            edge_features=None,
        )

    @staticmethod
    def can_use_node_types() -> bool:
        """Returns whether the model can optionally use node types."""
        return True

    def is_using_node_types(self) -> bool:
        """Returns whether the model is parametrized to use node types."""
        return True

    @staticmethod
    def task_involves_edge_weights() -> bool:
        """Returns whether the model task involves edge weights."""
        return False

    @staticmethod
    def task_involves_edge_types() -> bool:
        """Returns whether the model task involves edge types."""
        return False

    @staticmethod
    def task_involves_node_types() -> bool:
        """Returns whether the model task involves node types."""
        return True

    @staticmethod
    def task_involves_topology() -> bool:
        """Returns whether the model task involves topology."""
        return False