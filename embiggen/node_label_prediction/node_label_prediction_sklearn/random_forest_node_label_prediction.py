"""Submodule wrapping Random Forest for node label prediction."""
from typing import Dict, Any
from sklearn.ensemble import RandomForestClassifier
from .sklearn_node_label_prediction_adapter import SklearnNodeLabelPredictionAdapter


class RandomForestNodeLabelPrediction(SklearnNodeLabelPredictionAdapter):
    """Create wrapper over Sklearn Random Forest classifier for node label prediction."""

    def __init__(
        self,
        n_estimators: int = 1000,
        criterion: str = "gini",
        max_depth: int = 10,
        min_samples_split: int = 2,
        min_samples_leaf: int = 1,
        min_weight_fraction_leaf: float = 0.,
        max_features="auto",
        max_leaf_nodes=None,
        min_impurity_decrease=0.,
        min_impurity_split=None,
        bootstrap=True,
        oob_score=False,
        n_jobs=-1,
        verbose=0,
        warm_start=False,
        class_weight=None,
        ccp_alpha=0.0,
        max_samples=None,
        random_state: int = 42
    ):
        """Create the Random Forest for Edge  Prediction."""
        self._n_estimators = n_estimators
        self._criterion = criterion
        self._max_depth = max_depth
        self._min_samples_split = min_samples_split
        self._min_samples_leaf = min_samples_leaf
        self._min_weight_fraction_leaf = min_weight_fraction_leaf
        self._max_features = max_features
        self._max_leaf_nodes = max_leaf_nodes
        self._min_impurity_decrease = min_impurity_decrease
        self._min_impurity_split = min_impurity_split
        self._bootstrap = bootstrap
        self._oob_score = oob_score
        self._n_jobs = n_jobs
        self._verbose = verbose
        self._warm_start = warm_start
        self._class_weight = class_weight
        self._ccp_alpha = ccp_alpha
        self._max_samples = max_samples

        super().__init__(
            RandomForestClassifier(
                n_estimators=n_estimators,
                criterion=criterion,
                max_depth=max_depth,
                min_samples_split=min_samples_split,
                min_samples_leaf=min_samples_leaf,
                min_weight_fraction_leaf=min_weight_fraction_leaf,
                max_features=max_features,
                max_leaf_nodes=max_leaf_nodes,
                min_impurity_decrease=min_impurity_decrease,
                min_impurity_split=min_impurity_split,
                bootstrap=bootstrap,
                oob_score=oob_score,
                n_jobs=n_jobs,
                random_state=random_state,
                verbose=verbose,
                warm_start=warm_start,
                class_weight=class_weight,
                ccp_alpha=ccp_alpha,
                max_samples=max_samples
            ),
            random_state
        )

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters used for this model."""
        return {
            **super().parameters(),
            **dict(
                n_estimators = self._n_estimators,
                criterion = self._criterion,
                max_depth = self._max_depth,
                min_samples_split = self._min_samples_split,
                min_samples_leaf = self._min_samples_leaf,
                min_weight_fraction_leaf = self._min_weight_fraction_leaf,
                max_features = self._max_features,
                max_leaf_nodes = self._max_leaf_nodes,
                min_impurity_decrease = self._min_impurity_decrease,
                min_impurity_split = self._min_impurity_split,
                bootstrap = self._bootstrap,
                oob_score = self._oob_score,
                n_jobs = self._n_jobs,
                verbose = self._verbose,
                warm_start = self._warm_start,
                class_weight = self._class_weight,
                ccp_alpha = self._ccp_alpha,
                max_samples = self._max_samples,
            )
        }

    @staticmethod
    def model_name() -> str:
        return "Random Forest Classifier"