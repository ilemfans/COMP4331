# -*- coding: utf-8 -*-

import scipy.io
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

UNCLASSIFIED = False
NOISE = 0


#import the data we need to use
def data_input():
    data = scipy.io.loadmat('DBSCAN-Points.mat')
    train_set = data['Points']
    #print (type(data))
    #print (data)
    return train_set



def main():
    # Compute DBSCAN
    X=data_input()
    db = DBSCAN(eps=0.12, min_samples=12).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    import matplotlib.pyplot as plt

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=8)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=4)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()

if __name__ == '__main__':
    import time
    start = time.clock()
    main()
    end = time.clock()
    print('finish all in %s' % str(end - start))