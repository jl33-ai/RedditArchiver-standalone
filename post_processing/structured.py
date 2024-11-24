import re

from bs4 import BeautifulSoup
import pandas as pd

def convert_to_df(html):
    """
    Converts html of Reddit thread into a structured dataframe
    Each comment is placed in a row along with metadata

    :param html:
    :return: Dataframe containing all commends in the thread
    """
    soup = BeautifulSoup(html, 'html.parser')

    urls = []
    usernames = []
    comments = []

    comment_divs = soup.find_all('div', id=re.compile('^t1_'), class_=re.compile(r'\bl1\b'))

    for div in comment_divs:
        header = div.find('header')
        if not header:
            continue

        a_tags = header.find_all('a')
        if len(a_tags) >= 2:
            username = a_tags[0].get_text(strip=True)
            url = a_tags[1].get('href')
        else:
            continue

        p_tags = [p for p in div.find_all('p', recursive=False)]

        comment_text = ' '.join([p.get_text(strip=True) for p in p_tags])

        urls.append(url)
        usernames.append(username)
        comments.append(comment_text)

    df = pd.DataFrame({'url': urls, 'username': usernames, 'comment': comments})

    return df
