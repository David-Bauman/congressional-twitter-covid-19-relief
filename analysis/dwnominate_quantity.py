import datetime
import matplotlib.pyplot as plt
import numpy as numpy
from secret import cur, conn
from sklearn.linear_model import LinearRegression

cur.execute("SELECT user_id FROM tweets;")

user_id_to_num_tweets = {}
for (uid,) in cur:
    if uid not in user_id_to_num_tweets:
        user_id_to_num_tweets[uid] = 0
    user_id_to_num_tweets[uid] += 1

cur.execute("SELECT twitter_id, nominate FROM mcs;")

nominates = []
num_tweets = []

for (twitter_id, nominate) in cur:
    if twitter_id in user_id_to_num_tweets:
        nominates.append(abs(nominate))
        num_tweets.append(user_id_to_num_tweets[twitter_id])

plt.scatter(nominates, num_tweets)
plt.ylabel("Number of tweets")
plt.xlabel("DW-NOMINATE Score")
plt.savefig("output/dwnominate_quantity.png")

x = np.array(nominates).reshape(-1, 1)
y = num_tweets
model = LinearRegression().fit(x, y)
r_sq = model.score(x, y)
print(f'r^2:', r_sq)