import json
import os

KEYWORDS = ["COVID relief", "stimulus checks", "$600", "$2000", "unemployment benefits", "PPP", "COVID19 relief", "COVID-19 relief"]
counter = 0
total_tweets = 0

files = sorted(os.listdir("./tweets/"))

matching_tweets = []

for filename in files:
  try:
    with open(f"tweets/{filename}", "r") as f:
      data = json.load(f)
    for item in data:
      total_tweets += 1
      text = item["full_text"]
      if any(keyword in text for keyword in KEYWORDS):
        counter += 1
        matching_tweets.append(item)
  except Exception as e:
    print(e)
  print(f"{filename} completed")

print(f"Final matched={counter:,} with keywords={KEYWORDS}")
print(f"Final tweet count={total_tweets:,}")