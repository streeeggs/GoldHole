from datetime import date, datetime
import os
import json
import pprint
import shutil

from mongo_util import get_database

# FIXME: THIS WHOLE THING SUCKS SHIT
# FIXME: AHHHHHHHH PATHS
path = os.getcwd() + "/logs"

# Dunno if this is the most efficient approach but also don't care
# https://stackoverflow.com/questions/57422734/how-to-merge-multiple-json-files-into-one-file-in-python

# Creates two files with the "_MERGE.json" file name on each date sub-folder that merges all files together.
# One file for users; one for "all" (title + date)
def merge_all_logs():
    # Each date
    for root_path, dirs, files in os.walk(path):
        # Verbose names are all you can think of past 11PM
        list_of_all_files, list_of_user_files = list(), list()

        # Sub-dirs only
        if path != root_path:
            # Each file for that day
            for file in files:
                day = root_path.split(path)[1].strip("\\")
                with open(root_path + "/" + file, "r", encoding="utf8") as infile:
                    if file.endswith("_all.json"):
                        data = json.load(infile)
                        list_of_all_files.extend(cleanData(data))
                    elif file.endswith("_user.json"):
                        data = json.load(infile)
                        list_of_user_files.extend(cleanData(data))

        if list_of_all_files and list_of_user_files:
            with open(
                path + "/" + day + "_all_MERGE.json", "w", encoding="utf8"
            ) as output_file:
                json.dump(list_of_all_files, output_file, ensure_ascii=False, indent=4)
                print(f"Finished writing {path + '/' + day + '_all_MERGE.json'}")

            with open(
                path + "/" + day + "_user_MERGE.json", "w", encoding="utf8"
            ) as output_file:
                json.dump(list_of_user_files, output_file, ensure_ascii=False, indent=4)
                print(f"Finished writing {path + '/' + day + '_user_MERGE.json'}")

            updateGoldCollections(list_of_all_files, list_of_user_files)


def cleanData(data):
    for message in data:
        if type(message["message"]) is not dict and message["message"]:
            message["message"] = {
                "time": message["message"][0],
                "text": message["message"][1],
            }
        elif type(message["message"]) is dict:
            message["message"]["time"] = message["message"]["time"]

    return data


def updateGoldCollections(list_of_gold_by_title, list_of_gold_by_user):
    db = get_database("gold_hole")

    for title in list_of_gold_by_title:
        title["message"]["time"] = datetime.strptime(
            title["message"]["time"], "%Y-%m-%d %H:%M:%S"
        )

    for user in list_of_gold_by_user:
        user["message"]["time"] = datetime.strptime(
            user["message"]["time"], "%Y-%m-%d %H:%M:%S"
        )

    videos = db.videos
    videos.insert_many(list_of_gold_by_title)
    print(
        f"Finished inserting video records into collection for {list_of_gold_by_title[0]}"
    )

    users = db.users
    users.insert_many(list_of_gold_by_user)
    print(
        f"Finished inserting user records into collection for {list_of_gold_by_user[0]}"
    )


def pergeLogs():
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error purging files: %s : %s" % (path, e.strerror))
