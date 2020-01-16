import News,json,requests,time,io,sys,os,telegram,subprocess
from twython import Twython 

try:
    with open("config.json") as f:
        config = json.loads(f.read())
        language = config["language"]
        twitterEnabled = config["twitter"]["enabled"]
        twitter_consumer_key = config["twitter"]["consumer_key"]
        twitter_consumer_secret = config["twitter"]["consumer_secret"]
        twitter_access_token = config["twitter"]["access_token"]
        twitter_access_token_secret = config["twitter"]["access_token_secret"]
        twitter_message = config["twitter"]["message"]
        telegramEnabled = config["telegram"]["enabled"]
        telegram_bot_token = config["telegram"]["bot_token"]
        telegram_chat_id = config["telegram"]["chat_id"]
        telegram_message = config["telegram"]["message"]
        telegram_parse_mode = config["telegram"]["parse_mode"]
        delay = config["delay"]
except:
    sys.exit()
    print("Sorry something went wrong while reading the config file.")



while True:
    FortniteGame = requests.get("https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game",headers={'Accept-Language' : language.lower()}).json()["battleroyalenews"]["news"]["motds"]

    if os.path.isfile(f"StoredNews.json") == False:
        with open("StoredNews.json", "w+") as file:
            file.write(json.dumps(FortniteGame))
    else:
        with open("StoredNews.json") as f:
            StoredNews = json.loads(f.read())

        if FortniteGame != StoredNews:
            print("Cambiamenti")
            News.GetBRNews(Language = language.lower())
            if twitterEnabled is True:
                try:
                    twitter = Twython(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret)
                    twitter.verify_credentials()
                except:
                    print("Authentication Failed")

                os.system('ffmpeg -i NewsBR.mp4 -vcodec libx264 NewsBRTwitter.mp4')
                video = open('NewsBRTwitter.mp4', 'rb')
                response = twitter.upload_video(media=video, media_type='video/mp4', media_category='tweet_video', check_progress=True)
                twitter.update_status(status=twitter_message, media_ids=[response['media_id']])

                print("Uploaded News on Twitter")

            if telegramEnabled is True:

                bot = telegram.Bot(token = telegram_bot_token)
                bot.send_video(chat_id = telegram_chat_id, video = open("NewsBR.mp4", "rb"), caption = telegram_message, parse_mode = telegram_parse_mode, timeout = 1000)
                
                print("Uploaded News on Telegram")

            with open("StoredNews.json","w+") as f:
                f.write(json.dumps(FortniteGame))

    time.sleep(delay)
