from parsing import *
from learning import *
from viterbi import *
from modified_viterbi import *
from state_num_dictionary import *

enTrainFile = 'EN/train'
enTestFile = 'EN/dev.in'
fout = 'EN/dev.p2.out'
print('======= Test Output =======', file = open(fout,'w'))

train_sentences = parseData(enTrainFile)
test_sentences = parseData(enTestFile)

params = Counting(train_sentences)

tranParams = params.transPara()
emisParams = params.emissPara()

for sentence in test_sentences:
  vit = Viterbi(tranParams, emisParams)
  for word in sentence:
    print('{} {}'.(word,num2state[])


