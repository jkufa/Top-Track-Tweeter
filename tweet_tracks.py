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
  months = ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
  last_month = datetime.today().month-2
  if(last_month == 0):
    year = datetime.today().year-1
  else:
    year = datetime.today().year
  return last_month,year

class TweetTracks:
  def __init__(self):
    self.keys = get_keys()
    self.last_month,self.year = get_dates()
    self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.keys['CLIENT_ID'],
                                              client_secret=self.keys['SECRET_ID'],
                                              redirect_uri=self.keys['REDIRECT_URL'],
                                              scope='user-top-read playlist-modify-public'))
    self.user_id = self.sp.current_user()['id']

  def create_playlist(self):
    playlist_name = "Top Songs For " + self.months[self.last_month] + " " + str(self.current_year)
    self.sp.user_playlist_create(self.user_id,playlist_name)
    self.add_songs(playlist_name)

  def tweet_top_songs(self):
    results = self.fetch_top_songs()
    msg = "My top songs for " + self.months[self.last_month] + ":\n"
    for i, item in enumerate(results['items']):
      name = item['name']
      artist = item['artists'][0]['name']
      # print(artist)
      msg = msg + str(i+1) + ". " + name + " by " + artist + "\n"
    msg = msg + "Listen here: " + self.fetch_playlist_url("Top Songs For " + self.months[self.last_month] + " " + str(self.current_year)) + "\n"
    self.tweetify(msg)    
  
  def fetch_top_songs(self):
    return self.sp.current_user_top_tracks(limit=5,offset=0,time_range='short_term')

  # Fetch top songs and insert them into given playlist
  def add_songs(self, playlist):
    playlists = self.sp.current_user_playlists()
    tracks = self.fetch_top_songs()
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
  
  def tweetify(self, msg):
    tw = Twython(self.keys['API_KEY'], self.keys['SECRET_KEY'], self.keys['OAUTH_TOKEN'], self.keys['OAUTH_TOKEN_SECRET'])
    tw.update_status(status=msg)
    print("Tweeted message " + msg)

# ts = TweetTracks()
# ts.create_playlist()
# ts.tweet_top_tracks()
print("boop")