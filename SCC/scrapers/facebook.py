import pandas as pd
from facebook_scraper import get_posts


def get_fb_posts(group, pages):
    posts = []
    for post in get_posts(group=group, pages=pages): # group ID for don't shop here group
        posts.append(post)
    return posts

