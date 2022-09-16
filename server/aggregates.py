class MostEchosByTitle:
    def __init__(self):
        self.agg = [
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

class MostEchoByMessageAggregate:
    def __init__(self):
        self.agg = [
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

class FirstSaidByAggregate:
    def __init__(self):
        self.agg = [
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

class FirstSaidByMessageAggregate:
    def __init__(self):
        self.agg = [
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

class CountByVideoAggregate:
    def __init__(self):
        self.agg = [
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

class SumEchoByTitleAggregate:
    def __init__(self):
        self.agg = [
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

class VideoHistoryAggregate:
    def __init__(self):
        self.agg = [
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