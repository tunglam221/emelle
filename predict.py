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

vit = Viterbi(tranParams, emisParams)
for sentence in test_sentences:
  v = vit.decode(sentence)
  for i in range(len(v)):
    print('{} {}'.(sentence[i], num2state[])


