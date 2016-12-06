from state_num_dictionary import *
from parsing import * 
from perceptron import *
from viterbi import *
from copy import deepcopy
from evalResult import *

def printPrediction(sentences, fout, k):
    # input: an array of labelled sentences 
    # input: output file name
    # input: which prediction,
    #       0: only one prediction 
    #       k (k>0): the k-th best
    print('', end = "", file = open(fout,'w')) 
    for sen in sentences:
        if (k == 0): 
            state = sen.state
        else:
            state = sen.state[k-1]
        observation = sen.observation

        for it in range(0,len(state)):
            print(observation[it],state[it], file = open(fout,'a',encoding='UTF-8'))
        print('', file = open(fout,'a'))

def printEvaluation(fpre, fgold, fout):
    # input:
    #       fpre, prediction file name
    #       fgold, golden standard file name
    #       fout, output file name
    gold = open(fgold, 'r', encoding='UTF-8')
    prediction = open(fpre, 'r', encoding='UTF-8')

    observed = get_observed(gold)
    predicted = get_predicted(prediction)

    print('----- Gold:',fgold,'|| Prediction:',fpre,'-----', file=open(fout,'a'))

    compare_observed_to_predicted(observed, predicted, fout)

    print('', file = open(fout,'a'))

# ======= main function =======

fname_eval = 'results.out'
print('', end = '', file = open(fname_eval,'w'))

for lang in ['EN', 'ES']:
    fname_learn = lang + '/train'
    fname_pre = lang + '/dev.in'
    fname_gold = lang + '/dev.out'

    print('=====================', file=open(fname_eval,'a'))
    print('==== Language:',lang,file=open(fname_eval,'a'))
    print('=====================\n',file=open(fname_eval,'a'))

    # parse the labelled data
    sentences_labelled = parseData(fname_learn) 

    # parse the data to be predicted
    sentences_raw = parseData(fname_pre)

    fout = lang + '/dev.p3.out'
    sentences_process = deepcopy(sentences_raw)
    perceptron = Perceptron(sentences_labelled, 10)
    perceptron.train()
    algo_part3 = Viterbi(perceptron.trans_count, perceptron.emis_count) 
    for sen in sentences_process:
        state = algo_part3.decode(sen) 
        for i in range(1, len(state)-1):
            sen.state.append(num2state[state[i]])
    printPrediction(sentences_process, fout, 0)
    printEvaluation(fout, fname_gold, fname_eval)

