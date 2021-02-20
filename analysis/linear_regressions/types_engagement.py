import matplotlib.pyplot as plt
import numpy as np
from secret import cur, conn
from sklearn.linear_model import LinearRegression

for engagement in ["favorites", "retweets"]:
    cur.execute(f"SELECT {engagement}, type FROM tweets WHERE type != '?' AND type != 'f';")
    data = sorted(cur.fetchall(), key=lambda k: k[0])
    xs, ys = map(list,zip(*data))
    x = np.array(xs).reshape((-1, 1))
    for t in ['p', 'i', 'c', 'n', 'a', 'l']:
        ty = [1 if y == t else 0 for y in ys]
        y = np.array(ty)
        model = LinearRegression().fit(x, y)
        r_sq = model.score(x, y)
        print(f'r^2 {engagement} {t}:', r_sq)
        plt.scatter(x, y)
        plt.savefig(f"output/linear_regressions/types_engagement/{engagement}/2{t}.png")
        plt.clf()