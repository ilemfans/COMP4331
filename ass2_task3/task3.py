# -*- coding: utf-8 -*-

from sklearn.neural_network import MLPClassifier

from sklearn.tree import DecisionTreeClassifier
import scipy.io
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


# SVM classifier
def mlp_classifier(train_x, train_y):
    #We can set the number of layers and the sizes here
    #The possible choices are listed below
    clf = MLPClassifier(hidden_layer_sizes=(50, 20))
    clf.fit(train_x, train_y)
    return clf

#clf = MLPClassifier(hidden_layer_sizes=(50))
#clf = MLPClassifier(hidden_layer_sizes=(100))
#clf = MLPClassifier(hidden_layer_sizes=(100,10))
#clf = MLPClassifier(hidden_layer_sizes=(50,20))

if __name__ == '__main__':
    # we test the time used
    import time

    start = time.time()

    # read in and predict
    train_set, train_lable, test_set, test_lable = data_input()
    clf = mlp_classifier(train_set, train_lable)
    predict_result = clf.predict(test_set)

    # calculate the different scores
    precision = precision_score(test_lable, predict_result, average='weighted')
    accuracy = accuracy_score(test_lable, predict_result)
    f1_score = f1_score(test_lable, predict_result, average='weighted')
    recall = recall_score(test_lable, predict_result, average='weighted')

    # print out the answer
    print(precision, accuracy, f1_score, recall)
    elapsed = (time.time() - start)
    print(elapsed)