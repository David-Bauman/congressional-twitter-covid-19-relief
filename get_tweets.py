import json
import tweepy
import yaml
from secret import API_KEY, API_SECRET_KEY

auth = tweepy.AppAuthHandler(API_KEY, API_SECRET_KEY)
api = tweepy.API(auth)

def fetch_all_tweets(user_id):
  all_tweets = []
  try:
    new_tweets = api.user_timeline(user_id=user_id, count=200, include_rts=False, tweet_mode="extended")
  except tweepy.error.TweepError as e:
    print(e)
    return
  
  while len(new_tweets) > 0:
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1
    if all_tweets[-1].created_at.year < 2020:
      break
    try:
      new_tweets = api.user_timeline(user_id=user_id, count=200, include_rts=False, tweet_mode="extended", max_id=oldest)
    except tweepy.error.TweepError as e:
      print(e)
      break

  tweets = [tweet._json for tweet in all_tweets if tweet.created_at.year == 2020]
  with open(f"tweets/{user_id}.json", "w") as f:
    json.dump(tweets, f, ensure_ascii=False, indent=4)
  return

with open("mc_data/media.yaml", "r") as f:
  mcs_data = yaml.safe_load(f)

for mc_data in mcs_data:
  if "social" not in mc_data:
    print(mc_data)
    continue
  if "twitter_id" not in mc_data["social"]:
    print(mc_data)
    continue
  user_id = mc_data["social"]["twitter_id"]
  fetch_all_tweets(user_id)
  twitter = mc_data["social"]["twitter"]
  print(f"done with {twitter}")

