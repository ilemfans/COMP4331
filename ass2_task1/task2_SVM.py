# -*- coding: utf-8 -*-

from sklearn.neighbors import KNeighborsClassifier

# SVM classifier
def svm_classifier(train_x, train_y):
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    model.fit(train_x, train_y)
    return model


if __name__ == '__main__':


    svm_train_X = [[1, 1, 1, 0],
         [1, 1, 1, 1],
         [2, 1, 1, 0],
         [3, 2, 1, 0],
         [3, 3, 2, 0],
         [3, 3, 2, 1],
         [2, 3, 2, 1]]

    svm_train_y = [0,0,1,1,1,0,1]

    svm_test_X = [[3,2,1,1]]

    svm_k = 3

    svm_classifier = svm_classifier(svm_train_X,svm_train_y)

    print(svm_classifier.predict(svm_test_X))