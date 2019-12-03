
import numpy as np
import matplotlib.pyplot as plt

results = []

f = open("17.11.2019_1800-1900.txt", "r")

lines = f.readlines()

# : ya gore veriyi bolme
for line in lines:
    a = line.split(':')
    results.append(int(a[1]))

datasets = ['art', 'economy', 'politics', 'sport', 'technology']

# grafik
plt.bar(datasets, results)
plt.xlabel('datasets')
plt.ylabel('results')
plt.title('17.11.2019_1800-1900')
plt.show()
