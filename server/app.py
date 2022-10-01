from flask import Flask, make_response, request
from bson.json_util import dumps
from bson.son import SON
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
from flask_cors import CORS
from collections import Counter
from dotenv import load_dotenv
from markupsafe import escape
from flask_caching import Cache
from aggregates import (
    MostEchosByTitle,
    MostEchoByMessageAggregate,
    FirstSaidByAggregate,
    FirstSaidByMessageAggregate,
    CountByVideoAggregate,
    SumEchoByTitleAggregate,
    VideoHistoryAggregate,
    Users,
)

import pandas as pd
import pprint
import os
import json

load_dotenv()
config = {
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
}
app = Flask(__name__)
app.config["MONGO_URI"] = os.environ["GH_CONN_STR"]
CORS(app, resources={r"/*": {"origins": "*"}})
mongo = PyMongo(app)
app.config.from_mapping(config)
cache = Cache(app)

## Start Aggregates
most_echo_by_title_aggregate = MostEchosByTitle().agg

most_echo_by_message_aggregate = MostEchoByMessageAggregate().agg

first_said_by_aggregate = FirstSaidByAggregate().agg

first_said_by_message_aggregate = FirstSaidByMessageAggregate().agg

count_by_video_aggregate = CountByVideoAggregate().agg

sum_echo_by_title_aggregate = SumEchoByTitleAggregate().agg

video_history_aggregate = VideoHistoryAggregate().agg

# Wraper for make_response
def success(json):
    return make_response(json, 200, {"Content-Type": "application/json"})


@app.route("/user/top")
@cache.cached(timeout=120)
def top_users():
    # Who said it first
    first_said = mongo.db.users.aggregate(first_said_by_aggregate)
    # How many times was it said
    count_by_title = mongo.db.users.aggregate(most_echo_by_title_aggregate)

    # DFs for each
    said_df = pd.DataFrame(list(first_said)).sort_values(by=["Date"], ascending=False)
    count_df = pd.DataFrame(list(count_by_title)).sort_values(
        by=["Count"], ascending=False
    )

    # Merge
    result = said_df.merge(count_df, on=["Message", "Title"]).sort_values(
        by=["Count"], ascending=False
    )
    parsed = json.loads(result.to_json(orient="records"))

    return success(json.dumps(parsed))


@app.route("/users")
@cache.cached(timeout=120)
def users():
    # Who said it first
    first_said = mongo.db.users.aggregate(first_said_by_aggregate)
    # How many times was it said
    count_by_title = mongo.db.users.aggregate(most_echo_by_title_aggregate)

    # DFs for each
    said_df = pd.DataFrame(list(first_said)).sort_values(by=["Date"], ascending=False)
    count_df = pd.DataFrame(list(count_by_title)).sort_values(
        by=["Count"], ascending=False
    )

    # Merge
    result = said_df.merge(count_df, on=["Message", "Title"]).sort_values(
        by=["Count"], ascending=False
    )
    parsed = json.loads(result.to_json(orient="records"))

    return success(json.dumps(parsed))


@app.route("/users/top/real")
@cache.cached(timeout=120)
def users_topTitle():

    # Who's the best
    top = Counter(json.loads(users_topMessage())["Count"]).most_common(1)[0][0]

    # What did they say
    what_said = mongo.db.users.aggregate(
        first_said_by_aggregate + [{"$match": {"Name": top}}]
    )

    # How many times did people repeat them
    count_by_title = mongo.db.users.aggregate(most_echo_by_title_aggregate)

    # DFs for each
    said_df = pd.DataFrame(list(what_said)).sort_values(by=["Date"], ascending=False)
    count_df = pd.DataFrame(list(count_by_title)).sort_values(
        by=["Count"], ascending=False
    )

    # Merge
    result = said_df.merge(count_df, on=["Message", "Title"]).sort_values(
        by=["Count"], ascending=False
    )

    return success(json.loads(result.to_json(orient="records")))


@app.route("/users/top/message")
@cache.cached(timeout=120)
def users_topMessage():
    # Who said it first
    first_said = mongo.db.users.aggregate(first_said_by_message_aggregate)
    # How many times was it said
    count_by_text = mongo.db.users.aggregate(most_echo_by_message_aggregate)

    # DFs for each
    said_df = pd.DataFrame(list(first_said)).sort_values(by=["Date"], ascending=False)
    count_df = pd.DataFrame(list(count_by_text)).sort_values(
        by=["Count"], ascending=False
    )

    # Merge
    result = (
        said_df.merge(count_df, on=["Message"])
        .groupby(by=["Name"])
        .sum()
        .sort_values(by=["Count"], ascending=False)
        .head(20)
    )
    parsed = json.loads(result.to_json(orient="columns"))
    return success(dumps(parsed))


# Useless?
@app.route("/videos")
@cache.cached(timeout=120)
def videos():
    return success(dumps(mongo.db.videos.aggregate(count_by_video_aggregate)))


# Videos uses users table lol
@app.route("/videos/top")
@cache.cached(timeout=120)
def videos_top():
    return success(dumps(mongo.db.users.aggregate(sum_echo_by_title_aggregate)))


@app.route("/videos/history/<name>")
@cache.memoize(120)
def videos_history(name):
    pipeline = (
        video_history_aggregate
        + [{"$match": {"Title": name}}]
        + [{"$sort": {"_id.date": 1}}]
    )
    return success(dumps(mongo.db.videos.aggregate(pipeline)))


@app.route("/test/users")
@cache.cached(timeout=120, query_string=True)
def test():
    date_bin = request.args.get("date_bin") or "ALLTIME"
    top_users_obj = list(mongo.db.users.aggregate(Users().getWinnersArray(date_bin)))

    response = success(
        dumps(
            mongo.db.users.aggregate(
                Users().winnersFavorByDate(top_users_obj[0]["names"], date_bin)
            )
        )
    )
    return response
