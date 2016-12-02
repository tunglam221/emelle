from parsing import * 

fin = 'EN/train' 
fout = 'parse_test.out'

sens = parseData(fin) 

print('', end = '', file = open(fout,'w'))

for sen in sens:
    obs = ''
    for word in sen.observation:
        obs = obs + ' ' + word
    print(obs, file = open(fout,'a'))
    print(sen.entity, file = open(fout,'a'))
    print('', file = open(fout, 'a'))
