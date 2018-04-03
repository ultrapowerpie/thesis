from matplotlib import pyplot as plt
import numpy as np
import csv

with open('data/tmp.csv', 'r') as f:
    csvreader = csv.reader(f, delimiter=',')
    a = zip(*csvreader)

h = list(map(float, a[0]))
print np.log(h)
plt.hist(np.nan_to_num(np.log(h)), np.arange(0,5, 0.1))
plt.show()
