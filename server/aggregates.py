## Duuno what the "proper" pattern is for aggregates or if these are the most optimal aggregates
## Going to create classes with different pipelines that build off of one another
## Pipelines that are static (no variables/only rely off of another static) are attributes
## Pipelines that are dynamic (need some input) are methods

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from enum import Enum

"""TODO: Novel incoming...
This implementation has its issues like:
 - pipeline ordering isn't enforced  
    + one could easily shoot themselves in the foot if some aggregates /need/ to be ran first (none in this but could be in the future)
    + https://www.mongodb.com/docs/manual/reference/operator/aggregation/match/#restrictions
 - a lot was written in the mindset of "build on previous aggregation"
    + with a stronger background in SQL, I'm used to the mindset of piping results into other queries instead of building one monolith
    + this approach attempts to mimic that though albiet awkwardly with specific return fields to accomedate
    + perhaps could be solved with some generic "adapter" to build out a project string to fit a subqueries need?
- no model enforcement
    + would be wayyy easier to know what the hell I'm developing if I were running multiple queries, mapping each to a model, and then aggregating further
"""

"""TODO: Clean up unused shit """


class EchosBinnedByDate:
    def __init__(self):
        self.agg = [
            {"$match": {"name": {"$not": {"$regex": "^streeegg.*"}}}},
            {
                "$group": {
                    "_id": {"text": {"$toLower": "$message.text"}, "name": "$name"},
                    "minDate": {"$min": "$message.time"},
                },
            },
            {"$sort": {"minDate": 1, "_id.name": 1}},
            {"$group": {"_id": "$_id.text", "out": {"$first": "$$ROOT"}}},
            {
                "$project": {
                    "name": "$out._id.name",
                    "date": "$out.minDate",
                    "text": "$out._id.text",
                }
            },
            {
                "$group": {
                    "_id": {
                        "user": "$name",
                        "month": {
                            "$dateToString": {"format": "%Y-%m", "date": "$date"}
                        },
                    },
                    "items": {"$push": "$text"},
                }
            },
            {
                "$project": {
                    "user": "$_id.user",
                    "month": "$_id.month",
                    "items": {"$setUnion": ["$items", "$items"]},
                }
            },
            {
                "$project": {
                    "user": "$_id.user",
                    "month": "$_id.month",
                    "items": "$items",
                    "count": {"$size": "$items"},
                }
            },
            {"$sort": {"count": -1, "user": 1}},
        ]


class MostEchosByTitle:
    def __init__(self):
        self.agg = [
            {
                "$group": {
                    "_id": {"title": "$title", "text": {"$toLower": "$message.text"}},
                    "count": {
                        "$sum": {
                            "$cond": [
                                {"$ne": [{"$type": "$message.text"}, "missing"]},
                                1,
                                0,
                            ]
                        }
                    },
                }
            },
            {"$group": {"_id": "$_id", "out": {"$sum": "$count"}}},
            {
                "$project": {
                    "Title": "$_id.title",
                    "Message": "$_id.text",
                    "Count": "$out",
                }
            },
            {"$sort": {"Count": -1}},
        ]


class MostEchoByMessageAggregate:
    def __init__(self):
        self.agg = [
            {
                "$group": {
                    "_id": {"text": {"$toLower": "$message.text"}},
                    "count": {
                        "$sum": {
                            "$cond": [
                                {"$ne": [{"$type": "$message.text"}, "missing"]},
                                1,
                                0,
                            ]
                        }
                    },
                }
            },
            {"$sort": {"count": -1, "_id.text": 1}},
            {"$group": {"_id": "$_id.text", "out": {"$first": "$$ROOT"}}},
            {"$project": {"Message": "$out._id.text", "Count": "$out.count"}},
            {"$sort": {"Count": -1}},
        ]


