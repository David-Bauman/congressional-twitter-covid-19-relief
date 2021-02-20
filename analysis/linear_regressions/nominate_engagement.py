import matplotlib.pyplot as plt
import numpy as np
from secret import cur, conn
from sklearn.linear_model import LinearRegression

cur.execute("SELECT twitter_id, nominate FROM mcs;")
twitter_id_to_nominate = {}
for (tid, nominate) in cur.fetchall():
    twitter_id_to_nominate[tid] = nominate

nominates = []
retweets = []
favorites = []
hashtags = []
data = {}
cur.execute("SELECT user_id, retweets, favorites, num_hashtags FROM tweets;")
for (tid, r, f, nh) in cur.fetchall():
    if tid not in twitter_id_to_nominate:
        continue
    nom = twitter_id_to_nominate[tid]
    if nom not in data:
        data[nom] = {'n': 0, 'retweets': 0, 'favorites': 0, 'num_hashtags': 0}
    data[nom]["n"] += 1
    data[nom]["retweets"] += r
    data[nom]["favorites"] += f
    data[nom]["num_hashtags"] += nh

for nom, dic in sorted(data.items(), key=lambda k: k[0]):
    n = dic["n"]
    r = dic["retweets"]
    f = dic["favorites"]
    nominates.append(nom)
    retweets.append(r/n)
    favorites.append(f/n)
    hashtags.append(dic["num_hashtags"]/n)


x = np.array(nominates).reshape((-1, 1))
y = np.array(hashtags)

model = LinearRegression().fit(x, y)
r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)
print('slope:', model.coef_)
plt.plot(x, y)
plt.savefig("output/linear_regressions_nominate.png")