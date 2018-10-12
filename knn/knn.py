# -*- coding: utf-8 -*-

import scipy.io
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score

#import the data we need to use
def data_input():
    data = scipy.io.loadmat('train_images.mat')
    train_set = data['train_images']
    # a training set of 10,000 examples,Each example is a 28x28 grayscale image
    data = scipy.io.loadmat('train_labels.mat')
    train_lable = data['train_labels'][0]
    #a training set associated with a label from 10 classes.
    data = scipy.io.loadmat('test_images.mat')
    test_set = data['test_images']
    # testSet of 1000 examples,Each example is a 28x28 grayscale image
    data = scipy.io.loadmat('test_labels.mat')
    test_lable = data['test_labels'][0]
    #  testLab is a list of labels of images.
    return train_set, train_lable, test_set, test_lable


# KNN induction
def KNN(X,y,k):

    neigh = KNeighborsClassifier(n_neighbors=k)
    neigh.fit(X, y)

    return neigh


if __name__ == "__main__":
    # we test the time used
    import time

    start = time.time()

    # read in and predict
    train_set, train_lable,test_set,test_lable=data_input()
    clf =KNN(train_set, train_lable,5)
    predict_result=clf.predict(test_set)

    # calculate the different scores
    precision= precision_score(test_lable, predict_result, average='weighted')
    accuracy=accuracy_score(test_lable, predict_result)
    f1_score=f1_score(test_lable, predict_result, average='weighted')
    recall=recall_score(test_lable, predict_result, average='weighted')

    # print out the answer
    print(precision, accuracy, f1_score, recall)
    elapsed = (time.time() - start)
    print(elapsed)

    #print (clf.predict(dtree_test_X))