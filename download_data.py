import tweepy
import json
import time
import sqlite3
from twitter_credentials import *



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

conn =  sqlite3.connect('example.sqlite')
c =  conn.cursor()
#-----
file_out = open('downloaded.json', 'w')

#===== tTweets table creation
tweet_data_to_export = [('id_str','text PRIMARY KEY'), ('txt','text'), ('created_at', 'text'), ('retweet_count', 'integer'), 
						('user_id','text'), ('created_new', 'text')]

tweet_fields_to_insert = [f + " " + t for (f,t) in tweet_data_to_export]
tweet_fields = ','.join(tweet_fields_to_insert)

c.execute('DROP INDEX IF EXISTS id_idx')
c.execute('DROP INDEX IF EXISTS id_idx5')
conn.commit()

c.execute('CREATE TABLE IF NOT EXISTS tTweets (' + tweet_fields + ")")
c.execute('CREATE UNIQUE INDEX  IF NOT EXISTS id_idx ON tTweets(id_str)')
#===== tUsers table creation

user_fields = []
user_fields_to_create = []
user_data_to_save = []

user = api.get_user('analyticbridge')

for k,v in user._json.items():
	print('adding field ' + k + ' to tUsers', 'type is ' + str(type(v)))
	if type(v) is dict:
		continue
	if type(v) is int:
		user_fields_to_create.append(str(k) + ' INTEGER')
	else: 
		user_fields_to_create.append(str(k) + ' TEXT')
	if k == 'id': user_fields_to_create[-1] = user_fields_to_create[-1] + " PRIMARY KEY"
	user_fields.append(k)
	user_data_to_save.append(v)

c.execute('CREATE TABLE IF NOT EXISTS tUsers (' + ', '.join(user_fields_to_create) + ')')
c.execute('CREATE UNIQUE INDEX IF NOT EXISTS user_id_idx ON tUsers(id)')
c.execute('INSERT OR REPLACE into tUsers (' + ','.join(user_fields) + ') VALUES (?' +', ?'*(len(user_fields)-1) + ')', user_data_to_save)

conn.commit()

data = []
for status in tweepy.Cursor(api.user_timeline, id='analyticbridge', count = 20).items(20):
	j = status._json
	created_new = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(j['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
	tweet = [j['id_str'], j['text'], j['created_at'], j['retweet_count'], j['user']['id'], created_new]
	data.append(tweet)

	json.dump(j, file_out, sort_keys = True, indent = 4)
	print('.', '')
	pass
c.executemany('''INSERT OR REPLACE into tTweets (id_str, txt, created_at,retweet_count, user_id, created_new) VALUES (?, ?, ?, ?, ?, ?)''', data)

#closing all the connections
conn.commit()
c.close()
conn.close()
file_out.close()
print('Done!')