# -*- coding: utf-8 -*-


# KNN classifier
def random_forest_classifier(train_x, train_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=8)
    model.fit(train_x, train_y)
    return model


if __name__ == '__main__':


    rf_train_X = [[1, 1, 1, 0],
         [1, 1, 1, 1],
         [2, 1, 1, 0],
         [3, 2, 1, 0],
         [3, 3, 2, 0],
         [3, 3, 2, 1],
         [2, 3, 2, 1]]

    rf_train_y = [0,0,1,1,1,0,1]

    rf_test_X = [[3,2,1,1]]

    rf_k = 3

    rf_classifier = random_forest_classifier(rf_train_X,rf_train_y)

    print(rf_classifier.predict(rf_test_X))