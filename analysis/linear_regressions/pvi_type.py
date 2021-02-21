import matplotlib.pyplot as plt
import numpy as np
from secret import cur, conn
from sklearn.linear_model import LinearRegression

cur.execute("SELECT twitter_id, pvi, party FROM mcs;")
twitter_id_to_seat_safety = {}
for (tid, pvi, party) in cur.fetchall():
    seat_safety = 0
    if party == "D":
        if pvi <= 2:
            seat_safety = abs(pvi-2)
        else:
            seat_safety = 2 - pvi
    else:
        seat_safety = pvi-2

    twitter_id_to_seat_safety[tid] = seat_safety

cur.execute("SELECT user_id, type FROM tweets WHERE type != '?' AND type != 'f';")
data = cur.fetchall()
for typ in  ['p', 'i', 'c', 'n', 'a', 'l']:
    d = {}
    for (tid, t) in data:
        if tid not in twitter_id_to_seat_safety:
            continue
        seat_safety = twitter_id_to_seat_safety[tid]
        if seat_safety not in d:
            d[seat_safety] = {'n': 0, 'type_value': 0}
        d[seat_safety]['n'] += 1
        d[seat_safety]['type_value'] += 1 if t == typ else 0

    d = sorted(d.items(), key=lambda i: i[0])
    xs, ys = map(list,zip(*d))
    ys = [y['type_value']/y['n'] for y in ys]

    x = np.array(xs).reshape((-1, 1))
    y = np.array(ys)

    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print(f'r^2 {typ}:', r_sq)
    plt.scatter(x, y)
    plt.savefig(f"output/linear_regressions/pvi_type/{typ}.png")
    plt.clf()