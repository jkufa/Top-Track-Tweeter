#!/bin/bash
if [ `date +%d` -gt 1 ]; then
  exit
else
  cd ~/Octokitty/Personal/Top-Track-Tweeter
  python3 tweet_tracks.py > ~/track_tweets/log_`date +"%Y-%m-%d"`.txt
fi