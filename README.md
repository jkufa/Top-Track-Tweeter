# Top Tracks Tweeter for Spotify
This is a simple script that tweets out your top played tracks from the past four weeks, creating a playlist containing those tracks as well.

## How to run:
1. Clone this repository
2. Create a Spotify application
3. Create a Twitter application
4. Create `keys.json` file
5. either run `tweet_tacks.py` or setup crontab to automate a monthly tweet

## 1. Clone Repository
To clone, simply run `git clone `.

## 2. Create Spotify Application
Follow the 3 steps in [this guide](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app) and find your Client ID and Secret ID.

## 3. Create Twitter Application
1. go to the [Twitter developer portal](https://developer.twitter.com/en/portal/projects-and-apps) and create a new project. 
2. Go to the project's settings and change the app permissions to read and write.
3. Go to keys and tokens to find your API key, secret key, and bearer token.
4. Generate an access token and secret token

## 4. Populate JSON
Create a file called `keys.json` file with the following attributes:
```json
{
  "API_KEY": "",
  "SECRET_KEY": "",
  "BEARER_TOKEN": "",
  "OAUTH_TOKEN": "",
  "OAUTH_TOKEN_SECRET": "",
  "CLIENT_ID": "",
  "SECRET_ID": "",
  "REDIRECT_URL": ""

}
```
Add the keys to all of the attributes.
|JSON Attribute|Key|
|--------------|---|
|API_KEY|Twitter API key|
|SECRET_KEY|Twitter secret key|
|BEARER_TOKEN|Twitter bearer token|
|OAUTH_TOKEN|Twitter access token|
|OAUTH_TOKEN_SECRET|Twitter secret token|
|CLIENT_ID|Spotify client id|
|SECRET_ID|Spotify secret id|
|REDIRECT_URL|url to redirect to after spotify authentication. Can be anything.|

## 5. Run Script
To run, simply type `python3 tweet_tracks.py` in the repository's directory.

Alternatively, if you want to set up a monthly automated tweet, simply do the following:
1. give the python script executable privilages with `chmod -x tweet_tracks.py`
2. type `crontab -e` in terminal and add the following: `* 23 1 * * <DIRECTORY TO PYTHON SCRIPT>`

Example: `* 23 1 * * ~/Octokitty/Personal/auto-tweet/tweet_tracks.py`

Now on the first day of every month, you will tweet out the top 5 tracks on your spotify account, accompanied by a newly created playlist!

