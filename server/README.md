# goldhole API

## Setup

- Create an `.env` file based on the sample provided for the mongoDb conn string
- `waitress-serve --listen=*:5000 app:app`

## DB

- BYO Database
- TODO item to write a small script to generate bogus data based on schema and to use environment variables instead of config files
- For now, setup a DB with the name `gold_hole` and collections `users` and `videos`
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
