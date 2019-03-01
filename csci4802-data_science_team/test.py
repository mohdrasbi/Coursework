import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
import time
import warnings
warnings.filterwarnings('ignore')

##################################

train_data = pd.read_csv("/Users/mohd/Desktop/data/train.csv")
test_data = pd.read_csv("/Users/mohd/Desktop/data/test.csv")

##################################

n = len(features)
x_train = features[:n]
y_train = results[:n]
x_test = test_d2[:n]

x_train = sklearn.preprocessing.scale(x_train)
x_test = sklearn.preprocessing.scale(x_test)

log_reg = LogisticRegression(random_state=0, solver='lbfgs', multi_class="multinomial").fit(x_train, y_train)

predict = log_reg.predict(x_test)

d = {'MachineIdentifier': test_data['MachineIdentifier'][:n], 'HasDetections': predict}
output = pd.DataFrame(data=d)

output.to_csv("output.csv", index=False)