#!/usr/bin/python3
"""
Queries the Reddit API and returns a list containing the titles of all hot
articles for a given subreddit
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Queries the Reddit API and returns a list containing the titles of all hot
    articles for a given subreddit
    """
    url = "https://www.reddit.com/r/{}/hot.json?after={}".format(subreddit,
                                                                 after)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/81.0.4044.138 Safari/537.36'}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        for post in response.json()['data']['children']:
            hot_list.append(post['data']['title'])
        after = response.json()['data']['after']
        if after is None:
            return hot_list
        return recurse(subreddit, hot_list, after)
    else:
        return None