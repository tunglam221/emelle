from state_num_dictionary import *
from viterbi import *

class Perceptron:
    def __init__(self, sentences, iteration):
        self.sentences = sentences
        self.trans_count = [x[:] for x in [[0] * 9] * 9]
        self.emis_count = {}
        self.iteration = iteration

    # z is the predicted tagged sequence by Viterbi, 
    # t is the actual tagged sequence, including START and STOP
    def update_params(self, sentence, z, t):
        for i in range(1, len(z)):
            self.trans_count[z[i-1]][z[i]]-=1
            self.trans_count[t[i-1]][t[i]]+=1
        for i in range(len(sentence)):
            if sentence[i] not in self.emis_count:
                self.emis_count[sentence[i]] = [0]*9
            self.emis_count[sentence[i]][z[i+1]]-=1
            self.emis_count[sentence[i]][t[i+1]]+=1

    def train(self):
        for i in range(self.iteration):
            for sentence in self.sentences:
                actual_tag = [0]
                predicted_tag = Viterbi(self.trans_count, self.emis_count).decode(sentence)
                for tag in sentence.state:
                    actual_tag.append(state2num[tag])
                actual_tag.append(8)
                self.update_params(sentence.observation, predicted_tag, actual_tag)
            # print("---One more iternation---")
            # print(predicted_tag)
            # print(actual_tag)
            # print(self.trans_count)
            # print(self.emis_count)

        x = (i+1)*len(self.sentences)
        for l in self.trans_count:
            for j in range(len(l)):
                l[j]=l[j]/float(x)
        for key in self.emis_count:
            for j in range(len(self.emis_count[key])):
                self.emis_count[key][j]=self.emis_count[key][j]/float(x)