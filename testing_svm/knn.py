# -*- coding: utf-8 -*-


from sklearn.tree import DecisionTreeClassifier
import scipy.io
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score

def data_input():
    data = scipy.io.loadmat('train_images.mat')
    train_set = data['train_images']
    # trainSet is a list(10000) of images; each image is a list(784) of int
    data = scipy.io.loadmat('train_labels.mat')
    train_lab = data['train_labels'][0]
    # similarly, trainLab is list of labels of images.
    data = scipy.io.loadmat('test_images.mat')
    test_set = data['test_images']
    # testSet is a list(1000) of images; each image is a list(784) of int
    data = scipy.io.loadmat('test_labels.mat')
    test_lab = data['test_labels'][0]
    # similarly, testLab is a list of labels of images.
    return train_set, train_lab, test_set, test_lab

# decision tree induction
def KNN(X,y,k):

    neigh = KNeighborsClassifier(n_neighbors=k)
    neigh.fit(X, y)

    return neigh


if __name__ == "__main__":
    train_set, train_lable,test_set,test_lable=data_input()
    clf =dtree_classifer(train_set, train_lable)
    predict_result=clf.predict(test_set)
    precision= precision_score(test_lable, predict_result, average='weighted')
    accuracy=accuracy_score(test_lable, predict_result)
    f1_score=f1_score(test_lable, predict_result, average='weighted')
    recall=recall_score(test_lable, predict_result, average='weighted')
    print(precision,accuracy,f1_score,recall)

    #print (clf.predict(dtree_test_X))