import os.path

from unittest import TestCase

from xn2v import CSFGraph
from xn2v.hetnode2vec_tf import N2vGraph
from xn2v.word2vec import ContinuousBagOfWordsWord2Vec


class TestCBOWconstruction(TestCase):
    """Use the test files in test/data/ppismall to construct a CBOW and test that we can get some random walks."""

    def setUp(self):
        # pos_train = 'tests/data/ppismall/pos_train_edges'
        # neg_test = 'tests/data/ppismall/neg_test_edges'
        # neg_train = 'tests/data/ppismall/neg_train_edges'
        # pos_test = 'tests/data/ppismall/pos_test_edges'

        curdir = os.path.dirname(__file__)
        pos_train = os.path.join(curdir, "data/ppismall/pos_train_edges")
        pos_train = os.path.abspath(pos_train)

        # build graph
        training_graph = CSFGraph(pos_train)

        # obtain data needed to build model
        worddictionary = training_graph.get_node_to_index_map()
        reverse_worddictionary = training_graph.get_index_to_node_map()

        # initialize n2v object
        p, q, gamma = 1, 1, 1
        use_gamma = False
        self.number_of_nodes_in_training = training_graph.node_count()
        self.n2v_graph = N2vGraph(csf_graph=training_graph, p=p, q=q, gamma=gamma, doxn2v=use_gamma)

        # generate random walks
        self.walk_length = 10
        self.num_walks = 5
        self.walks = self.n2v_graph.simulate_walks(num_walks=self.num_walks, walk_length=self.walk_length)
        # walks is now a list of lists of ints

        # build cbow model
        self.cbow = ContinuousBagOfWordsWord2Vec(self.walks,
                                                 worddictionary=worddictionary,
                                                 reverse_worddictionary=reverse_worddictionary,
                                                 num_steps=100)

        self.cbow.train()

    #def test_number_of_walks_performed(self):
    #    # expected number of walks is num_walks times the number of nodes in the training graph
    #    expected_n_walks = self.num_walks * self.number_of_nodes_in_training
    #    self.assertEqual(expected_n_walks, len(self.walks))