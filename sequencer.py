import numpy as np 
from sympy.utilities.iterables import variations
import itertools
from random import shuffle
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#TODO: Exceptions :: sequence_lengths != 0 or [2,2]
#TODO: Sequence types: entropy, advancing, combination
#TODO: Discontiguous sequences
#TODO: Make fontsize in rectangles 'adaptive'
#TODO: ID sequences and plot the sequence, its color and its ID under MAP

class sequencer:

    def __init__(self, sequence_lengths=[1], enable_plot=False, diversity=None, discontiguity_lenghts=0):
        self.sequence_lengths = sequence_lengths
        self.diversity = diversity
        self.discontiguity_lenghts = discontiguity_lenghts
        self.enable_plot = enable_plot


    def limited_sequence(self, num_labels, upper_bounds):
        self.depth = len(upper_bounds)
        
        self.sequence_bank = {t:[] for t in range(self.depth)}
        self.unseq = np.arange(num_labels)
        sequences = []
        for d in range(self.depth):
            for r in self.sequence_lengths:
                indices = np.random.randint(0, len(self.unseq), size=(upper_bounds[d], r))
                for i in self.unseq[indices]:
                    if d:
                        temp = [list(a) for a in i]
                        sequences.append(sum(temp,[]))
                    else:
                        sequences.append(list(i))
            if self.enable_plot: self.sequence_bank[d].append(sequences)
            self.unseq = np.random.permutation(sequences)
            sequences = []
        self.unseq = sum([list(a) for a in self.unseq], [])
        return self.unseq

    def sequence_map(self, height=1, show_seq_name=False):
        str_full = ''.join([str(i) for i in self.unseq])
        maxX = len(str_full)
        maxY = self.depth*height
        plt.figure(figsize=(maxX, maxY))
        plt.xlim(0, maxX); plt.ylim(0,maxY)
        fig, ax = plt.gcf(), plt.gca()
        x_pos = [0 for i in range(self.depth)]
        for d in range(self.depth-1, -1, -1):
            color = np.random.random([len(self.sequence_bank[d][0]), 3])
            for i in self.sequence_bank[d][0]:
                str_seq = ''.join(str(j) for j in i)
                x = 0
                while True:
                    x = str_full.find(str_seq, x)
                    if not x==-1:
                        ind = self.sequence_bank[d][0].index(i)
                        ax.add_patch(Rectangle((x, d*height), len(str_seq), height, color=color[ind], edgecolor=(1,1,1)))
                        if show_seq_name: ax.text(x+0.5*len(str_seq), d*height+0.5*height, str_seq, 
                                horizontalalignment='center', verticalalignment='center', fontsize=5, color='w')
                        x +=1
                    elif x==-1:
                        break
        plt.show()
        pass

    def plot_sequences(self): #Not a good idea to take 
        if self.enable_plot:
            str_full = ''.join([str(i) for i in self.unseq])
            str_small = {t:[] for t in range(self.depth)}
            for d,l in self.sequence_bank.items():
                for seq in l[0]:
                    str_seq = ''.join([str(a) for a in seq])
                    print(str_seq)
                    counter, flag, i = 0, True, 0 
                    while flag:
                        i = str_full.find(str_seq, i)
                        print(i)
                        if not i == -1: 
                            counter +=1; 
                            i+=1
                        elif i== -1:
                                str_small[d].append(counter)
                                counter, flag, i = 0, False, 0
                                break

            for d,l in str_small.items():
                plt.hist(l[0], bins=len(l))
                # plt.plot(l[0], color='r')
                plt.title("d{}".format(d))
                plt.show()
        else:
            print("Plotting was not enabled! You can enable plotting by using sequencer::enable_plot() function.")

    def enable_plot(self):
        self.enable_plot = True
        print("Please re-run sequence function, then apply sequencer::plot_sequences().")


    def create_dataset(self, data, label_dim, save=None):
        pass



if __name__ == '__main__':
    sequence = sequencer(sequence_lengths=[3,5], enable_plot=True)
    seq = sequence.limited_sequence(10,[10,10,10])
    # sequence.plot_sequences()
    sequence.sequence_map()