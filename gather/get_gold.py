import re
import json
import time
import os
import string
import traceback

from datetime import datetime, timedelta, date
from os.path import exists
from playwright.sync_api import sync_playwright

from cool_js import cool_js
from merge_data import merge_all_logs

# Test
#URL =  "https://coolhole.org/r/test"

# Prod
URL = "https://coolhole.org/"

TIME_TILL_KILL = 12

# FIXME: Custom JS needs to be loaded in. Logging in does nothing. Need to diagnose. Could try:
# 1. Waiting for chanjs to load (may never happen if websocket fucks off)
# 2. Try different browser options (issue seen in non-headless webkit and chromium)
# 3. Ignore it, just ask if the script changed and grab it manually
lottery_js = cool_js()

def buildFiles(results):
    """
    Given an array of results from main scraping function, build JSON files and parent folder.
    Used to reduce memory pressure and prep for DB transfer
    """

    # TODO: quit relying off of position; use a class
    users_results = results[0]
    video_results = results[1]
    raw_title = str(results[2])

    # Build title string; need to sanitize characters before saving 
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits) # '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    title = str(''.join(c for c in raw_title if c in valid_chars))
    
    # ick; path requirement
    path = "logs/" + str(date.today())
    if not os.path.exists(path):
        os.makedirs(path)

    user_filename = str(title + "_user.json")
    addFile(results[0], user_filename, path)

    video_filename = str(title + "_all.json")
    addFile(results[1], video_filename, path)


def addFile(result, fileName, path):
        """Given a result and file name, determine if file already exists. If it does, append to what's already there"""
        
        if exists(os.path.join(path, str(fileName))):
            with open(os.path.join(path, str(fileName)), 'r', encoding ='utf8', errors='ignore') as old_json:    
                # TODO: Gotta be a better way... feels really wasteful
                # https://stackoverflow.com/questions/57422734/how-to-merge-multiple-json-files-into-one-file-in-python
                old_dict = json.load(old_json)
                result.extend(old_dict)

        with open(os.path.join(path, str(fileName)), 'w', encoding ='utf8', errors='ignore') as json_file:
            json.dump(result, json_file, ensure_ascii = False, indent = 4)

def parseUserMessage(html):
    """Given some HTML, return a tuple of message, username, and timestamp"""

    # FIXME: Lotta reliance on structure and not names/ids; returns [time, text, name]
    # Could maybe use some cleverness with locators and getting attrs/ids from that? (first text w/o a name?)
    ''' 
    HTML comes in two flavors:
        - <div class="chat-msg-user_name" title="[18:49:07] user_name: message">
            <span class="timestamp" data-text="message">[23:59:99] </span>
            <span data-text="message">
                <strong class="username">user_name: </strong>
            </span>
            <span class="text-lottery" data-text="message">message</span>
        </div>
        - <div class="chat-msg-user_name" title="[23:59:99] message">
            <span class="timestamp" data-text="message">[23:59:99] </span>
            <span class="text-lottery" data-text="message">message</span>
        </div>
    '''
    try:
        # Time for regex
        
        # Get username
        username_class = re.search("class\=\"chat-msg-[\-\w\u00c0-\u00ff]{1,20}[\"|\s]", html).group(0) # class="chat-msg-user_name"
        username = username_class.split("-")[-1].strip(r'\"').strip()

        # Get timestamp
        #timestamp = re.search("\[\d{2}\:\d{2}\:\d{2}\]", html).group(0) # [23:59:99] (will probably pull from title)
        timestamp = "{0} {1}".format(str(date.today()), re.search("\[\d{2}\:\d{2}\:\d{2}\]", html).group(0).strip("[").strip("]")) # [23:59:59] (will probably pull from title) -> 1900-01-01 23:59:59

        # Get message
        data_text = re.search("data-text=\".+\">", html.split("</span>")[0]).group(0) # data-text="message"> (need the closing bracket to gaurentee I've selected the whole message)
        message = data_text.split("=")[1].split('"')[1] # Alternatively, I could have removed data-text= and > then i could just strip('"')

        return (timestamp, username, message)
    except Exception:
        print(f"Failed to parse {html}")
        print("-"*60)
        traceback.print_exc()
        print("-"*60)


