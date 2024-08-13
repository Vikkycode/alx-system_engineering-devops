#!/usr/bin/python3
"""Function to query subscribers on a given reddit subreedit"""
import requests

def number_of_subscribers(subreddit):
    """ Return the total number of subscribers on a given reddit subreddit"""

    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {
            "User-Agent":"linux:0x16.api.advanced:v1.0.0 (by /u/vikkycode_)"
    }

    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 404:
        return 0
    results = response.json().get("data")
    return results.get("subscribers")


