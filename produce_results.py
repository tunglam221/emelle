from state_num_dictionary import *
from parsing import * 
from learning import *
from simple_decode import * 
from viterbi import *
from modified_viterbi import * 
from copy import deepcopy

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
        print('', file = open(fout,'a'))



for lang in ['EN','ES','SG','CN']:
    fname_learn = lang + '/train'
    fname_pre = lang + '/dev.in'

    # parse the labelled data
    sentences_labelled = parseData(fname_learn) 

    # learn the parameters
    learn = Counting(sentences_labelled) 
    trans_par = learn.transPara() 
    emiss_par = learn.emissPara()
    print(emiss_par['New'])

    # parse the data to be predicted
    sentences_raw = parseData(fname_pre)

    # part 2
    fout = lang + '/dev.p2.out'
    sentences_process = deepcopy(sentences_raw)
    algo_part2 = SimpleDecode(trans_par, emiss_par) 
    for sen in sentences_process:
        algo_part2.simple_decode(sen)
    printPrediction(sentences_process, fout, 0)

    # part 3
    fout = lang + '/dev.p3.out'
    sentences_process = deepcopy(sentences_raw)
    algo_part3 = Viterbi(trans_par, emiss_par) 
    for sen in sentences_process:
        algo_part3.decode(sen) 
    printPrediction(sentences_process, fout, 0)

    if (lang == 'EN' or lang == 'ES'): 
        # part 4 
        fout = lang + '/dev.p4.out' 
        sentences_process = deepcopy(sentence_raw) 
        algo_part3 = ModifiedViterbi(trans_par, emiss_par) 
        for sen in sentences_process:
            algo_part3.decode(sen, 5)
        printPrediction(sentences_process, fout, 5)
