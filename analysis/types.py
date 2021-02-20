import datetime
import json
import matplotlib.dates as dates
import matplotlib.pyplot as plt
from collections import defaultdict
from secret import cur, conn

cur.execute("SELECT type FROM tweets WHERE type!='?';")

types = defaultdict(int)

for (typ,) in cur.fetchall():
    types[typ] += 1
print(types)

x = []
heights = []
sorted_types = sorted(types.items(), key=lambda r: r[1], reverse=True)
for (k, v) in sorted_types:
    x.append(k)
    heights.append(v)

plt.bar(x, heights)
plt.savefig("output/types")