class FirstSaidByAggregate:
    def __init__(self):
        self.agg = [
            {"$match": {"name": {"$not": {"$regex": "^streeegg.*"}}}},
            {
                "$group": {
                    "_id": {
                        "title": "$title",
                        "text": {"$toLower": "$message.text"},
                        "name": "$name",
                    },
                    "minDate": {"$min": "$message.time"},
                },
            },
            {"$sort": {"minDate": 1, "_id.name": 1}},
            {"$group": {"_id": "$_id.text", "out": {"$first": "$$ROOT"}}},
            {
                "$project": {
                    "Title": "$out._id.title",
                    "Message": "$out._id.text",
                    "Name": "$out._id.name",
                    "Date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d %H:%M:%S",
                            "date": "$out.minDate",
                        }
                    },
                }
            },
        ]


class FirstSaidByMessageAggregate:
    def __init__(self):
        self.agg = [
            {"$match": {"name": {"$not": {"$regex": "^streeegg.*"}}}},
            {
                "$group": {
                    "_id": {"text": {"$toLower": "$message.text"}, "name": "$name"},
                    "minDate": {"$min": "$message.time"},
                },
            },
            {"$sort": {"minDate": 1, "_id.name": 1}},
            {"$group": {"_id": "$_id.text", "out": {"$first": "$$ROOT"}}},
            {
                "$project": {
                    "Message": "$out._id.text",
                    "Name": "$out._id.name",
                    "Date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d %H:%M:%S",
                            "date": "$out.minDate",
                        }
                    },
                }
            },
        ]


class CountByVideoAggregate:
    def __init__(self):
        self.agg = [
            {
                "$group": {
                    "_id": {"title": "$title", "text": {"$toLower": "$message.text"}},
                    "agg": {"$addToSet": "$title"},
                },
            },
            {"$sortByCount": "$_id.title"},
            {"$project": {"Title": "$_id", "Count": "$count"}},
            {"$sort": {"Count": -1, "Title": 1}},
        ]


class SumEchoByTitleAggregate:
    def __init__(self):
        self.agg = [
            {
                "$group": {
                    "_id": {"title": "$title", "text": {"$toLower": "$message.text"}},
                    "count": {
                        "$sum": {
                            "$cond": [
                                {"$ne": [{"$type": "$message.text"}, "missing"]},
                                1,
                                0,
                            ]
                        }
                    },
                }
            },
            {"$group": {"_id": "$_id.title", "out": {"$sum": "$count"}}},
            {"$project": {"Title": "$_id", "Count": "$out"}},
            {"$sort": {"Count": -1, "Title": 1}},
        ]


class VideoHistoryAggregate:
    def __init__(self):
        self.agg = [
            {
                "$group": {
                    "_id": {"title": "$title", "text": {"$toLower": "$message.text"}},
                    "minDate": {"$min": "$message.time"},
                }
            },
            {
                "$group": {
                    "_id": {
                        "title": "$_id.title",
                        "date": {
                            "$dateToString": {
                                "format": "%Y-%m-%d %H",
                                "date": "$minDate",
                            }
                        },
                    },
                    "count": {"$sum": 1},
                }
            },
            {"$project": {"Title": "$_id.title", "Date": "$date", "Count": "$count"}},
        ]


class DateBins(Enum):
    """Laughably bad date conversions. Just ignore it for now..."""

    WEEK = [
        "%Y-%m-%d %w",
        datetime.combine(
            date.today() - timedelta(days=date.today().isoweekday() % 7),
            datetime.min.time(),
        ),
    ]
    MONTH = [
        "%Y-%m-%d",
        datetime.combine(date.today().replace(day=1), datetime.min.time()),
    ]
    YEAR = ["%Y-%m", datetime(date.today().year, 1, 1)]
    # Hard deadline of 5 years b/c fk u
    ALLTIME = ["%Y-%m", datetime(date.today().year - 5, 1, 1)]


