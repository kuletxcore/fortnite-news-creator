# Fortnite News Creator

![](https://img.shields.io/github/stars/MyNameIsDark01/fortnitenewscreator.svg) ![](https://img.shields.io/github/forks/MyNameIsDark01/fortnitenewscreator.svg) ![](https://img.shields.io/github/tag/MyNameIsDark01/fortnitenewscreator.svg) ![](https://img.shields.io/github/release/MyNameIsDark01/fortnitenewscreator.svg) ![](https://img.shields.io/github/issues/MyNameIsDark01/fortnitenewscreator.svg)

## Setup

1) Install Python
    - sudo apt install python3
    - sudo apt install python3-pip
  
2) Install the requirements
    - sudo pip3 install -r requirements.txt

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

If you want use this sort of library with your script copy News.py, util.py, config.json and assets folder. (It's a complete script so... WHY DO YOU WANT USE WITH ANOTHER SCRIPT?)

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
