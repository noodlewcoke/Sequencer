import numpy as np 
from sympy.utilities.iterables import variations
import itertools
import torch
from torchvision import datasets, transforms
from random import shuffle
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.gridspec as gridspec

#TODO: Exceptions :: sequence_lengths != 0 or [2,2]
#TODO: Sequence types: entropy, advancing, combination
#TODO: Discontiguous sequences
#TODO: Make fontsize in rectangles 'adaptive'
#TODO: ID sequences and plot the sequence, its color and its ID under MAP
#TODO: Test create_dataset function and 
class sequencer:

    def __init__(self, sequence_lengths=[1], enable_plot=False, diversity=None, discontiguity_lenghts=0):
        self.sequence_lengths = sequence_lengths
        self.diversity = diversity
        self.discontiguity_lenghts = discontiguity_lenghts
        self.enable_plot = enable_plot


    def limited_sequence(self, num_labels, upper_bounds):
        self.depth = len(upper_bounds)
        self.num_labels = num_labels
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

    def sequence_map(self, height=0.1, show_seq_name=False):
        str_full = ''.join([str(i) for i in self.unseq])
        maxX = len(str_full)
        maxY = self.depth*height
        plt.figure(figsize=(maxX, maxY), frameon=False)
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
        # plt.axis('off')
        plt.ylabel('Depth of Sequence')
        plt.xlabel('timestep')
        # plt.savefig('Saved/map.png')
        plt.show()

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


    def create_dataset(self, data, label, reuse_data=True, save=None):
        self.traverser = [0 for i in range(self.num_labels)]
        self.length = len(data)
        new_dataset = []
        for i in self.unseq:
            t = self.traverser[i]
            while True:
                d = data[t%self.length]
                if label[t%self.length]==i:
                    new_dataset.append(d)
                    # if t+1==len(data):
                    #     self.traverser[i] = 0
                    # else:
                    self.traverser[i] = t+1
                    break
                else:
                    if t+1==len(data):
                        if self.traverser[i]==0:
                            print("WARNING: Sequence does not contain label {}".format(self.traverser[i]))
                            break
                        # t=0
                    t+=1
                    # else:
                    #     t+=1
        if isinstance(save, str):
            np.load(save)
        return np.array(new_dataset)

def plot(samples):
    fig = plt.figure(figsize=(1,5))
    gs = gridspec.GridSpec(1,5)
    gs.update(wspace=0.05, hspace=0.05)

    for i, sample in enumerate(samples):
        ax = plt.subplot(gs[i])
        plt.axis('off')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_aspect('equal')
        plt.imshow(sample.reshape(28,28), cmap='Greys_r')

    return fig

if __name__ == '__main__':
    sequence = sequencer(sequence_lengths=[5], enable_plot=True)
    seq = sequence.limited_sequence(10,[10,10,10, 10])
    print(len(seq))
    # sequence.plot_sequences()
    sequence.sequence_map()
    data = []
    train_loader = torch.utils.data.DataLoader(datasets.MNIST('../data', train=True, download=True, transform=transforms.Compose([transforms.ToTensor()])), batch_size=60000)
    # for i in train_loader:
    #     n = tuple([j.numpy() for j in i])
    #     # data.append(n)
    #     break
    data = [i.numpy() for i in next(iter(train_loader))]
    data, label = data
    # print(type(label[0]))
    seq_data = sequence.create_dataset(data=data, label=label, save='Saved/dataset')
    # print(seq_data.shape)
    # print(seq[50:55])
    # fig = plot(seq_data[50:55])
    # plt.show()