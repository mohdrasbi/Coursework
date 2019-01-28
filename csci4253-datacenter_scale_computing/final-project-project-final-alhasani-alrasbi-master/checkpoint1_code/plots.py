import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_num_awards(path, ax, title):
    df = pd.read_csv(path)
    x = [i for i in df["awarding_agency_name"].value_counts().index]
    y = [df["awarding_agency_name"].value_counts()[i] for i in x]
    for i in range(len(x)):
        x[i] = x[i][x[i].find("(")+1:-1]
    
    ax.bar(x, y)
    ax.set_title(title)

def plot_tot_funding(path, ax, title):
    df = pd.read_csv(path)
    x = [i for i in df["awarding_agency_name"].value_counts().index]
    y = []
    for i in range(len(x)):
        y.append(df[df["awarding_agency_name"] == x[i]]["total_funding_amount"].sum()/10**6)
        x[i] = x[i][x[i].find("(")+1:-1]
    
    ax.bar(x, y)
    ax.set_title(title)


#Assume the files are in a directory called datasets
fig, axes = plt.subplots(3, 3, figsize=(24, 16))
fig.suptitle("Number of awards every FY for each agency", size=25)
plot_num_awards("datasets/2010.csv", axes[0, 0], "2010")
plot_num_awards("datasets/2011.csv", axes[0, 1], "2011")
plot_num_awards("datasets/2012.csv", axes[0, 2], "2012")
plot_num_awards("datasets/2013.csv", axes[1, 0], "2013")
plot_num_awards("datasets/2014.csv", axes[1, 1], "2014")
plot_num_awards("datasets/2015.csv", axes[1, 2], "2015")
plot_num_awards("datasets/2016.csv", axes[2, 0], "2016")
plot_num_awards("datasets/2017.csv", axes[2, 1], "2017")
plot_num_awards("datasets/2018.csv", axes[2, 2], "2018")
plt.savefig("1")

fig, axes = plt.subplots(3, 3, figsize=(24, 16))
fig.suptitle("Total funding every FY for each agency (in millions)", size=25)
plot_tot_funding("datasets/2010.csv", axes[0, 0], "2010")
plot_tot_funding("datasets/2011.csv", axes[0, 1], "2011")
plot_tot_funding("datasets/2012.csv", axes[0, 2], "2012")
plot_tot_funding("datasets/2013.csv", axes[1, 0], "2013")
plot_tot_funding("datasets/2014.csv", axes[1, 1], "2014")
plot_tot_funding("datasets/2015.csv", axes[1, 2], "2015")
plot_tot_funding("datasets/2016.csv", axes[2, 0], "2016")
plot_tot_funding("datasets/2017.csv", axes[2, 1], "2017")
plot_tot_funding("datasets/2018.csv", axes[2, 2], "2018")
plt.savefig("2")