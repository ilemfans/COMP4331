# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 22:12:48 2016
@author: dsm
"""

from pymining import itemmining, assocrules


class freq_mining(object):
    """docstring for ClassName"""

    def __init__(self, transactions, min_sup, min_conf):
        self.transactions = transactions  # database
        self.min_sup = min_sup  # minimum support
        self.min_conf = min_conf  # minimum support

    def freq_items(self):
        relim_input = itemmining.get_relim_input(self.transactions)
        item_sets = itemmining.relim(relim_input, self.min_sup)
        return item_sets

    def association_rules(self):
        item_sets = self.freq_items()
        rules = assocrules.mine_assoc_rules(item_sets, self.min_sup, self.min_conf)
        return rules


def main(transactions, min_sup, min_conf):
    item_mining = freq_mining(transactions, min_sup, min_conf)
    freq_items = item_mining.freq_items()
    rules = item_mining.association_rules()

    return freq_items

def load_data_set():
    """
    Load a sample dataset from a txt file
    Returns:
        A data set: A list of transactions. Each transaction contains several items.
    """
    file = open("testing.txt").readlines()
    data = []
    maxLength = 0  # maxsize of transaction
    for i in range(len(file)):
        data.append([int(s) for s in file[i].split() if s.isdigit()])
        if len(data[i]) > maxLength:
            maxLength = len(data[i])
    return data
# print rules

if __name__ == "__main__":
    min_sup = 2
    min_conf = 0.5

    import time  # calculate the running time of the project

    beginning = time.time()
    transactions = load_data_set()  # load datasets and store them into an array
    #print(transactions)
    print (time.time() - beginning)
    fo = open("result.txt", "w")  # open a file to write the final report
    print(time.time() - beginning)

    min_sup = 2  # set the minimum support
    freqItems = main(transactions, min_sup,min_conf)  # find out the final output
    fre_i = freqItems.keys()  # store the keys of the the output
    # write them into a file
    print(freqItems)
    for Lk in fre_i:
        for i in range(len(Lk)):
            fo.write(str(list(Lk)[i]))
            fo.write(" ")
        fo.write(":")
        fo.write(str(freqItems[Lk]))
        #print(type(freqItems[Lk]))
        fo.write("\n")
    print(time.time() - beginning)
