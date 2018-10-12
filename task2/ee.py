class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue  # value
        self.count = numOccur  # count
        self.nodeLink = None  #
        self.parent = parentNode  # parent node
        self.children = {}  # children node

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):  # display the output
        #print ' ' * ind, self.name, '  ', self.count
        for child in self.children.values():
            child.disp(ind + 1)


def createTree(dataSet, minSup=1):
    # count the number of each element in Itemset
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

    # delete the those infrequent items whose supports are 1, and apply apriori
    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del (headerTable[k])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0: return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]

    # construct the root node of fp-tree
    retTree = treeNode('Null Set', 1, None)

    # acquire frequent itemsets (k=1) and update the tree
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            # sort items by frequency
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    # if a node appears, increase the count of this node
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        # else build new nodes
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # create if this node does not appear in terms of headerTable
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


# update the header link
def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# create a dataset for test
def loadSimpDat():
    # open a txt file to find all the datasets inside and send them into a 2D array data
    file = open("COMP4331.txt").readlines()
    data = []
    maxLength = 0  # maxsize of transaction
    for i in range(len(file)):
        data.append([int(s) for s in file[i].split() if s.isdigit()])
        if len(data[i]) > maxLength:
            maxLength = len(data[i])
    return data


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


# leafNode
def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases, minSup)
        if myHead != None:
            #print 'conditional tree for: ', newFreqSet
            myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


if __name__ == "__main__":
    simpDat = loadSimpDat()
    #print simpDat
    initSet = createInitSet(simpDat)
    #print initSet
    myFPtree, myHeaderTab = createTree(initSet, 100)
    myFPtree.disp()
    #print findPrefixPath('t', myHeaderTab['t'][1])
    freqItems = []
    fo = open("result1.txt", "w")
    mineTree(myFPtree, myHeaderTab, 100, set([]), freqItems)
    for Lk in freqItems:
    #    for freq_set in Lk:
        for i in range(len(Lk)):
            fo.write(str(list(Lk)[i]))
            fo.write(" ")
        fo.write("\n")
    #print freqItems