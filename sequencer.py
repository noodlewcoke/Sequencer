import numpy as np 
from sympy.utilities.iterables import variations
import itertools
from random import shuffle

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
        unseq = np.arange(num_labels)
        sequences = []
        for d in range(depth):
            for r in self.sequence_lengths:
                indices = np.random.randint(0, len(unseq), size=(upper_bounds[d], r))
                for i in unseq[indices]:
                    if d:
                        temp = [list(a) for a in i]
                        sequences.append(sum(temp,[]))
                    else:
                        sequences.append(list(i))

            unseq = np.random.permutation(sequences)
            
            # shuffle(sequences)
            # unseq = np.array(sequences.copy())
            sequences = []
        unseq = [list(a) for a in unseq]
        return sum(unseq,[])

    def time_invariant_seq(self, len_data, n_class):
        pass

    def create_dataset(self, data, label_dim, save=None):
        pass



if __name__ == '__main__':
    sequence = sequencer(sequence_lengths=[3,5])
    seq = sequence.limited_sequence(10, [100,100,100, 100])
    print(seq)
    print(len(seq))
