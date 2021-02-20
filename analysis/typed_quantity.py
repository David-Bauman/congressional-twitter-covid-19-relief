import datetime
import json
import matplotlib.dates as dates
import matplotlib.pyplot as plt
from collections import defaultdict
from secret import cur, conn

cur.execute("SELECT user_id, created_at, type FROM tweets;")
tweets = cur.fetchall()
typed = defaultdict(int)
gary = defaultdict(int)
for (tid, date, typ) in tweets:
  formatted_date = date.strftime("%Y-%m-%d")
  if typ != "?":
    typed[formatted_date] += 1
  gary[formatted_date] += 1


r_quantity = []
r_dates = []
sorted_r = sorted(typed.items(), key=lambda r: r[0])
for item in sorted_r:
  r_quantity.append(item[1])
  if (item[1] > 60):
    print(f"r: {item}")
  r_dates.append(datetime.datetime.strptime(item[0], "%Y-%m-%d"))

d_quantity = []
d_dates = []
sorted_d = sorted(gary.items(), key=lambda r: r[0])
for item in sorted_d:
  d_quantity.append(item[1])
  if (item[1] > 60):
    print(f"d: {item}")
  d_dates.append(datetime.datetime.strptime(item[0], "%Y-%m-%d"))

plt.gca().xaxis.set_major_formatter(dates.DateFormatter("%m-%d"))
plt.gca().xaxis.set_major_locator(dates.MonthLocator())
plt.plot(d_dates, d_quantity)
plt.plot(r_dates, r_quantity)
plt.ylabel("Number of tweets")
plt.xlabel("Date (2020)")
plt.gcf().autofmt_xdate()
plt.legend(["All Tweets", "Typed Tweets"], loc="upper left")
plt.savefig("output/typed_quantity.png")