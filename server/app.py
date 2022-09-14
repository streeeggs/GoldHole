from flask import Flask
from bson.json_util import dumps
from bson.son import SON
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
from flask_cors import CORS
from collections import Counter
from dotenv import load_dotenv
from markupsafe import escape

import pandas as pd
import pprint
import os
import json

load_dotenv()
app = Flask(__name__)
app.config["MONGO_URI"] = os.environ["GH_CONN_STR"]
CORS(app, resources={r'/*': {'origins': '*'}})
mongo = PyMongo(app)

## Start Aggregates
# TODO: Organize this better and write comments for them
most_echo_by_title_aggregate = [
    {
      "$group": {
        "_id": {
          "title": "$title",
          "text": { "$toLower": "$message.text" }
        },
        "count": {
          "$sum": {
            "$cond": [
              {
                "$ne": [
                  {
                    "$type": "$message.text"
                  },
                  "missing"
                ]
              }, 1,0]
          }
        }
      }
    },
    {
       "$group": {
          "_id": "$_id",
          "out": { "$sum": "$count" }
       }
    },
    {
       "$project": {
          "Title": "$_id.title",
          "Message": "$_id.text",
          "Count": "$out"
       }
    },
    {
       "$sort": { "Count": -1 }
    }
 ]

most_echo_by_message_aggregate = [
    {
      "$group": {
        "_id": {
          "text": { "$toLower": "$message.text" }
        },
        "count": {
          "$sum": {
            "$cond": [
              {
                "$ne": [
                  {
                    "$type": { "$toLower": "$message.text" }
                  },
                  "missing"
                ]
              }, 1,0]
          }
        }
      }
    },
    {
       "$sort": { "count": -1, "_id.text": 1 }
    },
    {
       "$group": {
          "_id": "$_id.text",
          "out": { "$first": "$$ROOT" }
       }
    },
    {
       "$project": {
          "Message": "$out._id.text",
          "Count": "$out.count"
       }
    },
    {
       "$sort": { "Count": -1 }
    }
 ]

first_said_by_aggregate = [
    {
      "$match": { "name": { "$not": { "$regex": "^streeegg.*" } } }
    },
    {      
        "$group": {
            "_id": {
                "title": "$title",
                "text": { "$toLower": "$message.text" },
                "name": "$name"
            },
            "minDate": { "$min" : "$message.time"  }
            },
    },
    { 
        "$sort": { "minDate" : 1, "_id.name": 1 }
    },
    {
        "$group": {
            "_id": "$_id.text",
            "out": { "$first": "$$ROOT" }
        }
    },
    {
        "$project": {
            "Title": "$out._id.title",
            "Message": "$out._id.text",
            "Name": "$out._id.name",
            "Date": { "$dateToString": { "format": "%Y-%m-%d %H:%M:%S", "date": "$out.minDate"} }
        }
    }
]

first_said_by_message_aggregate = [
    {
      "$match": { "name": { "$not": { "$regex": "^streeegg.*" } } }
    },
    {      
        "$group": {
            "_id": {
                "text": { "$toLower": "$message.text" },
                "name": "$name"
            },
            "minDate": { "$min" : "$message.time"  }
            },
    },
    { 
        "$sort": { "minDate" : 1, "_id.name": 1 }
    },
    {
        "$group": {
            "_id": "$_id.text",
            "out": { "$first": "$$ROOT" }
        }
    },
    {
        "$project": {
            "Message": "$out._id.text",
            "Name": "$out._id.name",
            "Date": { "$dateToString": { "format": "%Y-%m-%d %H:%M:%S", "date": "$out.minDate"} }
        }
    }
]

count_by_video_aggregate = [
  {      
    "$group": {
        "_id": {
          "title": "$title",
          "text": { "$toLower": "$message.text" }
        },
        "agg": { "$addToSet" : "$title"  }
      },
  },
  {
    "$sortByCount": "$_id.title"
  },
  {
      "$project": {
        "Title": "$_id",
        "Count": "$count"
      }
  },
  {
      "$sort": { "Count": -1, "Title": 1}
  }
]

sum_echo_by_title_aggregate = [
    {
      "$group": {
        "_id": {
          "title": "$title",
          "text": { "$toLower": "$message.text" }
        },
        "count": {
          "$sum": {
            "$cond": [
              {
                "$ne": [
                  {
                    "$type": "$message.text"
                  },
                  "missing"
                ]
              }, 1,0]
          }
        }
      }
    },
    {
       "$group": {
          "_id": "$_id.title",
          "out": { "$sum": "$count" }
       }
    },
    {
       "$project": {
          "Title": "$_id",
          "Count": "$out"
       }
    },
    {
       "$sort": { "Count": -1, "Title": 1 }
    }
 ]

