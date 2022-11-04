# GoldHole

Parse coolhole and look at shit

# Code Tour

_Long winded mainly to remind myself what the hell I built_

## WebScraper

- Uses playwright
- Grabs data
- Places into two sets (one based on videos and one based on users). Basically useless but whatever.
- Saves the data after each video to `/logs/**Title Of Video**_all.json` and `/logs/**Title Of Video**_users.json` OR if we pass midnight (relic of old code that inferred the date based on the file it was in)
- After the time allotted it up, merge all files into a two "merge" file/day/user or video (again pointless)
- For each of those files, check the latest uploaded date in their respective DB (unnecessary to do multiple times), and insert the files into the two DB
- Purge all the log files

## UI

- Uses Vue 2 with Vueitfy and vue-chartjs (chart.js fork)
  - Hard dep on Vue 2 due to [Vueitfy still working on Vue 3 integration](https://vuetifyjs.com/en/introduction/roadmap/#v30-titan)
  - Would love to try composition API eventually
- Use node

## API / DB

- Uses flask + flask_pymongo to interact with MongoDB
- Uses caching as well
- Aggregate classes are imported at the top and called as needed
- Pandas used to further aggregate subqueries where it was required (where possible, everything was done in the aggregation for performance purposes)
  - Usually not ideal (besides performance) since just using the bare JSON responses from `json.dumps` and `bson.json_util.dumps` which don't match
- DB schema in corresponding readme

# ToDo in order of importance

- [x] Retention policy on scrapped log files
- [ ] Setup automated task for web scraper
  - [ ] Remove usage of FS
  - [ ] Allow for continuous operation
  - [ ] Optimize (possible memory leak? machine tends to lag really bad after allowing to run for a while)
  - [x] Environment variables for secrets
- [ ] Fix UI build size (324.4kB JS chunk and 299.4kB CSS chunk)
- [ ] Resolve UI dep vulnerabilities so depend-a-bot stops complaining
- [ ] Make binned winners (week, month, year, all time)
  - [x] API aggregation for users (day, week, month, all time)
  - [ ] Graphs to reflect with user control over bin
- [ ] 💸Stocks view💸
  - [ ] API aggregation for videos? and gold (binned + any stat cool math)
  - [ ] [Graphs](https://github.com/chartjs/chartjs-chart-financial)
- [ ] [WordCloud](https://github.com/sgratzl/chartjs-chart-wordcloud) to replace stupid radar
- [ ] Parse "gold emojis"
- [x] API Caching
- [ ] UI Caching
- [ ] API Authentication
- [ ] Mock data
- [ ] Unit tests
- [x] Update READMEs
- [ ] Style navbar
- [ ] Style graphs on load
- [ ] Style layout
- [ ] Style style style
- [ ] Organize UI mapping and utilities
- [x] Organize API aggregates better
