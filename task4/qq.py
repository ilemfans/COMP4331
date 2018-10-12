# -*- coding: utf-8 -*-


from pymining import itemmining, assocrules


class freq_mining(object):
    """docstring for ClassName"""

    #set default value for class freq_mining
    def __init__(self, transactions, min_sup):
        self.transactions = transactions  # transaction is the
        self.min_sup = min_sup  # minimum support we given

    def freq_items(self):
        #Give this function a list of transactions and a key function, returns a data
        #structure used as the input of the relim algorithm.
        relim_input = itemmining.get_relim_input(self.transactions)
        #use the input from get_relim_input() and minimum support
        #to return frequent item sets of items appearing in a list of transactions
        #based on Recursive Elimination
        item_sets = itemmining.relim(relim_input, self.min_sup)
        return item_sets



def main(transactions, min_sup):
    """
        main function to find the actual
        Returns:
            A dictionary stores all the frequent itemsets and the support
    """
    item_mining = freq_mining(transactions, min_sup)
    freq_items = item_mining.freq_items()

    return freq_items


def load_data_set():
    """
    Load a sample dataset from a txt file
    Returns:
        A data set: A list of transactions. Each transaction contains several items.
    """
    file = open("COMP4331.txt").readlines()
    data = []
    maxLength = 0  # maxsize of transaction
    for i in range(len(file)):
        data.append([int(s) for s in file[i].split() if s.isdigit()])
        if len(data[i]) > maxLength:
            maxLength = len(data[i])
    return data

def deciding_max_closed(freqItems):
    """
        Input the dictionary we get from main func
        we find itemsets whose items are totally contained in another and thei support is not the same
        according to the defination of closed itemsets
        Then find those who does not have a immediate supersets
        Returns:
            Two lists containing closed frequent itemsets and maximum frequent itemsets
    """
    closed_fi = []
    max_fi = []
    the_keys = freqItems.keys()
    for Lk in the_keys:
        check = 1#check=0不能进closed
        count = 0#count=1不能进max
        for CheckLk in the_keys:
            d = [False for c in Lk if c not in CheckLk]
            if (not d):
                if (len(CheckLk) != len(Lk)):
                    count = 1
                    if (freqItems[Lk] == freqItems[CheckLk]):
                        check = 0
        if (check):
            closed_fi.append(Lk)
        if (not count):
            max_fi.append(Lk)
            if(not check):
                closed_fi.append(Lk)


    return closed_fi, max_fi


if __name__ == "__main__":
    import time
    beginning = time.time()
    transactions = load_data_set()
    print (time.time() - beginning)

    #open three files to write in the final result
    cfi = open("cal_cfi.txt", "w")
    mfi = open("cal_mfi.txt", "w")
    print(time.time() - beginning)

    min_sup = 100#the minimum support
    freqItems=main(transactions, min_sup)#calculate the frequent itemsets and their result
    #print(freqItems)
    print(time.time() - beginning)

    closed_fi,max_fi=deciding_max_closed(freqItems)
    outputu = freqItems.keys()


    #write the result in files
    for Lk in closed_fi:
        for i in range(len(Lk)):
            cfi.write(str(list(Lk)[i]))
            if (i != len(Lk) - 1):
                cfi.write(",")
        cfi.write("\n")

    for Lk in max_fi:
        for i in range(len(Lk)):
            mfi.write(str(list(Lk)[i]))
            if (i != len(Lk) - 1):
                mfi.write(",")
        mfi.write("\n")
    print(time.time() - beginning)

