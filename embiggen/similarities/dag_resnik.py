from typing import List, Optional, Union
import pandas as pd
import numpy as np
from ensmallen import models, Graph


class DAGResnik:

    def __init__(self):
        self._model = models.DAGResnik()

    def fit(
        self,
        graph: Graph,
        node_frequencies: Optional[np.ndarray] = None,
    ):
        """Fit the Resnik similarity model.

        Parameters
        --------------------
        graph: Graph
            The graph to run predictions on.
        node_frequencies: Optional[np.ndarray] = None
            Optional vector of node frequencies.
        """
        self._model.fit(graph, node_frequencies)

    def get_similarity_from_node_id(
        self,
        src,
        dst
    ) -> float:
        """Return the similarity between the two provided nodes.

        Arguments
        --------------------
        first_node_id: NodeT
            The first node for which to compute the similarity.
        second_node_id: NodeT
            The second node for which to compute the similarity.
        """
        return self._model.get_similarity_from_node_id(src, dst)

    def get_similarities_from_graph(
        self,
        graph: Graph,
        return_predictions_dataframe: bool = False
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Execute predictions on the provided graph.

        Parameters
        --------------------
        graph: Graph
            The graph to run predictions on.
        node_frequencies: Optional[np.ndarray]
            Optional vector of node frequencies.
        return_predictions_dataframe: bool = False
            Whether to return a pandas DataFrame, which as indices has the node IDs.
            By default, a numpy array with the predictions is returned as it weights much less.
        """
        predictions = self._model.get_similarities_from_graph(
            graph,
        )

        if np.isnan(predictions).any():
            raise ValueError(
                "There are NaN values in the predicted probabilities!"
            )

        if return_predictions_dataframe:
            predictions = pd.DataFrame(
                {
                    "predictions": predictions,
                    "sources": graph.get_directed_source_node_ids(),
                    "destinations": graph.get_directed_destination_node_ids(),
                },
            )

        return predictions

    def get_similarities_from_bipartite_graph_from_edge_node_ids(
        self,
        graph: Graph,
        source_node_ids: List[int],
        destination_node_ids: List[int],
        return_predictions_dataframe: bool = False
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Execute predictions probabilities on the provided graph bipartite portion.

        Parameters
        --------------------
        graph: Graph
            The graph from which to extract the edges.
        node_frequencies: Optional[np.ndarray]
            Optional vector of node frequencies.
        source_node_ids: List[int]
            The source nodes of the bipartite graph.
        destination_node_ids: List[int]
            The destination nodes of the bipartite graph.
        return_predictions_dataframe: bool = False
            Whether to return a pandas DataFrame, which as indices has the node IDs.
            By default, a numpy array with the predictions is returned as it weights much less.
        """
        return self.get_similarities_from_graph(
            graph.build_bipartite_graph_from_edge_node_ids(
                source_node_ids=source_node_ids,
                destination_node_ids=destination_node_ids,
                directed=True
            ),
            return_predictions_dataframe=return_predictions_dataframe
        )

    def get_similarities_from_bipartite_graph_from_edge_node_names(
        self,
        graph: Graph,
        source_node_names: List[str],
        destination_node_names: List[str],
        return_predictions_dataframe: bool = False
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Execute predictions probabilities on the provided graph bipartite portion.

        Parameters
        --------------------
        graph: Graph
            The graph from which to extract the edges.
        node_frequencies: Optional[np.ndarray]
            Optional vector of node frequencies.
        source_node_names: List[str]
            The source nodes of the bipartite graph.
        destination_node_names: List[str]
            The destination nodes of the bipartite graph.
        return_predictions_dataframe: bool = False
            Whether to return a pandas DataFrame, which as indices has the node IDs.
            By default, a numpy array with the predictions is returned as it weights much less.
        """
        return self.get_similarities_from_graph(
            graph.build_bipartite_graph_from_edge_node_names(
                source_node_names=source_node_names,
                destination_node_names=destination_node_names,
                directed=True
            ),
            return_predictions_dataframe=return_predictions_dataframe
        )

    def get_similarities_from_bipartite_graph_from_edge_node_prefixes(
        self,
        graph: Graph,
        source_node_prefixes: List[str],
        destination_node_prefixes: List[str],
        return_predictions_dataframe: bool = False
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Execute predictions probabilities on the provided graph bipartite portion.

        Parameters
        --------------------
        graph: Graph
            The graph from which to extract the edges.
        node_frequencies: Optional[np.ndarray]
            Optional vector of node frequencies.
        source_node_prefixes: List[str]
            The source node prefixes of the bipartite graph.
        destination_node_prefixes: List[str]
            The destination node prefixes of the bipartite graph.
        return_predictions_dataframe: bool = False
            Whether to return a pandas DataFrame, which as indices has the node IDs.
            By default, a numpy array with the predictions is returned as it weights much less.
        """
        return self.get_similarities_from_graph(
            graph.build_bipartite_graph_from_edge_node_prefixes(
                source_node_prefixes=source_node_prefixes,
                destination_node_prefixes=destination_node_prefixes,
                directed=True
            ),
            return_predictions_dataframe=return_predictions_dataframe
        )

    def get_similarities_from_bipartite_graph_from_edge_node_types(
        self,
        graph: Graph,
        source_node_types: List[str],
        destination_node_types: List[str],
        return_predictions_dataframe: bool = False
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Execute predictions probabilities on the provided graph bipartite portion.

        Parameters
        --------------------
        graph: Graph
            The graph from which to extract the edges.
        node_frequencies: Optional[np.ndarray]
            Optional vector of node frequencies.
        source_node_types: List[str]
            The source node prefixes of the bipartite graph.
        destination_node_types: List[str]
            The destination node prefixes of the bipartite graph.
        return_predictions_dataframe: bool = False
            Whether to return a pandas DataFrame, which as indices has the node IDs.
            By default, a numpy array with the predictions is returned as it weights much less.
        """
        return self.get_similarities_from_graph(
            graph.build_bipartite_graph_from_edge_node_types(
                source_node_types=source_node_types,
                destination_node_types=destination_node_types,
                directed=True
            ),
            return_predictions_dataframe=return_predictions_dataframe
        )

    def get_similarities_from_clique_graph_from_node_ids(
        self,
        graph: Graph,
        node_ids: List[int],
        return_predictions_dataframe: bool = False
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Execute predictions probabilities on the provided graph bipartite portion.

        Parameters
        --------------------
        graph: Graph
            The graph from which to extract the edges.
        node_frequencies: Optional[np.ndarray]
            Optional vector of node frequencies.
        node_ids: List[int]
            The nodes of the bipartite graph.
        return_predictions_dataframe: bool = False
            Whether to return a pandas DataFrame, which as indices has the node IDs.
            By default, a numpy array with the predictions is returned as it weights much less.
        """
        return self.get_similarities_from_graph(
            graph.build_clique_graph_from_node_ids(
                node_ids=node_ids,
                directed=True
            ),
            return_predictions_dataframe=return_predictions_dataframe
        )

    def get_similarities_from_clique_graph_from_node_names(
        self,
        graph: Graph,
        node_names: List[str],
        return_predictions_dataframe: bool = False
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Execute predictions probabilities on the provided graph bipartite portion.

        Parameters
        --------------------
        graph: Graph
            The graph from which to extract the edges.
        node_frequencies: Optional[np.ndarray]
            Optional vector of node frequencies.
        node_names: List[str]
            The nodes of the bipartite graph.
        return_predictions_dataframe: bool = False
            Whether to return a pandas DataFrame, which as indices has the node IDs.
            By default, a numpy array with the predictions is returned as it weights much less.
        """
        return self.get_similarities_from_graph(
            graph.build_clique_graph_from_node_names(
                node_names=node_names,
                directed=True
            ),
            return_predictions_dataframe=return_predictions_dataframe
        )

    def get_similarities_from_clique_graph_from_node_prefixes(
        self,
        graph: Graph,
        node_prefixes: List[str],
        return_predictions_dataframe: bool = False
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Execute predictions probabilities on the provided graph bipartite portion.

        Parameters
        --------------------
        graph: Graph
            The graph from which to extract the edges.
        node_frequencies: Optional[np.ndarray]
            Optional vector of node frequencies.
        node_prefixes: List[str]
            The node prefixes of the bipartite graph.
        return_predictions_dataframe: bool = False
            Whether to return a pandas DataFrame, which as indices has the node IDs.
            By default, a numpy array with the predictions is returned as it weights much less.
        """
        return self.get_similarities_from_graph(
            graph.build_clique_graph_from_node_prefixes(
                node_prefixes=node_prefixes,
                directed=True
            ),
            return_predictions_dataframe=return_predictions_dataframe
        )

    def get_similarities_from_clique_graph_from_node_types(
        self,
        graph: Graph,
        node_types: List[str],
        return_predictions_dataframe: bool = False
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Execute predictions probabilities on the provided graph bipartite portion.

        Parameters
        --------------------
        graph: Graph
            The graph from which to extract the edges.
        node_frequencies: Optional[np.ndarray]
            Optional vector of node frequencies.
        node_types: List[str]
            The node prefixes of the bipartite graph.
        return_predictions_dataframe: bool = False
            Whether to return a pandas DataFrame, which as indices has the node IDs.
            By default, a numpy array with the predictions is returned as it weights much less.
        """
        return self.get_similarities_from_graph(
            graph.build_clique_graph_from_node_types(
                node_types=node_types,
                directed=True
            ),
            return_predictions_dataframe=return_predictions_dataframe
        )