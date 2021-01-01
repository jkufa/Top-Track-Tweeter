#!/usr/bin/python3 

from datetime import datetime
from twython import Twython
from spotipy.oauth2 import SpotifyOAuth
import json
import spotipy

def get_keys():
  with open('keys.json','r') as file:
    data = file.read()
  return json.loads(data)
def get_dates(): 
  last_month = datetime.today().month-2 # -2 because datetime.today().month is not 0 index
  if(last_month == -1):
    year = datetime.today().year-1
  else:
    year = datetime.today().year
  return last_month,year

class TweetTracks:
  def __init__(self):
    self.months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    self.keys = get_keys()
    self.last_month,self.current_year = get_dates()
    self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.keys['CLIENT_ID'],
                                              client_secret=self.keys['SECRET_ID'],
                                              redirect_uri=self.keys['REDIRECT_URL'],
                                              scope='user-top-read playlist-modify-public'))
    self.user_id = self.sp.current_user()['id']

  # Create playlist, return True if successfully made
  def create_playlist(self):
    playlist_name = "Top Songs For " + self.months[self.last_month] + " " + str(self.current_year)
    if not self.does_playlist_exist(playlist_name):
      self.sp.user_playlist_create(self.user_id,playlist_name)
      return playlist_name
    return None

  # Make sure playlist that is about to be made doesn't already exist
  def does_playlist_exist(self,playlist_name):
    playlists = self.sp.user_playlists(self.user_id)
    for playlist in playlists['items']:
      if playlist['name'] == playlist_name and playlist['owner']['id'] == self.user_id:
        return True
    return False

  # Creates array of msg lines, and condenses said array into a new subarray that consists of tweets that are <= 280 characters
  def make_tweet_msgs(self,limit=5,range='short_term'):
    results = self.fetch_top_songs(limit,range)
    msg = ["My top songs for " + self.months[self.last_month] + ":"]
    for i, item in enumerate(results['items']):
      name = item['name']
      artist = item['artists'][0]['name']
      msg.append(str(i+1) + ". " + name + " by " + artist)
    msg.append("Listen here: " + self.fetch_playlist_url("Top Songs For " + self.months[self.last_month] + " " + str(self.current_year)))
    return(self.split_tweets(msg))

  # If msg from make_tweets is above 280 characters, split off lines from the end into multiple tweets
  def split_tweets(self, msg):
    tweet_len = 0
    tweets = []
    tweet_msg = ""
    i = 0
    while(i < len(msg)):
      if(tweet_len + len(msg[i]) <= 280):
        tweet_len += len(msg[i])
        tweet_msg = tweet_msg + (msg[i] + "\n")
        i += 1
      else:
        tweets.append(tweet_msg)
        tweet_len = 0
        tweet_msg = ""
    tweets.append(tweet_msg)
    return tweets

  def tweet_top_tracks(self,debug=False, msg=[]):
    tweets = self.make_tweet_msgs()
    if debug:
      tweets = msg
    curr_tweet = self.tweetify(tweets[0]) # Always tweet 1st entry
    for tw in tweets[1:]:
      curr_tweet = self.tweetify(tw, is_reply=True, twitter_id=curr_tweet['id'])
  
  def fetch_top_songs(self,song_no=5,range='short_term'):
    return self.sp.current_user_top_tracks(limit=song_no,offset=0,time_range=range)

  # Fetch top songs and insert them into given playlist
  def add_songs(self, playlist, tracks):
    playlists = self.sp.current_user_playlists()
    track_list = []
    for t in tracks['items']:
      track_list.append(t['id'])
    for pl in playlists['items']:
      if(pl['name'] == playlist):
        self.sp.user_playlist_add_tracks(self.user_id, pl['id'],track_list)
  
  def fetch_playlist_url(self, playlist_name):
    playlists = self.sp.current_user_playlists()
    for pl in playlists['items']: 
      if(pl['name'] == playlist_name):
        result = pl['external_urls']
        return result['spotify']
  
  def tweetify(self, msg, is_reply=False, twitter_id=''):
    tw = Twython(self.keys['API_KEY'], self.keys['SECRET_KEY'], self.keys['OAUTH_TOKEN'], self.keys['OAUTH_TOKEN_SECRET'])
    if is_reply:
      tweet = tw.update_status(status=msg, in_reply_to_status_id=twitter_id)
    else:
      tweet = tw.update_status(status=msg)
    print("Tweeted message:\n" + msg)
    return tweet
  

ts = TweetTracks()

# print("Current top songs:")
# msgs = ts.make_tweet_msgs(5,'medium_term')
# for msg in msgs:
#   print(msg)

# Run script
pname = ts.create_playlist()
if pname != None:
  tracks = ts.fetch_top_songs()
  ts.add_songs(pname,tracks)
  ts.tweet_top_tracks()
else:
  print("An error occured. The playlist already exists.")