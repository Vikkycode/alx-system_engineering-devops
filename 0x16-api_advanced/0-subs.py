#!/usr/bin/python3
"""
Function to query the number of subscribers in a given Reddit subreddit.
"""

import requests


def number_of_subscribers(subreddit):
    """ 
    Return the total number of subscribers in a given Reddit subreddit.
    
    Args:
        subreddit (str): The name of the subreddit to query.

    Returns:
        int: The number of subscribers. Returns 0 if the subreddit is invalid or on error.
    """

    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/vikkycode_)"
    }

    response = requests.get(url, headers=headers, allow_redirects=False)
    
    if response.status_code == 404:
        return 0
    
    try:
        results = response.json().get("data")
        return results.get("subscribers", 0)
    except (ValueError, AttributeError):
        return 0

