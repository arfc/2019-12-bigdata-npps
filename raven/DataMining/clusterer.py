#!/usr/bin/python

import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering, KMeans, DBSCAN
from sklearn.metrics import silhouette_score, silhouette_samples

def optimal_cluster_elbow (X):
    
    sum_of_squared_distances = []
    ncluster = range(2,20)
    for k in ncluster:
        fitting = KMeans(n_clusters=k).fit(X)
        sum_of_squared_distances.append(fitting.inertia_)
    plt.plot(ncluster, sum_of_squared_distances, 'bx-')
    plt.xlabel('cluster_size')
    plt.ylabel('sum_of_squared_distances')
    plt.savefig('optimal_cluster_elbow', dpi=500, bbox_inches='tight')

def optimal_cluster_silhouette (X):
    
    silhouette_coeff = []
    ncluster = range(2,20)
    for k in ncluster:
        fitting = AgglomerativeClustering(n_clusters=k).fit(X)
        labels = fitting.labels_
        silhouette_coeff.append(silhouette_score(X, labels))
    plt.plot(ncluster, silhouette_coeff, 'bx-')
    plt.xlabel('cluster_size')
    plt.ylabel('silhouette_score')
    plt.savefig('optimal_cluster_silhouette', dpi=500, bbox_inches='tight')

def read_features_targets(csvfile):
     with open(csvfile) as f:
          grid_output_dict = [{k: v for k, v in row.items()}
              for row in csv.DictReader(f, skipinitialspace=True)]
     
     classlist=[]
     kinflist=[]
     convlist=[]
     fluxist=[]
     feedlist=[]
     fuellist=[]
     saltlist=[]
     U35list=[]
     Ulist=[]
     pitchlist=[]
     Tlist=[]
     ratiolist=[]

     for key1 in grid_output_dict:
          kinf=float(key1['k_inf'])
          conv=float(key1['conversion_ratio'])
          flux=float(key1['fast_flux_graph'])
          feed=float(key1['feedback_doppler'])
          kinflist.append(kinf)
          convlist.append(conv)
          fluxist.append(flux)
          feedlist.append(feed)

          
          fuel=float(key1['fuel_type'])
          salt=float(key1['salt_type'])
          f_U35=float(key1['U235F4_mole_frac'])
          f_U=float(key1['UF4_mole_frac'])
          pitch=float(key1['pitch'])
          Tave=float(key1['Tave_fuel'])
          f_ms=float(key1['mod_salt_ratio'])
          fuellist.append(fuel)
          saltlist.append(salt)
          U35list.append(f_U35)
          Ulist.append(f_U)
          pitchlist.append(pitch)
          Tlist.append(Tave)
          ratiolist.append(f_ms)
          
          classlist.append(key1['fuel_type']+key1['salt_type'])

     X=np.transpose([kinflist,convlist,fluxist,feedlist,fuellist,saltlist,U35list,Ulist,pitchlist,Tlist,ratiolist]) # features for classification
     y=np.transpose([classlist])  # targets for classification

     return X, y

filename='dataMineDummy.csv'
X, y = read_features_targets(filename)

datasets = [  X, y  ]

# axis definition: 0 for k_inf; 1 for conversion_ratio; 2 for fast flux  and 3 for feedback
xaxis, yaxis = 2, 3
zaxis, waxis = 0, 1
aaxis, baxis = 4, 5
caxis, daxis = 6, 7
eaxis, faxis = 8, 9
gaxis = 10

# first scale for better fitting
X = StandardScaler().fit_transform(X)

# Optimal cluster size determination: Elbow method
# optimal_cluster_elbow (X)
# Optimal cluster size determination: Silhouette method
# optimal_cluster_silhouette (X)

