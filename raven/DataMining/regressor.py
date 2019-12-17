#!/usr/bin/python

from sklearn import metrics
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVR, SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, RandomForestRegressor, AdaBoostRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import BayesianRidge
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
        fitting = KMeans(n_clusters=k).fit(X)
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

         
     X=np.transpose([fuellist,saltlist,U35list,Ulist,pitchlist,Tlist,ratiolist]) # features for regression
     y=np.transpose([kinflist,convlist,fluxist,feedlist])  # targets for regression
     # X=np.transpose([kinflist,convlist,fluxist,feedlist,fuellist,saltlist,U35list,Ulist,pitchlist,Tlist,ratiolist]) # features for classification
     # y=np.transpose([classlist])  # targets for classification
     
     return X, y

filename='dataMineDummy.csv'
X, y = read_features_targets(filename)

datasets = [  X, y  ]

X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# plot limits
# axis definition: 0 for k_inf; 1 for conversion_ratio; 2 for fast flux  and 3 for feedback
yxaxis, yyaxis = 2,3
yzaxis, ywaxis = 0,1
# yx_min, yx_max = 0, 2.5
# yy_min, yy_max = 0, 3
yx_min, yx_max = 0, 120
yy_min, yy_max = -10, 5

# yx_min, yx_max = y[:, yxaxis].min() - .5, y[:, yxaxis].max() + .5
# yy_min, yy_max = y[:, yyaxis].min() - .5, y[:, yyaxis].max() + .5

names = [ 
         "Random Forest",
         "Decision Tree",         
         "Neural Network", 
         "KNeighbors", 
         ]

regressors = [
    RandomForestRegressor(n_estimators=200),
    DecisionTreeRegressor(),
    MLPRegressor(max_iter=2000),
    KNeighborsRegressor(n_neighbors=5),
]

# figure properties
plt.figure(figsize=(5*len(regressors), 5))
cm = 'Spectral'
msize=2
alpha=0.5

# iterate over regressors
i = 1
for name, reg in zip(names, regressors):
    print(name)
    ax = plt.subplot(len(datasets), len(regressors), i)
    
    reg.fit(X, y)
    score = reg.score(X, y)
    y_pred = reg.predict(X_test)
        
    # Plot the training points for regressors
    plt.scatter(y_test[:, yxaxis], y_test[:, yyaxis], cmap=cm, s=msize, label="real_values")
    plt.scatter(y_pred[:, yxaxis], y_pred[:, yyaxis], cmap=cm, s=msize, label="predicted_values")
    
    ax.set_xlim(yx_min, yx_max)
    ax.set_ylim(yy_min, yy_max)
    ax.set_title(name)
    if score is not 0:
        ax.text(yx_min- 16, yy_min + 1, ('score=%.2f' % score).lstrip('0'), size=10, horizontalalignment='right')
        ax.text(yx_min- 16, yy_min + 2, ('abs_err=%.2f' % metrics.mean_absolute_error(y_test, y_pred)).lstrip('0'), size=10, horizontalalignment='right')
        ax.text(yx_min- 16, yy_min + 3, ('ms_err=%.2f' % metrics.mean_squared_error(y_test, y_pred)).lstrip('0'), size=10, horizontalalignment='right')
        ax.text(yx_min- 16, yy_min + 4, ('rms=%.2f' % np.sqrt(metrics.mean_squared_error(y_test, y_pred))).lstrip('0'), size=10, horizontalalignment='right')
    i += 1

plt.tight_layout()
plt.savefig('regressors', dpi=500, bbox_inches='tight')

