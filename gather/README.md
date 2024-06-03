# goldhole web scraper

## Setup

- `python -m venv env`
- Locate appropriate active script in `Scripts`. (eg: `env\Scripts\activate.bat` for CMD or `env\Scripts\Activate.ps1` for PowerShell)
- `pip install -r requirements.txt`
- Copy `.env.sample`, name it `.env` and update the fields as needed
- `python app.py`

## What it does

- Uses playwright
- Grabs data
- Places into two sets (one based on videos and one based on users). Basically useless but whatever.
- Saves the data after each video to `/logs/**Title Of Video**_all.json` and `/logs/**Title Of Video**_users.json` OR if we pass midnight (relic of old code that inferred the date based on the file it was in)
- After the time allotted it up, merge all files into a two "merge" file/day/user or video (again pointless)
- For each of those files, check the latest uploaded date in their respective DB (unnecessary to do multiple times), and insert the files into the two DB
- Purge all the log files
