#!/usr/bin/python3
"""
Queries the Reddit API, parses the title of all hot articles, and prints a
sorted count of given keywords (case-insensitive, delimited by spaces.
"""
import requests


def count_words(subreddit, word_list, after=None, word_dict={}):
    """
    Queries the Reddit API, parses the title of all hot articles, and prints a
    sorted count of given keywords (case-insensitive, delimited by spaces.
    Javascript should count as javascript, but java should not)
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
                    if word in word_dict:
                        word_dict[word] += title.count(word.lower())
                    else:
                        word_dict[word] = title.count(word.lower())
        after = response.json()['data']['after']
        if after is None:
            if len(word_dict) == 0:
                return
            for key, value in sorted(word_dict.items(),
                                     key=lambda x: (-x[1], x[0])):
                print("{}: {}".format(key, value))
            return
        return count_words(subreddit, word_list, after, word_dict)
    else:
        return