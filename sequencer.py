import numpy as np 
from sympy.utilities.iterables import variations


#TODO: Exceptions :: sequence_lengths != 0 or [2,2]
#TODO: Returning a sequence map :: e.g. histogram
#TODO: Sequence types: entropy, advancing, combination
class sequencer:

    def __init__(self, sequence_lengths=[1], diversity=None, discontiguity_lenghts=0):
        self.sequence_lengths = sequence_lengths
        self.diversity = diversity
        self.discontiguity_lenghts = discontiguity_lenghts

    def limited_sequence(self, num_labels, upper_bounds):
        depth = len(upper_bounds)
        labels = np.arange(num_labels)
        sequences = []
        for d in range(depth):
            for r in self.sequence_lengths:
                for i in list(variations(range(len(labels)), r, repetition=True)):
                    sequences.append(i)
            labels = labels[np.random.permutation(sequences)[:upper_bounds[d]]]
            sequences = []
        return labels

    def time_invariant_seq(self, len_data, n_class):
        pass

    def create_dataset(self, data, label_dim, save=None):
        pass

def test(num_labels, sequence_lengths, upper_bounds):

    depth = len(upper_bounds)
    labels = np.arange(num_labels)
    sequences = []
    for r in sequence_lengths:
        for i in list(variations(labels, r, repetition=True)):
            sequences.append(i) 
    base = np.random.permutation(sequences)[:upper_bounds[0]]

    sequences = []   
    for r in sequence_lengths:
        for i in list(variations(base, r, repetition=True)):
            sequences.append(i)
    

    
    return np.random.permutation(sequences)[:upper_bounds[1]]
    # return np.concatenate([*base], axis=0)


if __name__ == '__main__':
    sequence = sequencer(sequence_lengths=[2])
    seq = sequence.limited_sequence(10, [100,50,10])
    # seq = test(4, [2,3], [25, 5])
    # seqt = set([tuple(set(s)) for s in seq])
    print(seq)
