class Sentence:
    
    def __init__(self,observation,count_transition,count_emission):
        #Observations
        self.observation = observation
        #Form of Dictionary {(i,j):count, ....}
        self.count_transition = count_transition
        #Form of Dictionary {('Pandora',3):count, .....} 
        self.count_emission = count_emission
        
class Counting:
    
    #Input: List of objects(sentences)
    #Output: 2D array of transition Count
    #States are as follows:    
    #START = 0, O = 1, B-VE = 2, B-neutral = 3, B+ve = 4, I-VE = 5, I-neutral = 6, I+ve = 7, STOP = 8
    
    def transCount(los):
        transPara = [x[:] for x in [[0] * 9] * 9]
        for s in los:
            for z in s.count_transition:
                transPara[z[0]][z[1]] += s.count_transition.get(z)
                
        return transPara
                

    #Input: List of object(sentences)
    #Output: Dictionary of Emission Count, in the Form of {"obs1" : array, "obs2" : array}, where array contains counts of each state
    #States are as follows:
    #START = 0 , O = 1, B-VE = 2, B-neutral = 3, B+ve = 4, I-VE = 5, I-neutral = 6, I+ve = 7, STOP = 8
    
    def emissCount(los):
        emissionPara = {}
        for s in los:
            for word in s.count_emission:
                if word[0] in emissionPara:
                    temp = emissionPara.get(word[0])
                    temp[word[1]] += s.count_emission.get(word)
                    emissionPara[word[0]] = temp
                    
                else:
                    array = [0] * 9
                    array[word[1]] = s.count_emission.get(word)
                    emissionPara[word[0]] = array
                
        return emissionPara
    
    def countPerState(transmission):
        result = [0] * 9
        count = 0
        for i in transmission:
            total = 0
            for j in i:
                total += j
            result[count] = total
            count += 1
        return result
    
    #Transmission Parameters    
    def transPara(transCount,countPerState):
        for i in range(0,9):
            for j in range(0,9):
                if(countPerState[i]!=0):
                    transCount[i][j] = transCount[i][j]/(countPerState[i])
        return transCount
    
    #Emission Parameters
    def emissPara(emissCount,countPerState):
        for word in emissCount:
            temp = emissCount.get(word)
            for i in range(0,9):
                temp[i] = temp[i]/(countPerState[i]+1)
            emissCount[word] = temp
            
        for i in range(0,9):
            emissCount[i] = 1/(countPerState[i] + 1)
        return emissCount
        
            
#Testing
listofSentences = []      
count_transition = {(1,2): 5,(2,3): 6 }
count_emission =  {('Pandora',3):1 , ('Pandora',6):7 ,('Lam',7):1, ('Nata',1):5} 
count_transition1 = {(7,8): 8,(4,5): 2, (6,7):2 , (1,2):5}
count_emission1 =  {('Stanley',7):1 , ('Anker',3):7 ,('Lam',7):1, ('Nata',1):5, ('Pandora',6):7} 
listofSentences.append(Sentence(["a","b"],count_transition,count_emission))
listofSentences.append(Sentence(["a","b"],count_transition1,count_emission1))
print("Tramission Count :")
z = Counting.transCount(listofSentences)
print(z)
print("Emission Count :")
x = Counting.emissCount(listofSentences)
print(x)
print("Count Per State :")
c = Counting.countPerState(z)
print(c)
print("Tramission Parameter :")
print(Counting.transPara(z,c))
print("Emission Parameter :")
print(Counting.emissPara(x,c))



