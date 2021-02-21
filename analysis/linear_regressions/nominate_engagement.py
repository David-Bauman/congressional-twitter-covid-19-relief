import matplotlib.pyplot as plt
import numpy as np
from secret import cur, conn
from sklearn.linear_model import LinearRegression

cur.execute("SELECT twitter_id, nominate FROM mcs;")
twitter_id_to_nominate = {}
for (tid, nominate) in cur.fetchall():
    twitter_id_to_nominate[tid] = nominate

for engagement in ["retweets", "favorites"]:
    nominates = []
    ys = []
    data = {}
    cur.execute(f"SELECT user_id, {engagement} FROM tweets;")
    for (tid, e) in cur.fetchall():
        if tid not in twitter_id_to_nominate:
            continue
        nom = twitter_id_to_nominate[tid]
        if nom not in data:
            data[nom] = {'n': 0, 'y': 0}
        data[nom]["n"] += 1
        data[nom]["y"] += e

    for nom, dic in sorted(data.items(), key=lambda k: k[0]):
        nominates.append(nom)
        ys.append(dic["y"]/dic["n"])


    x = np.array(nominates).reshape((-1, 1))
    y = np.array(ys)

    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print(f'r^2 {engagement}:', r_sq)
    plt.plot(x, y)
    plt.savefig(f"output/linear_regressions/nominate_engagement/{engagement}.png")
    plt.clf()