# This part is for contour plot
x_min, x_max = X[:, xaxis].min() - .5, X[:, xaxis].max() + .5
y_min, y_max = X[:, yaxis].min() - .5, X[:, yaxis].max() + .5
z_min, z_max = X[:, zaxis].min() - .5, X[:, zaxis].max() + .5
w_min, w_max = X[:, waxis].min() - .5, X[:, waxis].max() + .5
a_min, a_max = X[:, aaxis].min() - .5, X[:, aaxis].max() + .5
b_min, b_max = X[:, baxis].min() - .5, X[:, baxis].max() + .5
c_min, c_max = X[:, caxis].min() - .5, X[:, caxis].max() + .5
d_min, d_max = X[:, daxis].min() - .5, X[:, daxis].max() + .5
e_min, e_max = X[:, eaxis].min() - .5, X[:, eaxis].max() + .5
f_min,  f_max = X[:,  faxis].min() - .5, X[:,  faxis].max() + .5
g_min, g_max = X[:, gaxis].min() - .5, X[:, gaxis].max() + .5

mesh=200
x1s = np.linspace(x_min, x_max, mesh)
x2s = np.linspace(y_min, y_max, mesh)
x3s = np.linspace(z_min, z_max, mesh)
x4s = np.linspace(w_min, w_max, mesh)
x5s = np.linspace(a_min, a_max, mesh)
x6s = np.linspace(b_min, b_max, mesh)
x7s = np.linspace(c_min, c_max, mesh)
x8s = np.linspace(d_min, d_max, mesh)
x9s = np.linspace(e_min, e_max, mesh)
x10s = np.linspace(f_min, f_max, mesh)
x11s = np.linspace(g_min, g_max, mesh)
xx, yy = np.meshgrid(x1s, x2s)
zz, ww = np.meshgrid(x3s, x4s)
aa, bb = np.meshgrid(x5s, x6s)
cc, cc = np.meshgrid(x7s, x7s)
dd, ee = np.meshgrid(x8s, x9s)
ff, gg = np.meshgrid(x10s, x11s)

# Optimal cluster: 4 or 5 for KMeans from Silhouette and Elbow analyses
nclass=5
names = [ 
         "DBScan",
         "KMeans", 
         "Agglomerative",
         ]
clusterers = [
    DBSCAN(eps=0.2,min_samples=20),
    KMeans(n_clusters=nclass),
    AgglomerativeClustering(n_clusters=nclass),
]

# figure properties
plt.figure(figsize=(5*len(clusterers), 6))
cm = 'Spectral'
msize=2

# iterate over clusterers
i = 1
for name, clf in zip(names, clusterers):
    print(name)
    ax = plt.subplot(len(datasets), len(clusterers), i)
    
    if hasattr(clf, "fit_predict"):
        clf.fit(X)
        labels = clf.fit_predict(X)
        score =0
        Z = clf.fit_predict(np.c_[xx.ravel(), yy.ravel(), zz.ravel(), ww.ravel(), aa.ravel(), bb.ravel(), cc.ravel(), dd.ravel(), ee.ravel(), ff.ravel(), gg.ravel()])

    else:

        clf.fit(X, y.ravel())
        labels = clf.predict(X)
        score = clf.score(X, y.ravel())
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel(), zz.ravel(), ww.ravel(), aa.ravel(), bb.ravel(), cc.ravel(), dd.ravel(), ee.ravel(), ff.ravel(), gg.ravel()])
 
    # Put the result into a color plot
    Zlabel = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Zlabel, cmap=cm, alpha=0.4)
   
    # Plot the training points for clusterers
    ax.scatter(X[:, xaxis], X[:, yaxis], c=labels, cmap=cm, s=msize, alpha=0.8)
    
    # x_min, x_max = 0.25, 2.4
    # y_min, y_max = 0, 3
    x_min, x_max = 5, 110
    y_min, y_max = -10, 5    
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_title(name)

    i += 1

plt.tight_layout()
# plt.xlabel("$Fast flux per source$", fontsize=10)
# plt.ylabel("$Feedback coeff. (pcm)$", fontsize=10)
plt.savefig('clusterers', dpi=500, bbox_inches='tight')


