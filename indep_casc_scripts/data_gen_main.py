import joint_single as ms
import neighbors_twolevel as up
import casc_gen_graph as cg
import find_knodes as fk
import numpy as np
import seaborn as sb
import pandas as pd
import matplotlib.pyplot as plt

#inputs: name of data, path to original edge txt, factor X
#main function for generating ROC and N-nodes data
def data_gen(data,graph,X):
    for i in range(5):
      cg.gen(data,"../data/orig_graphs/"+graph)
      ms.main_subgraph(data,graph,X)
      up.update(data,[5,10,15,20,25])
      for i in range(3,6):
          fk.test_eff(data,graph,i)

#inputs: name of data, list of values of k to be tested
#plots rocs of various k in tests (both degree and graphlet features) for a given input data
def plot_roc(data,tests):
    toplot=pd.DataFrame()
    deg_fin=pd.DataFrame()
    for k in tests:
        #get ROCs for graphlet and degree features
        rocs=pd.read_csv("../data/"+str(data)+"/rocGraphs/"+str(k)+str(data)+"reg.txt",sep="\n",header=None).iloc[:35,:]
        degs=pd.read_csv("../data/"+str(data)+"/centROC/"+str(k)+str(data)+"reg.txt",sep="\n",header=None).iloc[:35,:]
        #grph column contains ROC values, k column contains which tested k the ROC belongs to
        temp_deg=pd.DataFrame({"grph": list(degs.iloc[:,0]), "k": [k]*len(list(degs.iloc[:,0]))})
        temp_rocs=pd.DataFrame({"grph": list(rocs.iloc[:,0]), "k": [k]*len(list(rocs.iloc[:,0]))})
        deg_fin=pd.concat([deg_fin,temp_deg],axis=0)
        toplot=pd.concat([toplot,temp_rocs],axis=0)
        #print mean and stdev of the ROCs for each k-value
        print(str(k)+"mean(deg): "+str(np.mean(degs.iloc[:,0]))+", std: "+str(np.std(degs.iloc[:,0])))
        print(str(k)+"mean(graphlets): "+str(np.mean(rocs.iloc[:,0]))+", std: "+str(np.std(rocs.iloc[:,0])))
    #mark rows as graphlet or degree
    toplot["type"]=list("g"*toplot.shape[0])
    deg_fin["type"]=list("d"*deg_fin.shape[0])
    toplot=toplot.append(deg_fin)
    print(toplot)
    plt.clf()
    ax=sb.boxplot(x=toplot['k'],y=toplot['grph'],hue=toplot["type"])
    ax.set_title("AUC scores of Graphlet/Degree-Based Models, "+str(data))
    ax.set_ylabel('AUC')
    ax.set_xlabel('')
    plt.savefig("../data/"+str(data)+"/rocs.png")

#data_gen("alv-X10","soc-advogato.txt",10)
plot_roc("alv-X10",[5,10,15,20,25])
