import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression, SGDClassifier, SGDRegressor
import time
import warnings
warnings.filterwarnings('ignore')

############################

print(1)
train_data = pd.read_csv("data/train.csv")
test_data = pd.read_csv("data/test.csv")

fil_train_data = pd.read_csv("data/filtered_train.csv").fillna(0)
fil_test_data = pd.read_csv("data/filtered_test.csv").fillna(0)


############################

print(2)
cols_num = []
cols_others = []
dtypes = train_data.dtypes
for i in range(len(dtypes)):
    if dtypes[i] in ['int64', 'float64']:
        cols_num.append(dtypes.index[i])
    else:
        cols_others.append(dtypes.index[i])

train_nums = train_data[cols_num].fillna(0)
cols_others.remove('MachineIdentifier')
train_others = train_data[cols_others]
test_others = test_data[cols_others]

############################

print(3)
cols_num.remove('HasDetections')
test_nums = test_data[cols_num].fillna(0)

features = train_nums[cols_num]
results = train_nums['HasDetections']

############################

print(4)
n = len(features)
x_train_tmp = features[:n]
y_train = results[:n]

x_test_tmp = test_nums[:n]

x_train = pd.concat([x_train_tmp, fil_train_data], axis=1)
x_test = pd.concat([x_test_tmp, fil_test_data], axis=1)

############################

print(5)
x_train1 = sklearn.preprocessing.scale(x_train)
x_test1 = sklearn.preprocessing.scale(x_test)

log_reg1 = LogisticRegression(random_state=0, solver='lbfgs', multi_class="multinomial").fit(x_train1, y_train)

predict1 = log_reg1.predict(x_test1)

d1 = {'MachineIdentifier': test_data['MachineIdentifier'][:n], 'HasDetections': predict1}
output1 = pd.DataFrame(data=d1)

output1.to_csv("output1.csv", index=False)

predict11 = log_reg1.predict(x_train1)
print(len(predict11))
print(predict11.head())
print("Score: {:.3f}".format(sum(predict11 == y_train)/n))

############################

print(6)
x_train2 = sklearn.preprocessing.scale(x_train)
x_test2 = sklearn.preprocessing.scale(x_test)

log_reg2 = LogisticRegression(random_state=0, solver='lbfgs', multi_class="multinomial").fit(x_train2, y_train)

predict2 = log_reg2.predict(x_test2)

d2 = {'MachineIdentifier': test_data['MachineIdentifier'][:n], 'HasDetections': predict2}
output2 = pd.DataFrame(data=d2)

output2.to_csv("output2.csv", index=False)

predict22 = log_reg2.predict(x_train2)

print("Score: {:.3f}".format(sum(predict22 == y_train)/n))

############################

print(7)
log_reg3 = LogisticRegression(random_state=0, solver='lbfgs', multi_class="multinomial").fit(x_train, y_train)

predict3 = log_reg3.predict(x_test)

d3 = {'MachineIdentifier': test_data['MachineIdentifier'][:n], 'HasDetections': predict3}
output3 = pd.DataFrame(data=d3)

output3.to_csv("output3.csv", index=False)

predict33 = log_reg3.predict(x_train)

print("Score: {:.3f}".format(sum(predict33 == y_train)/n))

############################

print(8)
sgd1 = SGDClassifier(loss="hinge", penalty="l2", max_iter=5).fit(x_train, y_train)

predict4 = sgd1.predict(x_test)

d4 = {'MachineIdentifier': test_data['MachineIdentifier'][:n], 'HasDetections': predict4}
output4 = pd.DataFrame(data=d4)

output4.to_csv("output4.csv", index=False)

predict44 = sgd1.predict(x_train)
print("Score: {:.3f}".format(sum(predict44 == y_train)/n))

############################

print(9)
sgd2 = SGDRegressor().fit(x_train, y_train)

predict5 = sgd2.predict(x_test)

d5 = {'MachineIdentifier': test_data['MachineIdentifier'][:n], 'HasDetections': predict5}
output5 = pd.DataFrame(data=d5)

output5.to_csv("output5.csv", index=False)

predict55 = sgd2.predict(x_train)
print("Score: {:.3f}".format(sum(predict55 == y_train)/n))

np.round(predict55)
















