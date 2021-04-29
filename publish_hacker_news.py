import requests
from bs4 import BeautifulSoup
from soupsieve import select
import pprint
import tweepy
import time
import re

class Selected(object):
    title = ""
    num_votes = 0
    link = ""
    age = 4320
    score = 0

    def __init__(self, title, num_votes, link, age):
        self.title = title
        self.num_votes = num_votes
        self.link = link
        self.age = age
        self.score = num_votes/age

    def __str__(self):
        return f' Votes: {self.num_votes}, Age: {self.age} min, Score: {self.score}, <<-->> {self.title} <<-->> {self.link}'

thresh = 500
page = 0
age = 4320
has_next = True
summary = []

while has_next:
    page += 1
    res = requests.get(f'https://news.ycombinator.com/news?p={str(page)}')
    soup = BeautifulSoup(res.text, 'html.parser')

    links = soup.select('.storylink')
    subtexts = soup.select('.subtext')
    votes = soup.select('.score')
    ages = soup.select('.age')
    page_sel = soup.select('.morelink')
    for i,vote in enumerate(votes):
        base_age = ages[i].getText()
        age_int = int(re.sub('\D', '', base_age))
        if 'minute' in base_age:
            age = age_int
        elif 'hour' in base_age:
            age = age_int * 60
        elif 'day' in base_age:
            age = age_int * 1440

        title = links[i].getText()
        href = links[i].get('href')
        subtext = subtexts[i].getText()
        if ' points' in subtext:
            num_votes = int(votes[i].getText().replace(' points',''))
            summary.append(Selected(title,num_votes,href,age))

    if len(page_sel) == 0:
        has_next = False

sorted_summary = sorted(summary, key=lambda x: x.score, reverse=True)
print('======================================================================================================')
print('======================================================================================================')

for element in sorted_summary:
    if (element.score > .06):
        print(element)

# Select most voted new 
print('======================================================================================================')
print('======================================================================================================')
most_voted_article = sorted_summary[0]

print(f'Winner article is: {most_voted_article}')
# Start twitter authentication
auth = tweepy.OAuthHandler('tweeter-apikey','tweeter-apikey')
auth.set_access_token('tweeter-apikey','tweeter-apikey')

api = tweepy.API(auth)
print('======================================================================================================')
print('======================================================================================================')

# Create a tweet
new_tweet = f'{most_voted_article.title} {most_voted_article.link}'
print('Now tweeting ' + new_tweet)
# api.update_status(new_tweet)
