import math
import queue
import heapq
#import time, pandas as pd
import numpy as np




def read_datasets():
    #read in the pause videos and play videos
    lines = np.loadtxt('click-stream event.csv', delimiter=',', dtype='str')
    df = lines[1:, :7].astype('float')
    for i in range(695):
        pause_video[i]=df[i][2]
        play_video[i]=df[i][3]
    return df


def getdisanceeu(using_number,cellb,pta,ptb):
    # print data
    #calculate the distance in the final step
    dis = 0
    xcora=store_points[using_number][pta][0]
    ycora = store_points[using_number][pta][1]
    xcorb = store_points[cellb][ptb][0]
    ycorb = store_points[cellb][ptb][1]
    dis = dis + (xcora - xcorb) * (xcora - xcorb)

    dis = dis + (ycorb - ycora) * (ycorb - ycora)
    dis = math.sqrt(dis)
    return dis

#let's set D to be 2*1.414
def step_two():
    #the step 2 of the algorithm
    for i in range(int(total_cells)):
        this_array=getdisancema(pause_video,play_video,(i%cell_per_length)*length+length/2,(i//cell_per_length)*length+length/2)
        icount=0
        for j in range(len(this_array)):
            if(this_array[j]==1):
                icount=icount+1
                assignments_count[i]=assignments_count[i]+1
                store_points[i].append([pause_video[j],play_video[j]])
        if icount>thresh:
            count[i]=1

def step_three():
    #the step 3 of the algorithm to add L1
    for i in range(int(total_cells)):
        if(count[i]==1):
            #print(i,count[2])

            if((count[i-1]!=1)&(i%cell_per_length!=0)):

                count[i-1]=2
            if ((count[i + 1] != 1) & (i % cell_per_length != cell_per_length-1)):

                count[i + 1] = 2
            if ((count[i - int(cell_per_length) ] != 1) &(i//cell_per_length!=0)):

                count[i - int(cell_per_length) ] = 2
            if ((count[i + int(cell_per_length) ] != 1) &(i//cell_per_length!=cell_per_height-1)):

                count[i + int(cell_per_length) ] = 2
            if((count[i-int(cell_per_length)-1]!=1)&((i)% cell_per_length != 0)&(i//cell_per_length!=0)):

                count[i-int(cell_per_length)-1] = 2
            if ((count[i + int(cell_per_length) - 1] != 1) & (
                    (i) % int(cell_per_length) != 0)&((i)//int(cell_per_length)!=int(cell_per_length)-1)):

                count[i + int(cell_per_length) - 1] = 2
            if ((count[i + int(cell_per_length) + 1] != 1) & (
                    (i ) % cell_per_length != cell_per_length-1)&(i//cell_per_length!=cell_per_height-1)):

                count[i + int(cell_per_length) + 1] = 2
            if ((count[i - int(cell_per_length) + 1] != 1) & (
                    (i ) % cell_per_length != cell_per_length-1)&(i//cell_per_length!=0)):

                count[i - int(cell_per_length) + 1] = 2

def step_fivea():
    #step5.a and 5.b  in the algorithm
    #decide whether to lable pink
    for i in range(int(total_cells)):
        if(count[i]==0):
            qfivea_count[i]=addone(i)
            if(assignments_count[i]>thresh):
                count[i]=2
            else:
                step_fiveb(i)

def execute_cell(using_number):
    #using cell is the index of the cell we decide to operate
    #we will put all points in the index cell to be outliers
    for i in range(len(store_points[using_number])):
        outlier.append(store_points[using_number][i])

def step_fiveb(using_number):
    #decide to operate each point
    for i in range(int(total_cells)):
        if(count[i]==0):
            addthree(using_number)
            if(qfivec_count[i]<thresh):
                execute_cell(i)
            else:
                last_step(i)

def last_step(using_number):
    #put the points into outliers
    for i in range(len(store_points[using_number])):
        last_count = last_counta(using_number,i)
        if(last_count<thresh):
            outlier.append(store_points[using_number][i])

def last_counta(numberq,the_point):
    #count the distances in D around the mentioned point
    below = numberq // cell_per_length
    above = max_play - below - 1
    left = numberq % cell_per_length
    right = max_pause - left - 1
    left_move = int(max(0, left - 3))
    right_move = int(min(cell_per_length - 1, left + 3))
    down_move = int(max(0, below - 3))
    above_move = int(min(below + 3, cell_per_length - 1))
    count_in_distance_d=0
    D=length*2*(math.sqrt(2))
    for i in range(down_move, above_move):
        for j in range(left_move, right_move):
            for k in range(len(store_points[i*int(cell_per_length)+j])):

                distance=getdisanceeu(numberq,i*int(cell_per_length)+j,the_point,k)
                if(distance!=0):
                    if(distance<=D):
                        count_in_distance_d=count_in_distance_d+1
    return count_in_distance_d

def addone(numberq):
    #add those in L1 of the cell,numberq is the index of the cell
    #result=assignments_count[numberq]
    below=numberq//cell_per_length
    above=max_play-below-1
    left=numberq%cell_per_length
    right=max_pause-left-1
    left_move=int(max(0,left-1))
    right_move=int(min(cell_per_length-1,left+1))
    down_move=int(max(0,below-1))
    above_move=int(min(below+1,cell_per_length-1))
    for i in range(down_move,above_move):
        for j in range(left_move,right_move):
            qfivea_count[numberq] = qfivea_count[numberq] + assignments_count[i * int(cell_per_length) + j]

def addthree(numberq):
    #add those in L3 in the mentioned cell, numberq is the index of the cell
    #result=assignments_count[numberq]
    below=numberq//cell_per_length
    above=max_play-below-1
    left=numberq%cell_per_length
    right=max_pause-left-1
    left_move=int(max(0,left-3))
    right_move=int(min(cell_per_length-1,left+3))
    down_move=int(max(0,below-3))
    above_move=int(min(below+3,cell_per_length-1))
    for i in range(down_move,above_move):
        for j in range(left_move,right_move):
            qfivec_count[numberq]=qfivec_count[numberq]+assignments_count[i*int(cell_per_length)+j]

# Calculate the distance of each point
def getdisancema(array1, array2,cell_xcor,cell_ycor):
    # check whether it is in the cell
    dismatrix = [0 for i in range(695)]

    for i in range(695):
        if(abs(array1[i] - cell_xcor)<length/2):
            if (abs(array2[i] - cell_ycor) < length / 2):
                dismatrix[i] = 1

    return dismatrix

def delrepeat(a):
    #delete repeat points in outliers

    ll2=[]
    for i in a:

        if i not in ll2:
            ll2.append(i)
    return ll2

if __name__ == '__main__':
    pause_video=[0 for i in range(695)]

    play_video=[0 for i in range(695)]
    length=8#the length of each cell
    thresh = 4#num of points inside one cell
    #D_Area=max_pause*max_play


    dataq = read_datasets()
    max_pause = max(pause_video)
    max_play = max(play_video)
    cell_per_length = max_pause //length + 1  # 横轴上多少个
    cell_per_height = max_play // length + 1  # 纵轴上多少个
    total_cells = cell_per_length * cell_per_height
    #int(total_cells)
    count = [0 for i in range(int(total_cells))]
    assignments_count = [0 for i in range(int(total_cells))]
    qfivea_count = [0 for i in range(int(total_cells))]
    qfivec_count = [0 for i in range(int(total_cells))]
    store_points= [[] for i in range(int(total_cells))]
    outlier=[]
    step_two()
    #print(count)

    #print(len(count),cell_per_length,cell_per_height)
    #for i in range(int(cell_per_height)):
    #    for j in range(int(cell_per_length)):
    #        print(count[int(cell_per_length)*i+j],end = "")
    #    print()
    step_three()
    step_fivea()
    #print()
    #for i in range(int(cell_per_height)):
    #    for j in range(int(cell_per_length)):
    #        print(count[int(cell_per_length)*i+j],end = "")
    #    print()
    #print(pause_video)
    #print(play_video)
    #print("dataq len:", len(dataq))
    print(max_pause,max_play)
    print(cell_per_length,cell_per_height)
    print(total_cells)
    #print(count)
    #print(assignments_count)
    noutlier=delrepeat(outlier)
    print(len(noutlier))
    print(noutlier)
