# GoldHole

Parse coolhole and look at shit

# Code Tour

## WebScraper

- Uses playwright
- Grabs data
- Places into two sets (one based on videos and one based on users). Basically useless but whatever.
- Saves the data after each video to `/logs/**Title Of Video**_all.json` and `/logs/**Title Of Video**_users.json` OR if we pass midnight (relic of old code that inferred the date based on the file it was in)
- After the time allotted it up, merge all files into a two "merge" file/day/user or video (again pointless)
- For each of those files, check the latest uploaded date in their respective DB (unnecessary to do multiple times), and insert the files into the two DB
- Purge all the log files

## UI

## API / DB

# ToDo in order of importance

- [x] Retention policy on scrapped log files
- [x] Setup automated task for web scraper (nearly)
- [ ] Fix UI build size (324.4kB JS chunk and 299.4kB CSS chunk)
- [ ] Make binned winners (week, month, year, all time)
- [ ] 💸Stocks view💸
- [ ] [WordCloud](https://github.com/sgratzl/chartjs-chart-wordcloud)
- [ ] Parse "gold emojis" (blank)
- [x] API Caching
- [ ] UI Caching
- [ ] API Authentication
- [ ] Unit tests
- [ ] Mock data
- [ ] Style navbar
- [ ] Style graphs on load
- [ ] Style layout
- [ ] Style style style
- [ ] Organize UI mapping and utilities
- [x] Organize API aggregates better
