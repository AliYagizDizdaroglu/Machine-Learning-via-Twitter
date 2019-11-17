import numpy as np
import matplotlib.pyplot as plt

results = []

f = open("results.txt", "r", encoding="utf8")

lines = f.readlines()

for line in lines:
    a = line.split(':')
    results.append(int(a[1]))

datasets = ['art', 'economy', 'politics', 'sport', 'technology']

plt.bar(datasets, results)
plt.xlabel('datasets')
plt.ylabel('results')
plt.title('grafik')
plt.show()