video_history_aggregate = [
  {
    "$group":
    {
      "_id": {
        "title": "$title",
        "text": { "$toLower": "$message.text" }
      },
      "minDate": { "$min": "$message.time" }
    }
  },
  { 
    "$group": { 
      "_id": {
        "title": "$_id.title",
        "date": { "$dateToString": { "format": "%Y-%m-%d %H", "date": "$minDate"} }
      },
      "count": { "$sum": 1 } 
    } 
  },
    {
      "$project": {
        "Title": "$_id.title",
        "Date": "$date",
        "Count": "$count"
      }
  },
]

@app.route("/user/top")
def top_users():
    # Who said it first
    first_said = mongo.db.users.aggregate(first_said_by_aggregate)
    # How many times was it said
    count_by_title = mongo.db.users.aggregate(most_echo_by_title_aggregate)

    # DFs for each
    said_df = pd.DataFrame(list(first_said)).sort_values(by=["Date"], ascending=False)
    count_df = pd.DataFrame(list(count_by_title)).sort_values(by=["Count"], ascending=False)
    
    # Merge
    result = said_df.merge(count_df, on=["Message", "Title"]).sort_values(by=["Count"], ascending=False)
    parsed = json.loads(result.to_json(orient="records"))

    return json.dumps(parsed, indent=4)

@app.route("/users")
def users():
    # Who said it first
    first_said = mongo.db.users.aggregate(first_said_by_aggregate)
    # How many times was it said
    count_by_title = mongo.db.users.aggregate(most_echo_by_title_aggregate)

    # DFs for each
    said_df = pd.DataFrame(list(first_said)).sort_values(by=["Date"], ascending=False)
    count_df = pd.DataFrame(list(count_by_title)).sort_values(by=["Count"], ascending=False)
    
    # Merge
    result = said_df.merge(count_df, on=["Message", "Title"]).sort_values(by=["Count"], ascending=False)
    parsed = json.loads(result.to_json(orient="records"))

    return json.dumps(parsed, indent=4)

@app.route("/users/top/real")
def users_topTitle():

    # Who's the best 
    top = Counter(json.loads(users_topMessage())["Count"]).most_common(1)[0][0]

    # What did they say
    what_said = mongo.db.users.aggregate(first_said_by_aggregate + [{"$match": { "Name": top }}])
    
    # How many times did people repeat them
    count_by_title = mongo.db.users.aggregate(most_echo_by_title_aggregate)

    # DFs for each
    said_df = pd.DataFrame(list(what_said)).sort_values(by=["Date"], ascending=False)
    count_df = pd.DataFrame(list(count_by_title)).sort_values(by=["Count"], ascending=False)
    
    # Merge
    result = said_df.merge(count_df, on=["Message", "Title"]).sort_values(by=["Count"], ascending=False)

    return json.dumps(json.loads(result.to_json(orient="records")), indent=4)

@app.route("/users/top/message")
def users_topMessage():
    # Who said it first
    first_said = mongo.db.users.aggregate(first_said_by_message_aggregate)
    # How many times was it said
    count_by_text = mongo.db.users.aggregate(most_echo_by_message_aggregate)

    # DFs for each
    said_df = pd.DataFrame(list(first_said)).sort_values(by=["Date"], ascending=False)
    count_df = pd.DataFrame(list(count_by_text)).sort_values(by=["Count"], ascending=False)
    
    # Merge
    result = said_df.merge(count_df, on=["Message"]).groupby(by=["Name"]).sum().sort_values(by=["Count"], ascending=False).head(20)
    parsed = json.loads(result.to_json(orient="columns"))
    return dumps(parsed)

# Useless?
@app.route("/videos")
def videos():
    return dumps(mongo.db.videos.aggregate(count_by_video_aggregate))

# Videos uses users table lol
@app.route("/videos/top")
def videos_top():
    return dumps(mongo.db.users.aggregate(sum_echo_by_title_aggregate))

@app.route("/videos/history/<name>")
def videos_history(name):
    pipeline = video_history_aggregate + [{"$match": { "Title": name }}] + [{"$sort": { "_id.date": 1}}]
    return dumps(mongo.db.videos.aggregate(pipeline))