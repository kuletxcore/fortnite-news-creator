# Fortnite News Creator
## Setup

1) Install Python
2) Install the requirements (pip install -r requirements.txt or pip3 install -r requirements.txt)
3) Install ffmpeg and x264lib (for ubuntu below)
  - sudo apt install ffmpeg
  - sudo apt install libx264-dev

## Compatibility
### Twitter:

If You want post on Twitter use Feed.py, remember to compile config.json.
  - Enable Twitter;
  - Insert app tokens;
  - Insert Twitter Message.

### Telegram:

If You want post on Telegram use Feed.py, remember to compile config.json.
  - Enable Telegram;
  - Insert Bot Token;
  - Insert Chat_ID;
  - Insert Telegram Message and parse_mode.

## Example:

```
import News

NewsBR = News.GetBRNews(Language = "en) #Set your language here
NewsCreative = News.GetCreativeNews(Language = "en) #Set your language here
NewsSTW = News.GetSTWNews(Language = "en) #Set your language here

It will create automatically a mp4 file called "News{NewsType}.mp4"
```

Output:

![BR](https://github.com/MyNameIsDark01/fortnitenewscreator/blob/master/examples/NewsBR.gif?raw=true)

![CREATIVE](https://github.com/MyNameIsDark01/fortnitenewscreator/blob/master/examples/NewsCreative.gif?raw=true)

![STW](https://github.com/MyNameIsDark01/fortnitenewscreator/blob/master/examples/NewsSTW.gif?raw=true)
