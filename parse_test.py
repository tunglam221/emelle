from parsing import * 

fin = 'EN/train' 
fout = 'parse_test.out'

sens = parseData(fin) 

print('', end = '', file = open(fout,'w'))

for sen in sens:
    for word in sen.observation:
        print(word,file = open(fout,'a'))
    print(file = open(fout,'a'))