# Goal: Gather "quality" metrics on golds. 
# Philosophy: Uniqueness implies "quality" between users (more repetitions, more value). Uniqueness impleis "quality" between videos (less likely ergo more valuable)
# Returns two sets: golds by user, title, and date and golds by title and date
def get_gold(lottery_js):

    try:
        # Locators
        whole_gold = page.locator("#messagebuffer div:has(.text-lottery)")
        timestamp_gold = page.locator("#messagebuffer div:has(.text-lottery) >> .timestamp")
        message_gold = page.locator("#messagebuffer div:has(.text-lottery) >> .text-lottery")
        name_gold = page.locator("#messagebuffer div:has(.text-lottery) >> .username")
        #white_hunting = page.locator("#messagebuffer span")

        # Even with login, still cant get usually JS
        page.evaluate(lottery_js)

        title = page.locator("#currenttitle-content")
        
        unique_golds_by_user, unique_golds_global = set(), set()

        # INCREDIBLY unsafe but idfc lmao
        # Delete vid b/c bandwith aint free
        video = page.locator(".embed-responsive")
        try:
            video.element_handle(timeout=1000).evaluate("el => el.remove()")
        except:
            print("Vid May have already been deleted, move on")

    except Exception:
        print("Exception during locators/setup")
        print("-"*60)
        traceback.print_exc()
        print("-"*60)
        return(None)

    # Have to do my own waiting for this title to appear
    # FIXME: Dangerous; put a timer on this
    title_text_origin = title.all_inner_texts()
    while not title_text_origin:
        title_text_origin = title.all_inner_texts()

    title_text_origin = title_text_origin[0]
    title_text_current = title_text_origin

    # FIXME: Use different invariant to find out if the video is over since this screws up logging if a video is the last in the queue (possible "infinite" loop)
    while title_text_current == title_text_origin:
        time.sleep(5)

        # HACK: If we're nearly past midnight, build the files to avoid having logs with the wrong dates on them
        if datetime.today() + timedelta(minutes=2) > datetime.combine(date.today(), datetime.max.time()):
            break

        # messages: gets time stamp and text eg: ['[23:39:02]', 'better']]
        whole_gold_text = whole_gold.all_text_contents()

        ## Add to the list

        count = whole_gold.count()
        gold_list = list()
        # Start from the last gold message and remove on the way up to keep the "i-th" ordering in place
        for i in reversed(range(count)):
            try:
                html = whole_gold.nth(i).evaluate("el => el.outerHTML")
                whole_gold.nth(i).evaluate("el => el.remove()")
                gold_list.append(parseUserMessage(html))
            except Exception:
                # ignore... usually timeout related and worth giving it another try next round
                print(f"Exception while gather inner html for {i}th element")
                print("-"*60)
                traceback.print_exc()
                print("-"*60)
                
        # gold: (timestamp, username, message) 
        for gold in gold_list:
            # FIXME: Intention was to use sets to avoid duplciates. 
            # However, with a timestamp involved, each record will always be unique thus making a set useless here
            unique_golds_by_user.add((title_text_current, gold[0], gold[1], gold[2]))
            unique_golds_global.add((title_text_current, gold[0], gold[2]))
            print(unique_golds_by_user, unique_golds_global)

        # Can sometimes grab title before it renders
        if(title.all_inner_texts()[0]):
            title_text_current = title.all_inner_texts()[0]


    if(unique_golds_by_user and unique_golds_global):
        # TODO: Confusing names and probably unnecessary composition
        user_array = [{"title": gold[0], "name": gold[2], "message": {"time": gold[1], "text": gold[3]}} for gold in unique_golds_by_user]
        video_array = [{"title": gold[0], "message": {"time": gold[1], "text": gold[2]}} for gold in unique_golds_global]
        return(user_array, video_array, title_text_origin)
    else:
        return(None)

if __name__ == "__main__":
    with sync_playwright() as p:

        target_time = datetime.now() + timedelta(hours=TIME_TILL_KILL)

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        #context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = browser.new_page()
        page.goto(URL, timeout=300000)

        # Login for channel JS and CSS
        page.fill("#username", "gold_minor")
        page.fill("#password", "Password1")
        page.click("#login")

        script_prompt = page.locator("#chanjs-allow")
        # Please let me get the gold script... please
        script_prompt.click()
        
        while target_time > datetime.now():

            # Need to pass lottery_js since websocket isn't sending it over
            res = get_gold(lottery_js) # returns (user_array, video_array, title_text_origin)

            # Create json file after video is over to perserve data in the event of a failure and reduce memory pressure
            if res:
                td = target_time - datetime.now()
                days, hours, minutes = td.days, td.seconds//3600, (td.seconds//60)%60
                print(f"time till kill: {days} days {hours} hours {minutes} minutes")

                try:
                    buildFiles(res)
                except Exception:
                    print("Failed to build files for the following results:")
                    print(json.dumps(res[0], indent=4))
                    print(json.dumps(res[1], indent=4))
                    print("-"*60)
                    traceback.print_exc()
                    print("-"*60)


        browser.close()
        
        merge_all_logs()
        print("Done")