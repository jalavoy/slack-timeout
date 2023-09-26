#!/usr/bin/env python3
import logging
import os
import re
import sys

import redis

logging.basicConfig(level=logging.INFO)
from pprint import pprint

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
redis_hostname = os.environ.get("REDIS_HOST", "localhost")
redis_port = os.environ.get("REDIS_PORT", 6379)

redis = redis.Redis(
    host=redis_hostname,
    port=redis_port,
    socket_timeout=5
)

try:
    redis.ping()
except Exception as e:
    logging.error("Unable to connect to redis")
    logging.error(e)
    sys.exit(1)

# process mentions
@app.event("app_mention")
def app_mention(event, client, say):
    line = event["text"].split()
    line.pop(0)
    if len(line) == 0:
        return
    target, time = line
    uid = get_uid(target)
    if uid == event["user"]:
        say("Please checkout https://988lifeline.org/")
        return
    if is_admin(client, uid):
        say("Nice try idiot")
        return
    if time == "clear":
        clear_timeout(say, uid)
        return
    if check_user_exists(uid) is not None:
        say("User is in timeout for {} more seconds".format(redis.ttl(uid)))
        return
    time = int(int(time) * 60)
    if time < 1:
        say("Timeout is not a positive integer")
        return
    set_timeout(say, uid, time, target)

# process messages
@app.event("message")
def process_message(event, client, say):
    if "subtype" in event.keys():
        if event["subtype"] == "message_deleted":
            return
    uid = event["user"]
    if check_user_exists(uid) is not None:
        client.chat_delete(
            channel=event["channel"],
            ts=event["event_ts"],
            token=os.environ.get("SLACK_OAUTH_TOKEN")
        )

# parse slack UID from message
def get_uid(target):
    m = re.search(r"\<\@(.*)\>", target)
    return(m.group(1))

# remove timeout
def clear_timeout(say, uid):
    redis.delete(uid)
    say(
        "User time-out removed"
    )

# check if a user is already in timeout
def check_user_exists(uid):
    return(redis.get(uid))

# whitelist admins
def is_admin(client, uid):
    userinfo = client.users_info(user=uid)
    if userinfo["user"]["is_admin"]:
        return True
    else:
        return False

# put user in timeout
def set_timeout(say, uid, time, target):
    redis.set(uid, 1, ex=time)
    say(
        text="Putting user {} in time-out for {} minutes".format(
            target,
            int(time / 60),
        )
    )

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()