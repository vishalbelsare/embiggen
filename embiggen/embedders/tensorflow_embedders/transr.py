"""TransR model."""
import tensorflow as tf
from ensmallen import Graph
import pandas as pd
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Reshape
from embiggen.embedders.tensorflow_embedders.siamese import Siamese
from embiggen.utils.abstract_models import EmbeddingResult
from embiggen.layers.tensorflow import FlatEmbedding


class TransRTensorFlow(Siamese):
    """TransR model."""

    def _build_output(
        self,
        srcs_embedding: tf.Tensor,
        dsts_embedding: tf.Tensor,
        not_srcs_embedding: tf.Tensor,
        not_dsts_embedding: tf.Tensor,
        graph: Graph
    ):
        edge_types = Input((1,), dtype=tf.int32, name="Edge Types")
        edge_type_embedding = FlatEmbedding(
            vocabulary_size=graph.get_number_of_edge_types(),
            dimension=self._embedding_size,
            input_length=1,
            mask_zero=graph.has_unknown_edge_types(),
            name="EdgeTypeEmbedding",
        )(edge_types)
        source_edge_type_embedding = Reshape((
            self._embedding_size,
            self._embedding_size
        ))(FlatEmbedding(
            vocabulary_size=graph.get_number_of_edge_types(),
            dimension=self._embedding_size*self._embedding_size,
            input_length=1,
            mask_zero=graph.has_unknown_edge_types(),
            name="SourceEdgeTypeEmbedding",
        )(edge_types))
        destination_edge_type_embedding = Reshape((
            self._embedding_size,
            self._embedding_size
        ))(FlatEmbedding(
            vocabulary_size=graph.get_number_of_edge_types(),
            dimension=self._embedding_size*self._embedding_size,
            input_length=1,
            mask_zero=graph.has_unknown_edge_types(),
            name="DestinationEdgeTypeEmbedding",
        )(edge_types))

        return (
            edge_types,
            0.0,
            tf.einsum(
                'ijk,ij->ij',
                source_edge_type_embedding,
                srcs_embedding
            ) + edge_type_embedding,
            tf.einsum(
                'ijk,ij->ij',
                destination_edge_type_embedding,
                dsts_embedding
            ),
            tf.einsum(
                'ijk,ij->ij',
                source_edge_type_embedding,
                not_srcs_embedding
            ) + edge_type_embedding,
            tf.einsum(
                'ijk,ij->ij',
                destination_edge_type_embedding,
                not_dsts_embedding
            )
        )

    @classmethod
    def model_name(cls) -> str:
        """Returns name of the current model."""
        return "TransR"

    @classmethod
    def requires_edge_types(cls) -> bool:
        return True

    def _extract_embeddings(
        self,
        graph: Graph,
        model: Model,
        return_dataframe: bool
    ) -> EmbeddingResult:
        """Returns embedding from the model.

        Parameters
        ------------------
        graph: Graph
            The graph that was embedded.
        model: Model
            The Keras model used to embed the graph.
        return_dataframe: bool
            Whether to return a dataframe of a numpy array.
        """
        node_embedding = self.get_layer_weights(
            "NodeEmbedding",
            model,
            drop_first_row=False
        )
        edge_type_embedding = self.get_layer_weights(
            "EdgeTypeEmbedding",
            model,
            drop_first_row=graph.has_unknown_edge_types()
        )
        source_edge_type_embedding = self.get_layer_weights(
            "SourceEdgeTypeEmbedding",
            model,
            drop_first_row=graph.has_unknown_edge_types()
        )
        destination_edge_type_embedding = self.get_layer_weights(
            "DestinationEdgeTypeEmbedding",
            model,
            drop_first_row=graph.has_unknown_edge_types()
        )

        if return_dataframe:
            node_embedding = pd.DataFrame(
                node_embedding,
                index=graph.get_node_names()
            )

            edge_type_names = graph.get_unique_edge_type_names()

            edge_type_embedding = pd.DataFrame(
                edge_type_embedding,
                index=edge_type_names
            )

            source_edge_type_embedding = pd.DataFrame(
                source_edge_type_embedding,
                index=edge_type_names
            )

            destination_edge_type_embedding = pd.DataFrame(
                destination_edge_type_embedding,
                index=edge_type_names
            )

        return EmbeddingResult(
            embedding_method_name=self.model_name(),
            node_embeddings=node_embedding,
            edge_type_embeddings=[
                edge_type_embedding,
                source_edge_type_embedding,
                destination_edge_type_embedding
            ]
        )

    @classmethod
    def can_use_node_types(cls) -> bool:
        """Returns whether the model can optionally use node types."""
        return False

    @classmethod
    def requires_edge_types(cls) -> bool:
        """Returns whether the model requires edge types."""
        return True