class Users:
    """
    User aggregation methods used to determine who "owns" a gold (first said) and how many times unique users have echoed said gold
    """

    # Must be first in any pipelines that use it!
    excludeCheaters = [{"$match": {"name": {"$not": {"$regex": "^streeegg.*"}}}}]

    winnersAggregateByMessage = [
        *excludeCheaters,
        # Get all unique messages per title+user and their earliest date
        {
            "$group": {
                "_id": {
                    "text": {"$toLower": "$message.text"},
                    "name": "$name",
                    "title": "$title",
                },
                "minDate": {"$min": "$message.time"},
            },
        },
        # Need to sort by date (tie breaker on name) the next stage...
        {"$sort": {"minDate": 1, "_id.name": 1}},
        # Grab first record to see who got it first and push all other "unique repeated" dates in an array
        {
            "$group": {
                "_id": "$_id.text",
                "out": {"$first": "$$ROOT"},
                "allDatesSaidUniqueToUserAndTitle": {"$push": "$minDate"},
            }
        },
        # Project to pull values out of objects
        {
            "$project": {
                "name": "$out._id.name",
                "date": "$out.minDate",
                "text": "$out._id.text",
                "allDatesSaidUniqueToUserAndTitle": "$allDatesSaidUniqueToUserAndTitle",
            }
        },
        # Size of the array = how many people said it
        {"$addFields": {"totalEcho": {"$size": "$allDatesSaidUniqueToUserAndTitle"}}},
    ]

    # Condense the result and sort to make it easier to parse for winners later
    usersFavorOrdered = [
        *winnersAggregateByMessage,
        {"$group": {"_id": {"name": "$name"}, "favor": {"$sum": "$totalEcho"}}},
        {"$project": {"_id": False, "name": "$_id.name", "favor": "$favor"}},
        {"$sort": {"favor": -1, "name": 1}},
    ]

    def getWinnersArray(self, dateBin, limit=3):
        """
        Expensively* determines the top users given a limit and returns an array
        *requires going through the whole pipeline plus an additional aggregate to reduce/sum the count
        use with care

        Parameters
        ---------
        dateBin : string enum DateBins
            which grouping of dates you want to search over
        limit : int, optional
            top winners
        """

        if hasattr(DateBins, dateBin):
            format_string = DateBins[dateBin].value[0]
            date_from = DateBins[dateBin].value[1]
            date_to = datetime.today()
        else:
            raise ValueError(f"Provided dateBin {dateBin} isn't an accept value")

        return [
            {
                "$match": {
                    "message.time": {
                        "$gte": date_from,
                        "$lte": date_to,
                    }
                }
            },
            *self.usersFavorOrdered,
            {"$limit": limit},
            {"$project": {"_id": False, "name": "$_id.name", "favor": True}},
        ]

    def winnersFavorByDate(self, winners, dateBin):
        """
        Gather number of golds for given winners binned per date given

        Parameters
        ----------
        winners : list(string)
            list of users we want to search for
        dateBin : enum DateBins
            which grouping of dates you want to search over
        """
        if hasattr(DateBins, dateBin):
            format_string = DateBins[dateBin].value[0]
            date_from = DateBins[dateBin].value[1]
            date_to = datetime.today()
        else:
            raise ValueError(f"Provided dateBin {dateBin} isn't an accept value")

        if not winners:
            raise ValueError("Winners list cannot be empty")

        return [
            {
                "$match": {
                    "message.time": {
                        "$gte": date_from,
                        "$lte": date_to,
                    }
                }
            },
            *self.winnersAggregateByMessage,
            {"$match": {"$expr": {"$in": ["$name", winners]}}},
            {"$unwind": "$allEchosWithDates"},
            {"$unwind": "$allEchosWithDates.allDatesSaidUniqueToUserAndTitle"},
            {
                "$group": {
                    "_id": {
                        "user": "$name",
                        "bin": {
                            "$dateToString": {
                                "format": format_string,
                                "date": "$allEchosWithDates.allDatesSaidUniqueToUserAndTitle",
                            }
                        },
                    },
                    "items": {"$push": "$text"},
                }
            },
            {
                "$project": {
                    "_id": False,
                    "user": "$_id.user",
                    "bin": "$_id.bin",
                    "messages": {"$setUnion": ["$items", "$items"]},
                    "totalEchoCount": {"$size": "$items"},
                }
            },
            {"$sort": {"bin": 1, "count": -1, "name": 1}},
        ]
