#!/usr/bin/python3
"""
Task 3 (advanced)
"""

import requests


def count_words(subreddit, word_list, after=None, counts={}):
    """
    Recursively queries the Reddit API, parses titles, and prints 
    a sorted count of keywords.
    """
    url = "https://www.reddit.com/r/{}/hot.json?after={}".format(subreddit,
                                                                 after)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/81.0.4044.138 Safari/537.36'}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        for post in response.json()['data']['children']:
            title = post['data']['title'].lower().split()
            for word in word_list:
                if word.lower() in title:
                    if word in counts:
                        counts[word] += title.count(word.lower())
                    else:
                        counts[word] = title.count(word.lower())
        after = response.json()['data']['after']
        if after is None:
            if len(counts) == 0:
                return
            for key, value in sorted(counts.items(),
                                     key=lambda x: (-x[1], x[0])):
                print("{}: {}".format(key, value))
            return
        return count_words(subreddit, word_list, after, counts)
    else:
        return