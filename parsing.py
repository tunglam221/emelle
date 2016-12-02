import state_num_dictionary
from copy import deepcopy

class Sentence: 

    def __init__(self, observation, state):
        # raw observation
        self.raw_observation = observation
        # observations, array of words
        self.observation = []
        # state, array of strings
        self.state = state
        # dictionary {'San Francisco':'positive', ...} 
        # <entity>:<state>
        # not converted to numbers
        self.raw_entity = None
        # cleaned keys in self.entity
        self.entity = {}
        # bool
        self.isLabelled = False
        # dictionary {(i,j):count, ...}
        self.count_transition = None 
        # dictionary {('Pandora',3):count, ...}
        self.count_emission = None

    def clean_word(self, s):
        ret = s.lower()
        for c in ret:
            if (c in '@#') & (len(s) != 1):
                ret = ret.replace(c,'')
        return ret

    def clean(self):
        # change upper case to lower case
        # remove special characters
        # ATTENTION: called in parseDate() already
        for word in self.raw_observation:
            clean_word = self.clean_word(word)
            self.observation.append(clean_word)
        for key in self.raw_entity:
            self.entity[self.clean_word(key)] = self.raw_entity[key]

    def count(self):
        # only works for labelled data
        if self.state:
            self.isLabelled = True
            observation = self.observation
            state = self.state
            dic = state_num_dictionary.state2num
            state_num = []
            for lab in state:
                state_num.append(dic[lab])
            ctrans = {}
            ctrans[(0, state_num[0])] = 1
            cemiss = {}
            for it in range(1,len(state)-1):
                tup = (state_num[it],state_num[it+1])
                if tup in ctrans:
                    ctrans[tup] += 1
                else:
                    ctrans[tup] = 1
            ctrans[(state_num[len(state_num)-1],8)] = 1
            for it in range(1,len(state)):
                etup = (observation[it],state_num[it])
                if etup in cemiss:
                    cemiss[etup] += 1
                else:
                    cemiss[etup] = 1
            self.count_transition = ctrans
            self.count_emission = cemiss

def parseData(inputFile):

    # Input: the name of a file
    # Output: a list of Sentences, with finished counting (if labelled) 
    #         a list of Sentences without observation and empty state (if unlabelled)

    fin = open(inputFile, encoding="utf8")
    vecSentence = []
    checkLabel = fin.readline().strip().split();
    if len(checkLabel) == 1:
        isLabelled = False
    else: isLabelled = True
    if isLabelled:
        obs = [checkLabel[0]];
        lab = [checkLabel[1]];
        entity = {};
        entity_name = '';
        entity_state = '';
        for line in fin:
            parsed = line.strip().split(); 
            if parsed:
                obs.append(parsed[0])
                lab.append(parsed[1])
                if parsed[1][0] == 'B':
                    entity_name = parsed[0]
                    entity_state = parsed[1][2:]
                if (bool(entity_name) & (parsed[1][0] == 'I')):
                    entity_name = entity_name + ' ' + parsed[0]
                if (bool(entity_name) & (parsed[1][0] == 'O')):
                    entity[entity_name] = entity_state
                    entity_name = ''
                    entity_state = ''
            else: 
                sen = Sentence(obs, lab)
                if bool(entity_name) :
                    entity[entity_name] = entity_state
                    entity_name = ''
                    entity_state = ''
                sen.raw_entity = entity
                sen.clean()
                sen.count()
                entity = {}
                obs = []
                lab = []
                vecSentence.append(sen)
    else:
        obs = [checkLabel[0]];
        for line in fin:
            word = line.strip().split()
            if word:
                obs.append(word[0])
            else:
                sen = Sentence(obs,[])
                sen.clean()
                obs = []
                vecSentence.append(sen)
    return vecSentence
