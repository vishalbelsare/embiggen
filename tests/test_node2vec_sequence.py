import pytest
from embiggen.sequences.node2vec_sequence import Node2VecSequence
from .test_sequences import TestSequences


class TestNode2VecSequences(TestSequences):

    def setUp(self):
        super().setUp()
        self._window_size = 4
        self._length = 100
        self._batch_size = 1
        self._sequence = Node2VecSequence(
            self._graph,
            length=self._length,
            batch_size=self._batch_size,
            window_size=self._window_size
        )

    def test_not_implemented_error(self):
        with pytest.raises(NotImplementedError):
            self._sequence.__getitem__(0)