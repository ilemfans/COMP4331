
# -*- coding: utf-8 -*-
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

#set debug mode to be true
DEBUG = True


#the funtion we use to get the data from GMM-Points.mat and change it into an array
def data_input():
    import scipy.io
    data = scipy.io.loadmat('GMM-Points.mat')
    train_set = data['Points']
    return train_set


#Gaussian distribution pdf of the kth model
# return a list
def phi(Y, mu_k, cov_k):
    norm = multivariate_normal(mean=mu_k, cov=cov_k)
    return norm.pdf(Y)


# Expectation Step:calculate
# Y is the 2D array of the sample
# mu is a multi-dimension array of means
# cov is the array of COV matrix
def getExpectation(Y, mu, cov, alpha):
    # number of samples
    N = Y.shape[0]
    # number of models
    K = alpha.shape[0]


    # We ask N and K biggger than 1 to avoid using one single sample
    assert N > 1, "There must be more than one sample!"
    assert K > 1, "There must be more than one gaussian model!"

    gamma = np.mat(np.zeros((N, K)))

    # calculate corresponding possibilities
    prob = np.zeros((N, K))
    for k in range(K):
        prob[:, k] = phi(Y, mu[k], cov[k])
    prob = np.mat(prob)

    # calculate the gamma of each sample
    for k in range(K):
        gamma[:, k] = alpha[k] * prob[:, k]
    for i in range(N):
        gamma[i, :] /= np.sum(gamma[i, :])
    return gamma

# M step: Given the cluster assignment, foreach cluster, the algorithm adjusts the center so that the sum of
#distance from the objects assigned to this cluster and the new center is minimized
# Y is the 2D array of the sample
def maximize(Y, gamma):
    # N is number of samples
    N, D = Y.shape
    # NUMBER OF MODELS
    K = gamma.shape[1]

    #initializing parameters
    mu = np.zeros((K, D))
    cov = []
    alpha = np.zeros(K)

    # calculate the parameters
    for k in range(K):
        Nk = np.sum(gamma[:, k])
        # calculate the mean
        for d in range(D):
            mu[k, d] = np.sum(np.multiply(gamma[:, k], Y[:, d])) / Nk

        cov_k = np.mat(np.zeros((D, D)))
        for i in range(N):
            cov_k += gamma[i, k] * (Y[i] - mu[k]).T * (Y[i] - mu[k]) / Nk
        cov.append(cov_k)

        alpha[k] = Nk / N
    cov = np.array(cov)
    return mu, cov, alpha


# scale each data to be from 0 to 1
def scale_data(Y):
    # 对每一维特征分别进行缩放
    for i in range(Y.shape[1]):
        max_ = Y[:, i].max()
        min_ = Y[:, i].min()
        Y[:, i] = (Y[:, i] - min_) / (max_ - min_)
    return Y


# Initializing parameters
def init_params(shape, K):
    N, D = shape
    mu = np.random.rand(K, D)
    cov = np.array([np.eye(D)] * K)
    alpha = np.array([1.0 / K] * K)
    return mu, cov, alpha



# THE EM-GMM
# times number of times to iteration
def GMM_EM(Y, K, times):
    Y = scale_data(Y)
    mu, cov, alpha = init_params(Y.shape, K)
    for i in range(times):
        gamma = getExpectation(Y, mu, cov, alpha)
        mu, cov, alpha = maximize(Y, gamma)
    return mu, cov, alpha



# input the data
Y = data_input()
using_list=zeros((400,2))
for i in range(400):
    using_list[i][0]=Y[i][0]
    using_list[i][1] = Y[i][1]
matY = np.matrix(using_list, copy=True)

# number of clusters K
K = 2

#calculate the coefficient of gmm model
mu, cov, alpha = GMM_EM(matY, K, 100)



# use getException to calculate the gamma
gamma = getExpectation(matY, mu, cov, alpha)
# calculate the corresponding lable of each sample
category = gamma.argmax(axis=1).flatten().tolist()[0]


# put every sample into the corresponding class
class1 = np.array([using_list[i] for i in range(400) if category[i] == 0])
class2 = np.array([using_list[i] for i in range(400) if category[i] == 1])

#the comparation part: below is what the lable shows
#class1 = np.array([Y[i] for i in range(N) if Y[i][2] == 0])
#class2 = np.array([Y[i] for i in range(N) if Y[i][2] == 1])

# draw the final result
plt.plot(class1[:, 0], class1[:, 1], 'rs', label="class1")
plt.plot(class2[:, 0], class2[:, 1], 'bo', label="class2")
plt.legend(loc="best")
plt.title("GMM Clustering By EM Algorithm")
plt.show()