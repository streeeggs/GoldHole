# GoldHole

Parse coolhole and look at shit

# Code Tour

## WebScraper

## API

## UI

# Setup

_Still WIP. Without using the exact DB I'm using which is currently an Atlas Cluster_

## UI

- Follow readme

## DB

- Still in TODO
- If you want to give it a go, setup a DB with the name `gold_hole` and collections `users` and `videos`
- `users` schema:

```json
{
  "_id": { "$oid": "objectID" },
  "title": "Title",
  "name": "Name",
  "message": {
    "time": { "$date": { "$numberLong": "1111111111111" } },
    "text": "text"
  }
}
```

- `videos` schema:

```json
{
  "_id": { "$oid": "objectID" },
  "title": "Title",
  "message": {
    "time": { "$date": { "$numberLong": "1111111111111" } },
    "text": "text"
  }
}
```

## API

- Create an `.ini` file based on the sample provided for the mongoDb conn string
- `python app.py`

## WebScraper

- Create an `.ini` file based on the sample provided for the mongoDb conn string
- `python get_gold.py`

# ToDo in order of importance

- [~] 💸Stocks view💸
- [ ] API Caching
- [ ] API Auth
- [ ] Retention policy on log files
- [ ] Unit tests
- [ ] Mock data
- [ ] Style nav
- [ ] Style graphs on load
- [ ] Style layout
- [ ] Style style style
- [ ] Organize UI mapping and utils
- [ ] Organize API aggregates better
