import sklearn.linear_model as lm
import sklearn.model_selection as ms
import numpy as np
import random
import networkx as nx
import networkx.algorithms.centrality as nc
import os, sys
sys.path.insert(0, '../')
import models.hawkes as hs
import graph_manip.graphAttribs as ga
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sklearn.metrics as mt


def loadMap(filename, numNodes):
    nodeCount = np.zeros((numNodes, 46))
    graphlets = open(os.path.join("graphlets", filename), "rb")
    for line in graphlets:
        data = line.split()
        n1 = int(data[0])
        n2 = int(data[1][:-1])
        for i in range(46):
            nodeCount[n1][i] += int(data[i + 2])
            nodeCount[n2][i] += int(data[i + 2])
    return nodeCount

def logReg(trainX, trainY, testData):
    
    model = lm.LinearRegression()
    model.fit(trainX, trainY)

    total_top_1_log  = []
    total_top_5_log  = []
    total_top_10_log = []
 
    for i in range(len(testData[0])):
        if len(testData[1][i]) > 0:
            curY = testData[1][i]
            predY = model.predict(testData[0][i])
            ordY = np.argsort(curY)
            ordPredY = np.argsort(predY)
            top_1 = set(ordY[-1:]) & set(ordPredY[-1:])
            top_5 = set(ordY[-5:]) & set(ordPredY[-5:])
            top_10 = set(ordY[-10:]) & set(ordPredY[-10:])

            total_top_1_log.append(len(top_1))
            total_top_5_log.append(len(top_5))
            total_top_10_log.append(len(top_10))
    print model.coef_
    return np.mean(total_top_1_log), np.mean(total_top_5_log), np.mean(total_top_10_log) 


    

def main():

    # Initialize values
    outData = []
    count = 0
    total_theta = 0
    total_num = 0
    graph_nodes = 0

    # Find the average critical theta for the shuffled graphs
#    for filename in os.listdir("graphlets"):
#        if filename.endswith("gfc"): 
#            
#            # Load up the related graphs
#            gDat = open(os.path.join("graphs", filename[:-4] + ".dat"), "rb")
#            firstLine = gDat.readline().split()
#
#            # Get the critical values
#            G = nx.read_edgelist(gDat, nodetype=int)
#            total_theta += ga.getCritTheta(G)
#            total_num += 1
#            print(str(total_num) + ': \t' + str((1.0 * total_theta)/total_num))
#            sys.stdout.flush()

    # Take the average of the calculated theta
    theta = 0.9965 * 0.013591952379440648 #total_theta / total_num
 
    # Load in data from files
    outData = []
    for filename in os.listdir("graphlets"):
        if filename.endswith("gfc"):
            
            # Load up the related graph
            gDat = open(os.path.join("graphs", filename[:-4] + ".dat"), "rb")
            firstLine = gDat.readline().split()
            G = nx.read_edgelist(gDat, nodetype=int)
            N = int(firstLine[0])
            graph_nodes = N
            
            # Load up the local graphlet counts
            nodeCount = loadMap(filename, N)
           
            D, V = hs.getEigData(G)
            # Calculate the expected hawkes events from each
            # node
            hVec = hs.getHawkesVecFromEig(D, V, theta)
            print "Done with Hawkes"
            dCent = nc.degree_centrality(G)
            print "Done with Degree"
           # eCent = nc.eigenvector_centrality(G)
           # print "Done with Eigen"
           # cCent = nc.closeness_centrality(G)
           # print "Done with closeness"
           # bCent = nc.harmonic_centrality(G)
           # print "Done with harmonic"
            # Store data as [local graphlets, degree centrality, eigen centrality, hawkes events, closeness centrality]
            outData.append([[], [], [], [], [], []])
            if len(hVec) > 0:
                for j in range(N):
                    #i = random.randint(0, N - 1)
                    outData[-1][0].append(nodeCount[j][np.array([1,0,10,11])])
                    outData[-1][1].append([dCent[j], dCent[j] ** 2, dCent[j] ** 3, dCent[j] ** 4])
                    outData[-1][2].append(0)#eCent[j])
                    outData[-1][3].append(hVec[j])
                    outData[-1][4].append(0)#cCent[j])
                    outData[-1][5].append(0)#bCent[j])
            count += 1
            print(count)
            sys.stdout.flush()

    # Process data for both linear regression and ordering

    separated_dat = []
    log_dat = []

    test_ind = set(random.sample(range(len(outData)), int(len(outData) * 0.3)))
    print test_ind

    # Process top-k data
    log_dat = [[[],[],[],[], [], []],[[],[],[],[], [], []]]
    for i in range(len(outData)):
        sort_ind = np.argsort(outData[i][3])
        new_dat = np.zeros(len(outData[i][1]))#np.linspace(0, 1, len(theta_dat[1][i][1]))
        new_dat[-10:] = 1
        if i in test_ind:
            log_dat[0][0].append(np.asarray(outData[i][0])[sort_ind])
            log_dat[0][1].append(np.asarray(outData[i][1])[sort_ind])
            log_dat[0][2].append(np.asarray(outData[i][2])[sort_ind].reshape(-1,1))
            log_dat[0][4].append(np.asarray(outData[i][4])[sort_ind].reshape(-1,1))
            log_dat[0][5].append(np.asarray(outData[i][5])[sort_ind].reshape(-1,1))
            log_dat[0][3].append(np.asarray(outData[i][3])[sort_ind])
        else:
            log_dat[1][0] += np.asarray(outData[i][0])[sort_ind].tolist()
            log_dat[1][1] += np.asarray(outData[i][1])[sort_ind].tolist()
            log_dat[1][2] += np.asarray(outData[i][2])[sort_ind].tolist()
            log_dat[1][4] += np.asarray(outData[i][4])[sort_ind].tolist()
            log_dat[1][5] += np.asarray(outData[i][5])[sort_ind].tolist()
            log_dat[1][3] += new_dat.tolist()

    # Initialize data arrays

    # Get logistic regression rankings
    top_1_graph, top_5_graph, top_10_graph = logReg(log_dat[1][0], log_dat[1][3], (log_dat[0][0], log_dat[0][3]))
    print(top_1_graph, top_5_graph, top_10_graph)
    top_1_graph, top_5_graph, top_10_graph = logReg(np.asarray(log_dat[1][1]), log_dat[1][3], (log_dat[0][1], log_dat[0][3]))
    print(top_1_graph, top_5_graph, top_10_graph)
    top_1_graph, top_5_graph, top_10_graph = logReg(np.asarray(log_dat[1][2]).reshape(-1,1), log_dat[1][3], (log_dat[0][2], log_dat[0][3]))
    print(top_1_graph, top_5_graph, top_10_graph)
    top_1_graph, top_5_graph, top_10_graph = logReg(np.asarray(log_dat[1][4]).reshape(-1,1), log_dat[1][3], (log_dat[0][4], log_dat[0][3]))
    print(top_1_graph, top_5_graph, top_10_graph)
    top_1_graph, top_5_graph, top_10_graph = logReg(np.asarray(log_dat[1][5]).reshape(-1,1), log_dat[1][3], (log_dat[0][5], log_dat[0][3]))
    print(top_1_graph, top_5_graph, top_10_graph)

main()
