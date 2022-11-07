# goldhole API

## Setup

- `python -m venv env`
- Locate appropriate active script in `Scripts`. (eg: `env\Scripts\activate.bat` for CMD or `env\Scripts\Activate.ps1` for PowerShell)
- `pip install -r requirements.txt`
- Copy `.env.sample`, name it `.env` and update the fields as needed
- `waitress-serve --port=5000 app:app`
  - Using `waitress` since no `guinicorn` support on Windows
  - `waitress` has no hot reload like gunicorn does (couldn't get `hupper` to work as suggested on [SO](https://stackoverflow.com/questions/36817604/how-to-change-and-reload-python-code-in-waitress-without-restarting-the-server))

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

## Debug Advice

Dunno what the "proper" approach here would be. Likely getting `waitress` to cooperate with VSCodium in loading debug symbols or something but even then, debugging DB aggregates is what's more valuable. Symbols won't help much there. Typical a debugging works like this:

1. Print out the resulting aggregate in console
2. Open up `aggs.mongodb` and paste the result in
3. Trial and error via `db.table_name.aggregate(` until it works
4. Usually fight to convert the syntax back to Python (I know the extension allows for exporting to python3 but usually fails on things like dates)
5. Likely more debugging in app due to baked in record limits on the extension

If you know of a better process, please let me know.
