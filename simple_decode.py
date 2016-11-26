# Using only emission parameter to predict

from state_num_dictionary import *

class SimpleDecode:
  def __init__(self, tran, emis):
    self.tran = tran
    self.emis = emis
    self.number_of_states = len(tran)

  def simple_decode(self, sentence):
    words = sentence.observation
    path = []
    for word in words:
      emission = [0]
      if word not in self.emis:
        for i in range(1, self.number_of_states-1):
          emission.append(self.emis[i])
      else:
        emission = self.emis[word]
      path.append(emission.index(max(emission)))
    for p in path:
      sentence.state.append(num2state[p])
