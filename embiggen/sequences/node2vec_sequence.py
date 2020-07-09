from typing import Tuple

import numpy as np  # type: ignore

from .abstract_node2vec_sequence import AbstractNode2VecSequence


class Node2VecSequence(AbstractNode2VecSequence):

    def __getitem__(self, idx: int) -> Tuple[Tuple[np.ndarray, np.ndarray], None]:
        """Return batch corresponding to given index.

        Parameters
        ---------------
        idx: int,
            Index corresponding to batch to be rendered.

        Returns
        ---------------
        Tuple of tuples with input data.
        """
        return self._graph.node2vec(
            idx,
            self._batch_size,
            self._length,
            iterations=self._iterations,
            window_size=self._window_size,
            shuffle=self._shuffle,
            min_length=self._min_length,
            return_weight=self._return_weight,
            explore_weight=self._explore_weight,
            change_node_type_weight=self._change_node_type_weight,
            change_edge_type_weight=self._change_edge_type_weight,
        ), None
