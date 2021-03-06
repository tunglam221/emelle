class Counting:

    def __init__(self, sentences):
        self.sentences = sentences
    
    #Input: List of objects(sentences)
    #Output: 2D array of transition Count
    #States are as follows:    
    #START = 0, O = 1, B-VE = 2, B-neutral = 3, B+ve = 4, I-VE = 5, I-neutral = 6, I+ve = 7, STOP = 8
    
    def transCount(self):
        transPara = [x[:] for x in [[0] * 9] * 9]
        for s in self.sentences:
            for z in s.count_transition:
                transPara[z[0]][z[1]] += s.count_transition.get(z)
                
        return transPara
                

    #Input: List of object(sentences)
    #Output: Dictionary of Emission Count, in the Form of {"obs1" : array, "obs2" : array}, where array contains counts of each state
    #States are as follows:
    #START = 0 , O = 1, B-VE = 2, B-neutral = 3, B+ve = 4, I-VE = 5, I-neutral = 6, I+ve = 7, STOP = 8
    
    def emissCount(self):
        emissionPara = {}
        for s in self.sentences:
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
    
    # Output: total state count
    def countPerState(self):
        transmission = self.transCount()
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
    def transPara(self):
        transCount = self.transCount()
        countPerState = self.countPerState()
        for i in range(0,9):
            for j in range(0,9):
                if(countPerState[i]!=0):
                    transCount[i][j] = transCount[i][j]/(countPerState[i])
        return transCount
    
    #Emission Parameters
    def emissPara(self):
        emissCount = self.emissCount()
        countPerState = self.countPerState()
        for word in emissCount:
            temp = emissCount.get(word)
            for i in range(0,9):
                temp[i] = temp[i]/(countPerState[i]+1)
            emissCount[word] = temp
            
        # Parameter for potential unseen data
        for i in range(0,9):
            emissCount[i] = 1/(countPerState[i] + 1)
        return emissCount


