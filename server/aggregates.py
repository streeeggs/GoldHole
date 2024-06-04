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
        "%Y-%m-%d",
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


class Users:
    """
    User aggregation methods used to determine who "owns" a gold (first said) and how many times unique users have echoed said gold
    """

    # Must be first in any pipelines that use it!
    excludeCheaters = [{"$match": {"name": {"$not": {"$regex": "^streeegg.*"}}}}]

    # TODO: Move/marry logic in to FirstSaidAggregate
    def messageStatsBinned(self, dateBin):
        if hasattr(DateBins, dateBin):
            format_string = DateBins[dateBin].value[0]
            date_from = DateBins[dateBin].value[1]
            date_to = datetime.today()
        else:
            raise ValueError(f"Provided dateBin {dateBin} isn't an accept value")

        return [
            *self.excludeCheaters,
            {
                "$match": {
                    "message.time": {
                        "$gte": date_from,
                        "$lte": date_to,
                    }
                }
            },
            # Get all unique messages per title+user and their earliest date
            {
                "$group": {
                    "_id": {
                        "text": {"$toLower": "$message.text"},
                        "name": "$name",
                        "title": "$title",
                    },
                    "minDate": {"$min": "$message.time"},
                }
            },
            # Need to sort so we can get first message
            {"$sort": {"minDate": 1, "_id.name": 1}},
            # Aggregate by who first said the message and push each time the message was repeated to an array. Bin each date added too
            {
                "$group": {
                    "_id": {
                        "text": "$_id.text",
                        "title": "$_id.title",
                    },
                    "first": {"$first": "$$ROOT"},
                    "whoFollowed": {
                        "$push": {
                            "text": "$_id.text",
                            "name": "$_id.name",
                            "title": "$_id.title",
                            "date": {
                                "$dateToString": {
                                    "format": format_string,
                                    "date": "$minDate",
                                }
                            },
                        }
                    },
                }
            },
        ]

    def winnersFavorByDate(self, dateBin, limit=3):
        """
        Gather all messages "owned" ordered by those with the most messages

        Parameters
        ----------
        dateBin : enum DateBins
            which grouping of dates you want to search over

        limit : int
            total number of users to return
        """

        return [
            *self.messageStatsBinned(dateBin),
            # Group by user and push the details of who followed them to an array
            {
                "$group": {
                    "_id": {"user": "$first._id.name"},
                    "messages": {
                        "$push": {
                            "message": "$_id.text",
                            "title": "$_id.title",
                            "details": "$whoFollowed",
                            "favorEarned": {"$size": "$whoFollowed"},
                        }
                    },
                }
            },
            # Not sure if it's faster/slower but seemed little nicer than "$size": "$messages.details" idk tired
            {"$addFields": {"totalFavor": {"$sum": "$messages.favorEarned"}}},
            {"$sort": {"totalFavor": -1, "name": 1}},
            {"$limit": limit},
            {
                "$facet": {
                    "totals": [
                        {
                            "$project": {
                                "_id": False,
                                "name": "$_id.user",
                                "messages": "$messages",
                                "totalFavor": "$totalFavor",
                            }
                        },
                    ],
                    # TODO: Find a way to consolidate this into the above query instead of needing a seperate group for this
                    # Issue is because we focus on the message text to get who said it first
                    # Directly conflicts with grouping by date and user alone
                    # hate this shit
                    "perdate": [
                        {"$unwind": "$messages"},
                        {"$project": {"details": "$messages.details"}},
                        {"$unwind": "$details"},
                        {
                            "$group": {
                                "_id": {"date": "$details.date", "user": "$_id.user"},
                                "favor": {"$sum": 1},
                            }
                        },
                        {
                            "$group": {
                                "_id": {"user": "$_id.user"},
                                "dates": {
                                    "$push": {"date": "$_id.date", "favor": "$favor"}
                                },
                            }
                        },
                        {
                            "$project": {
                                "_id": False,
                                "user": "$_id.user",
                                "dates": "$dates",
                                "totalFavor": {"$sum": "$dates.favor"},
                            }
                        },
                        {"$sort": {"totalFavor": -1}},
                    ],
                }
            },
        ]

    def favorPerUser(self, dateBin):
        """
        Gather the count per user

        Parameters
        ----------
        dateBin : enum DateBins
            which grouping of dates you want to search over
        """

        return [
            *self.messageStatsBinned(dateBin),
            # Group by user and sum the lenght of messages they own
            {
                "$group": {
                    "_id": {"user": "$first._id.name"},
                    "totalFavor": {"$sum": {"$size": "$whoFollowed"}},
                }
            },
            {"$sort": {"totalFavor": -1, "_id.user": 1}},
            {"$project": {"_id": False, "user": "$_id.user", "totalFavor": 1}},
        ]

    # TODO: Create own class for messages and move this there (only here b/c messageStatsBinned isn't a common function)
    def messageList(self, dateBin):
        """
        Gather thin information per message

        Parameters
        ----------
        dateBin : enum DateBins
            which grouping of dates you want to search over
        """

        return [
            *self.messageStatsBinned(dateBin),
            {
                "$project": {
                    "_id": False,
                    "user": "$first._id.name",
                    "message": "$first._id.text",
                    "title": "$first._id.title",
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d %H:%M:%S",
                            "date": "$first.minDate",
                        }
                    },
                    "favor": {"$size": "$whoFollowed"},
                }
            },
            {"$sort": {"favor": -1, "user": 1}},
        ]
