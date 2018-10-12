#-*-coding:utf-8-*-
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        #set default value for class treecode
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        #define a function to count the times a number appears
        self.count += numOccur

    def disp(self, ind=1):
        #print ' ' * ind, self.name, ' ', self.count
        #display the output
        for child in self.children.values():
            child.disp(ind + 1)

def createTree(dataSet, minSup=1):
    #create a  FP-tree
    #the first time to search through datasets and create a headerTable
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    #remove those itemsets that are smaller than minsup
    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del(headerTable[k])
    freqItemSet = set(headerTable.keys())
    #return none if it is an empty set
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None) # root node
    #the second time to search through the dataset to create a FP tree
    for tranSet, count in dataSet.items():
        #for each tranSet, store the frequecy of each element, we will sort them later
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)] # sorting
            updateTree(orderedItems, retTree, headerTable, count) # update the FP tree
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        #add one if this item appears
        inTree.children[items[0]].inc(count)
    else:
        #create a new node if this item does not happen
        inTree.children[items[0]] = treeNode(items[0], count, inTree)

        #update this head-pointer table or point the former one to a new item
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])

    if len(items) > 1:
        #do updateTree to those elements left behind
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

def findPrefixPath(basePat, treeNode):
    ''' 创建前缀路径 '''
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)

        if myHead != None:
            # 用于测试
            #print 'conditional tree for:', newFreqSet
            myCondTree.disp()

            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

def fpGrowth(dataSet, minSup=100):
    #the main function to combine the things above together
    initSet = createInitSet(dataSet)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    freqItems = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItems)
    return freqItems

def loadSimpDat():
    #open a txt file to find all the datasets inside and send them into a 2D array data
    file = open("COMP4331.txt").readlines()
    data = []
    maxLength = 0  # maxsize of transaction
    for i in range(len(file)):
        data.append([int(s) for s in file[i].split() if s.isdigit()])
        if len(data[i]) > maxLength:
            maxLength = len(data[i])
    return data



if __name__ == "__main__":
    """
    Test
    """
    import time
    beginning = time.time()
    dataSet = loadSimpDat()
    print(time.time() - beginning)
    fo = open("result.txt", "w")
    freqItems = fpGrowth(dataSet)
    print(time.time() - beginning)
    for Lk in freqItems:
        for i in range(len(Lk)):
            fo.write(str(list(Lk)[i]))
            if (i != len(Lk) - 1):
                fo.write(",")
        fo.write("\n")
    print(time.time() - beginning)
    #print(freqItems)