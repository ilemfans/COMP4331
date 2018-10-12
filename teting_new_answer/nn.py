#-*-coding:utf-8-*-

#the start of preparing
#load datasets
def loadDataSet():
    file = open("COMP4331.txt").readlines()
    data = []
    maxLength = 0  # maxsize of transaction
    for i in range(len(file)):
        data.append([int(s) for s in file[i].split() if s.isdigit()])
        if len(data[i]) > maxLength:
            maxLength = len(data[i])
    return data

def createC1(dataSet):
    C1 = []   #C1 contains 1-item itemsets
    for transaction in dataSet:  #search every transaction in datasets
        for item in transaction: #search every item
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    #frozen means can not be changed, match means do frozenset to every element in C1
    return map(frozenset,C1)

#Ck means datasets, D is the list, minsupport in this question is 100
#This function is used to generate L1 from C1, L1 means the minimum support of itemsets
def scanD(D,Ck,minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            #issubset：表示如果集合can中的每一元素都在tid中则返回true
            if can.issubset(tid):
                #calculate the support of rach itemset and store in dictionary ssCnt
                if not ssCnt.has_key(can):
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        #calculate the support of itemsets and consider adding it to retList
        support = ssCnt[key]
        if support >= minSupport:
            retList.insert(0, key)
        #build the dictionary
        supportData[key] = support
    return retList,supportData


#the start of apriori
#Create Ck,CaprioriGen (),input: frequent itemset Lk and number of items k
#return Ck
def aprioriGen(Lk,k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            #consider combining the two sets together
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])

    return retList

def apriori(dataSet, minSupport=100):
    C1 = createC1(dataSet)  #create C1
    D = map(set,dataSet)
    L1,supportData = scanD(D, C1, minSupport)
    L = [L1]
    #if two itemsets are length k-1, then they can combine if and only if they have the same former k-2 items
    k = 2
    while(len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk,supK = scanD(D,Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k +=1
    return L,supportData


if __name__=="__main__":
    import time

    beginning = time.time()
    dataSet = loadDataSet()
    print(time.time() - beginning)
    L,suppData = apriori(dataSet)
    i = 0
    print(time.time() - beginning)
    #print(L)
    fo = open("result.txt", "w")
    for Lk in L:
        for freq_set in Lk:
            #print (freq_set, support_data[freq_set])
            for i in range(len(freq_set)):
                fo.write(str(list(freq_set)[i]))
                fo.write(" ")
            fo.write("\n")
    print("end")