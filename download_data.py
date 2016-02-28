import tweepy
import json
import time
from datetime import datetime
from twitter_credentials import *
from declaration import Person, Status, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


#connection to twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#connection to DB
engine = create_engine('sqlite:///twittet_app.sqlite', echo=False)
DBSession = sessionmaker(bind=engine)
session =  DBSession()
#set parameters
user_name = 'analyticbridge'

#saving user data
person_full = api.get_user(user_name)
j =  person_full._json
if session.query(Person).filter(Person.screen_name == user_name).count() == 0:
	p =  Person(
				id = j['id'], 
				screen_name = j['screen_name'] , 
				name = j['name'],
				description = j['description'],
				location = j['location'],
				url = j['url'], 
				followers_count = j['followers_count'],
				statuses_count = j['statuses_count'], 
				friends_count = j['friends_count'])
	session.add(p)
	session.commit()
else:
	p = session.query(Person).filter(Person.screen_name == user_name).one()
	p.name = j['name']
	p.description = j['description']
	p.location = j['location']
	p.url = j['url']
	p.followers_count = j['followers_count']
	p.statuses_count = j['statuses_count']
	p.friends_count = j['friends_count']
	session.commit()

#saving tweets of user


for status in tweepy.Cursor(api.user_timeline, id='analyticbridge', count = 200).items(200):
	j = status._json
	if session.query(Status).filter(Status.id == j['id_str']).count() == 0:
		#add new tweet
		created_at = datetime.strptime(j['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
		s = Status(
			id = j['id_str'],
			text = j['text'],
			created_at = created_at,
			retweet_count = j['retweet_count'],
			retweeted = j['retweeted'],
			person = p)
		session.add(s)
		session.commit()
		print("Tweet " + j['id_str'] + " is imported")
	else:
		#update the tweet
		s = session.query(Status).filter(Status.id == j['id_str']).one()
		retweet_count = j['retweet_count'],
		session.commit()
