from datetime import timezone, datetime
import requests, json

base_url = "https://api.pushshift.io/reddit/search/submission/"

"""@params date_obj: A dictionary like object with the keys "year" "day"
and "month"
@Return Int representing Unix time in UTC
fucntion is used to convert human readable dates to one appropriate for the API"""
def dateToUnixUTC(date_obj):
    dt = datetime(date_obj['year'], date_obj['month'], date_obj['day'])
    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
    return int(timestamp)

"""
@params
sub: string name of subreddit
q: search term to query
before: int representing unix utc time or dict with day month year keys
after: see before

@Return: list of submission ids as strings
"""
def submissionIDList(sub=None, q=None, before=None, after=None):
    if type(before) == dict:
        before = dateToUnixUTC(before)
    if type(after) == dict:
        after = dateToUnixUTC(after)

    payload = {
    'q':q,
    'subreddit':sub,
    'before':before,
    'after':after
    }

    r = requests.get(base_url, params=payload)
    data = json.loads(r.text)

    return [post['id'] for post in data['data']]


def readJSONasDict(path):
    with open(path, 'r') as f:
        d = json.loads(f.read())
    return d


def removeDupes(l):
    return list(dict.fromkeys(l))
