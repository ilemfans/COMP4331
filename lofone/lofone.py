import math
import queue
import heapq
#import time, pandas as pd
import numpy as np

def read_datasets():

    #my_matrix = numpy.loadtxt(open("click-stream event.csv", "rb"), delimiter=",", skiprows=0)
    lines = np.loadtxt('click-stream event.csv', delimiter=',', dtype='str')
    df = lines[1:, :7].astype('float')

    return df


# Calculate the distance of each point
def getdisanceeu(data, datalen):
    # print data
    dismatrix = [[0 for i in range(datalen)] for i in range(datalen)]

    for i in range(datalen - 1):
        for j in range(i + 1, datalen):
            dis = 0
            for l in range(len(data[0])):
                # add the distances
                dis = dis + (data[i][l] - data[j][l]) * (data[i][l] - data[j][l])
            dis = math.sqrt(dis)
            dismatrix[i][j] = dis
            dismatrix[j][i] = dis
    return dismatrix

# Calculate the distance of each point
def getdisancema(data, datalen):
    # print data
    dismatrix = [[0 for i in range(datalen)] for i in range(datalen)]

    for i in range(datalen - 1):
        for j in range(i + 1, datalen):
            dis = 0
            for l in range(1,len(data[0])):
                # add the distances

                dis = dis + abs(data[i][l] - data[j][l])
            #dis = math.sqrt(dis)
            dismatrix[i][j] = dis
            dismatrix[j][i] = dis

    return dismatrix


# Calculate the K distance of each point
def getk_distance(matrix, datalen, k):
    kdis = [0 for i in range(datalen)]
    for i in range(datalen):
        pq = queue.PriorityQueue(k)
        for j in range(datalen):
            if i != j:
                if pq.full() == False:
                    pq.put(matrix[i][j] * -1)
                else:
                    kdis[i] = pq.get()
                    if matrix[i][j] * -1 > kdis[i]:
                        pq.put(matrix[i][j] * -1)
                    else:
                        pq.put(kdis[i])
        kdis[i] = pq.get() * -1
    #print( "kdis:",kdis)
    return kdis


# Calculate reachable disdance of each point
def getreach_distance(matrix, datalen, kdis):
    reachdis_matrix = [[0 for i in range(datalen)] for j in range(datalen)]
    for i in range(datalen):
        for j in range(datalen):
            if i == j:
                reachdis_matrix[i][j] = 0
            else:
                if matrix[i][j] > kdis[j]:
                    reachdis_matrix[i][j] = matrix[i][j]
                else:
                    reachdis_matrix[i][j] = kdis[j]
    # print("reachdis_matrix:"reachdis_matrix)
    return reachdis_matrix


# Calculate local reachable density of each point
def getlrd(reachdis_matrix, matrix, datalen, minpts):
    lrd = [0 for i in range(datalen)]
    for i in range(datalen):
        lrdpq = queue.PriorityQueue(minpts)
        for j in range(datalen):
            if i != j:
                if lrdpq.full() == False:
                    lrdpq.put([matrix[i][j] * -1, j])
                else:
                    temp = lrdpq.get()
                    if matrix[i][j] * -1 > temp[0]:
                        lrdpq.put([matrix[i][j] * -1, j])
                    else:
                        lrdpq.put(temp)
        while not lrdpq.empty():
            temp = lrdpq.get()
            lrd[i] = lrd[i] + reachdis_matrix[i][temp[1]]
        lrd[i] = minpts / (lrd[i] )

    print("lrd:", lrd)
    return lrd


# Calculate LOF of each point
def getlof(data, k, minpts):
    datalen = len(data)
    dismatrix = getdisanceeu(data, datalen)
    kdis = getk_distance(dismatrix, datalen, k)
    reach_mat = getreach_distance(dismatrix, datalen, kdis)
    lrd = getlrd(reach_mat, dismatrix, datalen, minpts)

    lof = [0 for i in range(datalen)]
    for i in range(datalen):
        lofpq = queue.PriorityQueue(minpts)
        for j in range(datalen):
            if i != j:
                if lofpq.full() == False:
                    lofpq.put([dismatrix[i][j] * -1, j])
                else:
                    temp = lofpq.get()
                    if dismatrix[i][j] * -1 > temp[0]:
                        lofpq.put([dismatrix[i][j] * -1, j])
                    else:
                        lofpq.put(temp)
        while not lofpq.empty():
            temp = lofpq.get()
            lof[i] = lof[i] + lrd[temp[1]]
        lof[i] = (lof[i] / minpts) / lrd[i]

    print("lof:", lof)
    print(len(lof))
    result_fin = [0 for i in range(5)]
    index = [0 for i in range(5)]
    for i in range(datalen):
        for j in range(5):
            if lof[i]>=result_fin[j]:
                k=4
                while k>j:
                    result_fin[k]=result_fin[k-1]
                    index[k]=index[k-1]
                    k=k-1
                result_fin[j]=lof[i]
                index[j]=i
                break
    #print(index)
    for i in range(5):
        print(index[i],lof[index[i]])
    return lof


if __name__ == '__main__':
    K = 3
    MinPts = 3
    # test data
    #dataq=[[1,0,0],[2,0,1],[3,1,1],[4,3,0]]
    dataq = read_datasets()
    print("dataq len:", len(dataq))
    pslof = getlof(dataq, K, MinPts)