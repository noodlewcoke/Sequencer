import numpy as np 
from sympy.utilities.iterables import variations

class sequencer:

    def __init__(self, sequence_lengths=1, depth=1, diversity=None, discontiguity_lenghts=0):
        self.sequence_lengths = sequence_lengths
        self.depth = depth
        self.diversity = diversity
        self.discontiguity_lenghts = discontiguity_lenghts

    def uniform_sequence(self, len_data, n_class):
        pass


    def create_dataset(self, data, label_dim, save=None):
        pass

def test(num_labels, sequence_lengths):
    labels = np.arange(num_labels)
    sequences = []
    for r in sequence_lengths:
        for i in list(variations(labels, r, repetition=True)):
            sequences.append(i) 
    return sequences


if __name__ == '__main__':
    seq = sequencer(sequence_lengths=5)
    print(len(test(2, [3])))