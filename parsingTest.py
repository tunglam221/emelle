from parsing import *

fname = 'EN/dev.in'
fout = 'parsingTest.out'
print('======= Test Output =======', file = open(fout,'w'))

aha = parseData(fname)
for sen in aha:
    obs = ''
    for word in sen.observation:
        obs = obs + ' ' + word
    state = ' '
    for lab in sen.state:
        state = state + ' ' + lab
    print('OBS:    ',obs, file = open(fout, 'a'))
    print('STATE:  ',state, file = open(fout, 'a'))
    print('ENTITY: ',sen.entity, file = open(fout, 'a'))
    print('TC:     ',sen.count_transition, file = open(fout,'a'))
    print('EC:     ',sen.count_emission, '\n', file = open(fout,'a'))
