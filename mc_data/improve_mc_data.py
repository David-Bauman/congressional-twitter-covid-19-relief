import json
import yaml

STATE_TO_ABBREV = {
  "Alabama": "AL",
  "Alaska": "AK",
  "American Samoa": "AS",
  "Arizona": "AZ",
  "Arkansas": "AR",
  "California": "CA",
  "Colorado": "CO",
  "Connecticut": "CT",
  "Delaware": "DE",
  "District of Columbia": "DC",
  "Federated States Of Micronesia": "FM",
  "Florida": "FL",
  "Georgia": "GA",
  "Guam": "GU",
  "Hawaii": "HI",
  "Idaho": "ID",
  "Illinois": "IL",
  "Indiana": "IN",
  "Iowa": "IA",
  "Kansas": "KS",
  "Kentucky": "KY",
  "Louisiana": "LA",
  "Maine": "ME",
  "Marshall Islands": "MH",
  "Maryland": "MD",
  "Massachusetts": "MA",
  "Michigan": "MI",
  "Minnesota": "MN",
  "Mississippi": "MS",
  "Missouri": "MO",
  "Montana": "MT",
  "Nebraska": "NE",
  "Nevada": "NV",
  "New Hampshire": "NH",
  "New Jersey": "NJ",
  "New Mexico": "NM",
  "New York": "NY",
  "North Carolina": "NC",
  "North Dakota": "ND",
  "Northern Mariana Islands": "MP",
  "Ohio": "OH",
  "Oklahoma": "OK",
  "Oregon": "OR",
  "Palau": "PW",
  "Pennsylvania": "PA",
  "Puerto Rico": "PR",
  "Rhode Island": "RI",
  "South Carolina": "SC",
  "South Dakota": "SD",
  "Tennessee": "TN",
  "Texas": "TX",
  "Utah": "UT",
  "Vermont": "VT",
  "Virgin Islands": "VI",
  "Virginia": "VA",
  "Washington": "WA",
  "West Virginia": "WV",
  "Wisconsin": "WI",
  "Wyoming": "WY"
}

PARTY_CODE_TO_PARTY = {
  200: "R",
  100: "D",
  328: "L"
}

with open("mc_data/media.yaml", "r") as f:
  media = yaml.safe_load(f)
media_data = {}
for member in media:
    uid = member["id"]["bioguide"]
    media_data[uid] = member

with open("mc_data/legislators.yaml", "r") as f:
  legislators = yaml.safe_load(f)

with open("mc_data/nominate.json", "r") as f:
  nominate_data = json.load(f)
  ordered_nominate_data = {}
  for member in nominate_data:
    ordered_nominate_data[member["bioguide_id"]] = member

with open("mc_data/PVI-House.csv", "r") as f:
  house_PVI = {}
  for line in f.readlines():
    details = line.split(",")
    state, district = details[0].split("-")
    if district == "AL": # at-large
      district = 1 # it's what the nominate data does so for consistency, we do it too
    district = int(district)
    pvi = details[2]
    if state not in house_PVI:
      house_PVI[state] = {}
    house_PVI[state][district] = pvi

with open("mc_data/PVI-Senate.csv", "r") as f:
  senate_PVI = {}
  for line in f.readlines():
    details = line.split(",")
    state = details[0]
    pvi = details[1]
    senate_PVI[STATE_TO_ABBREV[state]] = pvi

improved_data = []
for legislator in legislators:
  if legislator["id"]["bioguide"] not in media_data:
      continue
  member = media_data[legislator["id"]["bioguide"]]
  data = {}
  data["id"] = member["id"]
  bioguide_id = member["id"]["bioguide"]
  if "social" in member and "twitter" in member["social"]:
    data["social"] = {"twitter": member["social"]["twitter"], "twitter_id": member["social"]["twitter_id"]}
  try:
    nominate_data = ordered_nominate_data[bioguide_id]
  except KeyError as e:
    print(e)
    continue
  data["nominate"] = nominate_data["nominate_dim1"]
  data["party"] = PARTY_CODE_TO_PARTY[nominate_data["party_code"]]
  data["chamber"] = nominate_data["chamber"]
  if data["chamber"] == "House":
    data["pvi"] = house_PVI[nominate_data["state_abbrev"]][nominate_data["district_code"]]
  else:
    data["pvi"] = senate_PVI[nominate_data["state_abbrev"]]
  data["name"] = nominate_data["bioname"]
  
  data["gender"] = legislator["bio"]["gender"] if "bio" in legislator and "gender" in legislator["bio"] else "?"
  improved_data.append(data)

print(len(improved_data))

with open("mc_data/improved_mc_data.json", "w") as f:
  json.dump(improved_data, f)