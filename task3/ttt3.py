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

if __name__ == "__main__":
    import time#calculate the running time of the project
    beginning = time.time()
    transactions = load_data_set()#load datasets and store them into an array
    print (time.time() - beginning)
    fo = open("result.txt", "w")#open a file to write the final report
    print(time.time() - beginning)

    min_sup = 100#set the minimum support
    freqItems=main(transactions, min_sup)#find out the final output
    fre_i=freqItems.keys()#store the keys of the the output
    #write them into a file
    #print(freqItems)
    for Lk in fre_i:
        for i in range(len(Lk)):
            fo.write(str(list(Lk)[i]))
            if(i!=len(Lk)-1):
                fo.write(",")
        fo.write("\n")
    print(time.time() - beginning)

