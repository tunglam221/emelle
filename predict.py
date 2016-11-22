from parsing import *
from learning import *
from viterbi import *
from modified_viterbi import *
from state_num_dictionary import *

enFile = 'EN/dev.out'
sentences = parseData(enFile)
params = Counting(sentences)

tranParams = params.transPara()
emisParams = params.emissPara()

vit = ModifiedViterbi(tranParams, emisParams)
for result in vit.decode("Starbucks is my favorite brand of coffee", 3):
  print('========================')
  for i in result:
    print(num2state[i])

