import requests,json,textwrap
import PIL
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO
import cv2
import numpy as np
import glob
import os
from util import ImageUtil, Utility
from math import ceil

TitleColor = (255,255,255)
DescriptionColor = (51,236,254)

config = open("config.json", "r", encoding = "utf-8").read()
config = json.loads(config)
sort = config["sort"]

def GetCreativeNews(Language = "en"):

    FortniteGame = requests.get("https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game",headers={'Accept-Language' : Language.lower()}).json()["creativenews"]["news"]["motds"]

    AvoidScam = "https://cdn2.unrealengine.com/Fortnite/fortnite-game/battleroyalenews/v42/BR04_MOTD_Shield-1024x512-75eacc957ecc88e76693143b6256ba06159efb76.jpg"

    image_array = []

    for filename in glob.glob('News/NewsCreative/*.png'):
        os.remove(filename)

    for index, Message in enumerate(FortniteGame):
        news = News(Language, FortniteGame, Message)
        news.save(f"News/NewsCreative/{index - sort}.png")

    for filename in glob.glob('News/NewsCreative/*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        image_array.append(img)

    out = cv2.VideoWriter('NewsCreative.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 1, size)

    for i in range(len(image_array)):
        for item in range(4):
            out.write(image_array[i])
    out.release


def GetSTWNews(Language = "en"):

    FortniteGame = requests.get("https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game",headers={'Accept-Language' : Language.lower()}).json()["savetheworldnews"]["news"]["messages"]

    AvoidScam = "https://cdn2.unrealengine.com/Fortnite/fortnite-game/battleroyalenews/v42/BR04_MOTD_Shield-1024x512-75eacc957ecc88e76693143b6256ba06159efb76.jpg"

    image_array = []

    for filename in glob.glob('News/NewsSTW/*.png'):
        os.remove(filename)

    for index, Message in enumerate(FortniteGame):
        news = News(Language, FortniteGame, Message)
        news.save(f"News/NewsSTW/{index - sort}.png")

    for filename in glob.glob('News/NewsSTW/*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        image_array.append(img)

    out = cv2.VideoWriter('NewsSTW.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 1, size)

    for i in range(len(image_array)):
        for item in range(4):
            out.write(image_array[i])
    out.release

def GetBRNews(Language = "en"):

    FortniteGame = requests.get("https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game",headers={'Accept-Language' : Language.lower()}).json()["battleroyalenews"]["news"]["motds"]

    AvoidScam = "https://cdn2.unrealengine.com/Fortnite/fortnite-game/battleroyalenews/v42/BR04_MOTD_Shield-1024x512-75eacc957ecc88e76693143b6256ba06159efb76.jpg"

    image_array = []

    for filename in glob.glob('News/NewsBR/*.jpg'):
        os.remove(filename)

    for index, Message in enumerate(FortniteGame):
        news = News(Language, FortniteGame, Message)
        news.save(f"News/NewsBR/{index - sort}.jpg")

    for filename in glob.glob('News/NewsBR/*.jpg'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        image_array.append(img)

    out = cv2.VideoWriter('NewsBR.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 1, size)

    for i in range(len(image_array)):
        for item in range(4):
            out.write(image_array[i])
    out.release

def News(Language, FortniteGame, Message):

    if Language == "ja":
        DescriptionFont = ImageFont.truetype('assets/Fonts/NotoSansJP-Bold.otf', 36)
    elif Language == "ko":
        DescriptionFont = ImageFont.truetype('assets/Fonts/NotoSansKR-Regular.otf', 36)
    else:
        DescriptionFont = ImageFont.truetype('assets/Fonts/burbanksmall-bold.otf', 36)

    Background = Image.new("RGB", (1920, 1080))
    Draw = ImageDraw.Draw(Background)

    msg = ""
    TitleFontS = 100
    Title = ""

    if len(Message["body"]) > len(msg) and "body" in Message:
        msg = Message["body"]

    NewDesc = ""
    for Desc in msg.split("\n"):
        for Des in textwrap.wrap(Desc, width=39):
            NewDesc += f'\n{Des}'

    msg = NewDesc #Split the Description

    Title = Message["title"].upper()
    Description = Message["body"]

    NewsImage = Image.open(BytesIO(requests.get(Message["image"]).content)) #Download the Imag
    NewsImage = NewsImage.resize((1920, 1080), Image.ANTIALIAS) #Resize the downloaded Image

    TitleFontSize = 60

    if Language == "ja":
        TitleFont = ImageFont.truetype('assets/Fonts/NIS_JYAU.otf', TitleFontSize)
    elif Language == "ko":
        TitleFont = ImageFont.truetype('assets/Fonts/AsiaERINM.otf', TitleFontSize)
    else:
        TitleFont = ImageFont.truetype('assets/Fonts/BurbankBigRegular-Black.otf', TitleFontSize)

    NewDesc = ""
    for Desc in Description.split("\n"):
        for Des in textwrap.wrap(Desc, width=56):
            NewDesc += f'\n{Des}'

    Description = NewDesc #Split the Description

    Background.paste(NewsImage,(0, 0)) #paste Background
    Draw.text((50, 850),Title,TitleColor, font=TitleFont) #Draw Title

    Draw.multiline_text((50, 870),Description,DescriptionColor,font=DescriptionFont,spacing=13) #Draw Description

    TopTitle = TopUI(Language, FortniteGame)
    if TopTitle is not None:
        Background.paste(TopTitle, (0, 0))

    return Background

def TopUI(Language, FortniteGame):

    TopUI = Image.new("RGBA", (1920, 50))
    canvas = ImageDraw.Draw(TopUI)

    titles = []

    for item in FortniteGame:
        title = item["title"]
        titles.append(title)

    if len(titles) == 1:
        rows = max(ceil(len(titles) / 3), ceil(len(titles) / 3))

        i = 0
        for item in FortniteGame:
            card = GenerateCard1Titles(Language, item)
            if card is not None:
                TopUI.paste(
                    card,
                    ((0 + ((i % 3) * (card.width)), (0 + ((i // 3) * (card.height)))))
                )

                i = i + 1

    elif len(titles) == 2:
        rows = max(ceil(len(titles) / 2), ceil(len(titles) / 2))

        i = 0
        for item in FortniteGame:
            card = GenerateCard2Titles(Language, item)
            if card is not None:
                TopUI.paste(
                    card,
                    ((0 + ((i % 2) * (card.width)), (0 + ((i // 2) * (card.height)))))
                )

                i = i + 1

    elif len(titles) == 3:
        rows = max(ceil(len(titles) / 3), ceil(len(titles) / 3))

        i = 0
        for item in FortniteGame:
            card = GenerateCard3Titles(Language, item)
            if card is not None:
                TopUI.paste(
                    card,
                    ((0 + ((i % 3) * (card.width)), (0 + ((i // 3) * (card.height)))))
                )

                i = i + 1

    elif len(titles) == 4:
        rows = max(ceil(len(titles) / 4), ceil(len(titles) / 4))

        i = 0
        for item in FortniteGame:
            card = GenerateCard4Titles(Language, item)
            if card is not None:
                TopUI.paste(
                    card,
                    ((0 + ((i % 4) * (card.width)), (0 + ((i // 4) * (card.height)))))
                )

                i = i + 1
                
    elif len(titles) == 5:
        rows = max(ceil(len(titles) / 5), ceil(len(titles) / 5))

        i = 0
        for item in FortniteGame:
            card = GenerateCard5Titles(Language, item)
            if card is not None:
                TopUI.paste(
                    card,
                    ((0 + ((i % 5) * (card.width)), (0 + ((i // 5) * (card.height)))))
                )

                i = i + 1

    return TopUI

def GenerateCard1Titles(Language, item):

    card = Image.new("RGBA", (1920, 50))

    canvas = ImageDraw.Draw(card)

    if Language == "ja":
        font = ImageFont.truetype('assets/Fonts/NotoSansJP-Bold.otf', 15)
    elif Language == "ko":
        font = ImageFont.truetype('assets/Fonts/NotoSansKR-Regular.otf', 15)
    else:
        font = ImageFont.truetype('assets/Fonts/burbanksmall-black.otf', 15)

    title = item["title"]
    title = title.upper()

    icon = item["image"]
    icon = ImageUtil.Download(item, icon)
    icon = ImageUtil.RatioResize(item, icon, 1920, 1080)
    card.paste(icon, ImageUtil.CenterX(item, icon.width, card.width))

    try:
        TINT_COLOR = (0, 0, 205)  # Black
        TRANSPARENCY = 0.7  # Degree of transparency, 0-100%
        OPACITY = int(255 * TRANSPARENCY)

        cardBottom = Image.new("RGBA", (1920,360), TINT_COLOR)
        draw = ImageDraw.Draw(cardBottom)
        draw.rectangle(((1920, 360), (0, 0)), fill=TINT_COLOR+(OPACITY,))
    except Exception as e:
        print(e)
    card.paste(cardBottom, (0, 0), cardBottom)

    textWidth, _ = font.getsize(title)
    if textWidth >= 1920:
        # Ensure that the item name does not overflow
        if Language == "ja":
            font, textWidth = ImageUtil.FitTextX2(item, title, 16, 1920)
        elif Language == "ko":
            font, textWidth = ImageUtil.FitTextX1(item, title, 16, 1920)
        else:
            font, textWidth = ImageUtil.FitTextX(item, title, 16, 1920)
    canvas.text(
        ImageUtil.CenterX(item, textWidth, card.width, 15),
        title,
        (255, 255, 255),
        font=font,
    )

    return card

def GenerateCard2Titles(Language, item):

    card = Image.new("RGBA", (960, 50))

    canvas = ImageDraw.Draw(card)

    if Language == "ja":
        font = ImageFont.truetype('assets/Fonts/NotoSansJP-Bold.otf', 15)
    elif Language == "ko":
        font = ImageFont.truetype('assets/Fonts/NotoSansKR-Regular.otf', 15)
    else:
        font = ImageFont.truetype('assets/Fonts/burbanksmall-black.otf', 15)

    title = item["title"]
    title = title.upper()

    icon = item["image"]
    icon = ImageUtil.Download(item, icon)
    icon = ImageUtil.RatioResize(item, icon, 960, 540)
    card.paste(icon, ImageUtil.CenterX(item, icon.width, card.width))

    try:
        TINT_COLOR = (0, 0, 205)  # Black
        TRANSPARENCY = 0.7  # Degree of transparency, 0-100%
        OPACITY = int(255 * TRANSPARENCY)

        cardBottom = Image.new("RGBA", (960,360), TINT_COLOR)
        draw = ImageDraw.Draw(cardBottom)
        draw.rectangle(((960, 360), (0, 0)), fill=TINT_COLOR+(OPACITY,))
    except Exception as e:
        print(e)
    card.paste(cardBottom, (0, 0), cardBottom)

    textWidth, _ = font.getsize(title)
    if textWidth >= 960:
        # Ensure that the item name does not overflow
        if Language == "ja":
            font, textWidth = ImageUtil.FitTextX2(item, title, 16, 960)
        elif Language == "ko":
            font, textWidth = ImageUtil.FitTextX1(item, title, 16, 960)
        else:
            font, textWidth = ImageUtil.FitTextX(item, title, 16, 960)
    canvas.text(
        ImageUtil.CenterX(item, textWidth, card.width, 15),
        title,
        (255, 255, 255),
        font=font,
    )

    return card

def GenerateCard3Titles(Language, item):

    card = Image.new("RGBA", (640, 50))

    canvas = ImageDraw.Draw(card)

    if Language == "ja":
        font = ImageFont.truetype('assets/Fonts/NotoSansJP-Bold.otf', 15)
    elif Language == "ko":
        font = ImageFont.truetype('assets/Fonts/NotoSansKR-Regular.otf', 15)
    else:
        font = ImageFont.truetype('assets/Fonts/burbanksmall-black.otf', 15)

    title = item["title"]
    title = title.upper()

    icon = item["image"]
    icon = ImageUtil.Download(item, icon)
    icon = ImageUtil.RatioResize(item, icon, 640, 360)
    card.paste(icon, ImageUtil.CenterX(item, icon.width, card.width))

    try:
        TINT_COLOR = (0, 0, 205)  # Black
        TRANSPARENCY = 0.7  # Degree of transparency, 0-100%
        OPACITY = int(255 * TRANSPARENCY)

        cardBottom = Image.new("RGBA", (640,360), TINT_COLOR)
        draw = ImageDraw.Draw(cardBottom)
        draw.rectangle(((640, 360), (0, 0)), fill=TINT_COLOR+(OPACITY,))
    except Exception as e:
        print(e)
    card.paste(cardBottom, (0, 0), cardBottom)

    textWidth, _ = font.getsize(title)
    if textWidth >= 620:
        # Ensure that the item name does not overflow
        if Language == "ja":
            font, textWidth = ImageUtil.FitTextX2(item, title, 16, 1920)
        elif Language == "ko":
            font, textWidth = ImageUtil.FitTextX1(item, title, 16, 1920)
        else:
            font, textWidth = ImageUtil.FitTextX(item, title, 16, 1920)
    canvas.text(
        ImageUtil.CenterX(item, textWidth, card.width, 15),
        title,
        (255, 255, 255),
        font=font,
    )

    return card

def GenerateCard4Titles(Language, item):

    card = Image.new("RGBA", (480, 50))

    canvas = ImageDraw.Draw(card)

    if Language == "ja":
        font = ImageFont.truetype('assets/Fonts/NotoSansJP-Bold.otf', 15)
    elif Language == "ko":
        font = ImageFont.truetype('assets/Fonts/NotoSansKR-Regular.otf', 15)
    else:
        font = ImageFont.truetype('assets/Fonts/burbanksmall-black.otf', 15)

    title = item["title"]
    title = title.upper()

    icon = item["image"]
    icon = ImageUtil.Download(item, icon)
    icon = ImageUtil.RatioResize(item, icon, 480, 270)
    card.paste(icon, ImageUtil.CenterX(item, icon.width, card.width))

    ### 1920 * 1080 = 384
    try:
        TINT_COLOR = (0, 0, 205)  # Black
        TRANSPARENCY = 0.7  # Degree of transparency, 0-100%
        OPACITY = int(255 * TRANSPARENCY)

        cardBottom = Image.new("RGBA", (480,360), TINT_COLOR)
        draw = ImageDraw.Draw(cardBottom)
        draw.rectangle(((480, 360), (0, 0)), fill=TINT_COLOR+(OPACITY,))
    except Exception as e:
        print(e)
    card.paste(cardBottom, (0, 0), cardBottom)

    textWidth, _ = font.getsize(title)
    if textWidth >= 480:
        # Ensure that the item name does not overflow
        if Language == "ja":
            font, textWidth = ImageUtil.FitTextX2(item, title, 16, 480)
        elif Language == "ko":
            font, textWidth = ImageUtil.FitTextX1(item, title, 16, 480)
        else:
            font, textWidth = ImageUtil.FitTextX(item, title, 16, 480)
    canvas.text(
        ImageUtil.CenterX(item, textWidth, card.width, 15),
        title,
        (255, 255, 255),
        font=font,
    )

    return card

def GenerateCard5Titles(Language, item):

    card = Image.new("RGBA", (384, 50))

    canvas = ImageDraw.Draw(card)

    if Language == "ja":
        font = ImageFont.truetype('assets/Fonts/NotoSansJP-Bold.otf', 15)
    elif Language == "ko":
        font = ImageFont.truetype('assets/Fonts/NotoSansKR-Regular.otf', 15)
    else:
        font = ImageFont.truetype('assets/Fonts/burbanksmall-black.otf', 15)

    title = item["title"]
    title = title.upper()

    icon = item["image"]
    icon = ImageUtil.Download(item, icon)
    icon = ImageUtil.RatioResize(item, icon, 384, 216)
    card.paste(icon, ImageUtil.CenterX(item, icon.width, card.width))

    ### 1920 * 1080 = 384
    try:
        TINT_COLOR = (0, 0, 205)  # Black
        TRANSPARENCY = 0.7  # Degree of transparency, 0-100%
        OPACITY = int(255 * TRANSPARENCY)

        cardBottom = Image.new("RGBA", (384,360), TINT_COLOR)
        draw = ImageDraw.Draw(cardBottom)
        draw.rectangle(((384, 360), (0, 0)), fill=TINT_COLOR+(OPACITY,))
    except Exception as e:
        print(e)
    card.paste(cardBottom, (0, 0), cardBottom)

    textWidth, _ = font.getsize(title)
    if textWidth >= 364:
        # Ensure that the item name does not overflow
        if Language == "ja":
            font, textWidth = ImageUtil.FitTextX2(item, title, 16, 1920)
        elif Language == "ko":
            font, textWidth = ImageUtil.FitTextX1(item, title, 16, 1920)
        else:
            font, textWidth = ImageUtil.FitTextX(item, title, 16, 1920)
    canvas.text(
        ImageUtil.CenterX(item, textWidth, card.width, 15),
        title,
        (255, 255, 255),
        font=font,
    )

    return card
