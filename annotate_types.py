import datetime
import mariadb
import os
import random
from secret import MYSQL_PASSWORD, MYSQL_USER, conn, cur

cur.execute("SELECT created_at, text FROM tweets WHERE type='?';")

rows = cur.fetchall()

random.shuffle(rows)

"""
enum type:
    ? = not annotated yet
    f = false positive, tweet is not about covid relief
    c = credit claiming
        "I voted YES on the Paycheck Protection Program that Republicans and President @realDonaldTrump pushed to be included in the CARES Act. The PPP has provided $80 million in loans to Peoria businesses and saved 15,000 Peoria jobs!" - 2020-08-10 18:12:10
    a = advertising
        "Full day. The @ProbSolveCaucus zoomed w/ guest @GovLarryHogan to discuss a # of issues that require bipartisan solutions. We also discussed efforts to improve PPP. Next week, I'm heading to DC to be present for several votes. Stay tuned. #MI06"
        Note how it doesn't stake a position on any issue. The only thing you get out of it is an the impression of a hardworker.
    p = position taking
        Often like "I urge the President to get behind/sign into law...."
        Or: "PPP funds should not be going to Planned Parenthood" came up often
    n = negative partisan statement (other side sucks)
        "Democrats blocked another Coronavirus relief package that would have extended the PPP and provided critical aid to workers. Clearly, they don’t care about helping the people. They just want to bail out blue states and push their leftist pet projects." - 2020-09-14 18:15:00 
    l = positive partisan statement (party loyalty)
    i = informational
        "If you need to apply for unemployment benefits please go to https://t.co/NDbajrBBAf." - 2020-03-21 21:13:43
        Usually directing constituents towards resources such as applying for PPP or describing covid relief scams
"""
cur.execute("SELECT COUNT(*) FROM tweets WHERE type!='?';")
i = cur.fetchall()[0][0]
cur.execute("SELECT COUNT(*) FROM tweets;")
total = cur.fetchall()[0][0]
for (created_at, text) in rows:
    i += 1
    print("{}/{}".format(i, total))
    print(text)
    typ = input("> ")
    while len(typ) != 1:
        print("{} is not okay.".format(typ))
        typ = input("> ")
    cur.execute("UPDATE tweets SET type=%s WHERE created_at=%s;", (typ, created_at))
    conn.commit()
    os.system("clear")
