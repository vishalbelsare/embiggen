"""Submodule providing wrapper for PyKeen's TransD model."""
from typing import Union, Type, Dict, Any, Optional
from pykeen.training import TrainingLoop
from pykeen.models import TransD
from .entity_relation_embedding_model_pykeen import EntityRelationEmbeddingModelPyKeen
from pykeen.triples import CoreTriplesFactory


class TransDPyKeen(EntityRelationEmbeddingModelPyKeen):

    def __init__(
        self,
        embedding_size: int = 100,
        relation_dim: Optional[int] = None,
        scoring_fct_norm: int = 2,
        epochs: int = 100,
        batch_size: int = 2**10,
        training_loop: Union[str, Type[TrainingLoop]
                             ] = "Stochastic Local Closed World Assumption"
    ):
        """Create new PyKeen TransD model.

        Details
        -------------------------
        This is a wrapper of the TransD implementation from the
        PyKeen library. Please refer to the PyKeen library documentation
        for details and posssible errors regarding this model.

        Parameters
        -------------------------
        embedding_size: int = 100
            The dimension of the embedding to compute.
        relation_dim: int = 30
            The dimension of the relation embedding to compute.
        scoring_fct_norm: int = 2
            Norm exponent to use in the loss.
        epochs: int = 100
            The number of epochs to use to train the model for.
        batch_size: int = 2**10
            Size of the training batch.
        device: str = "auto"
            The devide to use to train the model.
            Can either be cpu or cuda.
        training_loop: Union[str, Type[TrainingLoop]
                             ] = "Stochastic Local Closed World Assumption"
            The training loop to use to train the model.
            Can either be:
            - Stochastic Local Closed World Assumption
            - Local Closed World Assumption
        """
        self._scoring_fct_norm = scoring_fct_norm
        self._relation_dim = relation_dim
        super().__init__(
            embedding_size=embedding_size,
            epochs=epochs,
            batch_size=batch_size,
            training_loop=training_loop
        )

    @staticmethod
    def smoke_test_parameters() -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        return dict(
            **EntityRelationEmbeddingModelPyKeen.smoke_test_parameters(),
            scoring_fct_norm=1,
        )

    def parameters(self) -> Dict[str, Any]:
        return {
            **super().parameters(),
            **dict(
                scoring_fct_norm=self._scoring_fct_norm,
                relation_dim=self._relation_dim
            )
        }

    @staticmethod
    def model_name() -> str:
        """Return name of the model."""
        return "TransD"

    def _build_model(
        self,
        triples_factory: CoreTriplesFactory
    ) -> TransD:
        """Build new TransD model for embedding.

        Parameters
        ------------------
        graph: Graph
            The graph to build the model for.
        """
        return TransD(
            triples_factory=triples_factory,
            embedding_dim=self._embedding_size,
            relation_dim=self._relation_dim,
            scoring_fct_norm=self._scoring_fct_norm
        )
