#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import telegram # pip3 install python-telegram-bot

import json
import re

REQUEST_URL = "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize"
PARSER = {
    "electimes" : {
        "title_selector" : "#article-view > div > header > div.heading-group > h3",
        "content_selector" : "#article-view-content-div"
    }
}

class SummarizerBot():
    def __init__(self):
        self.headers = {}
        self.bot = ""
        self.chat_id = ""

        self.init_api()
        self.init_bot()
        self.init_data()

    def summarize(self, url):
        self.fetch_contents(url)
        self.send_data_to_telegram(url)

    def init_api(self):
        try:
            with open("api_info.txt", "r") as f:
                client_id = f.readline().replace("\n","")
                client_secret = f.readline().replace("\n","")
                self.headers = {
                                "X-NCP-APIGW-API-KEY-ID": client_id,
                                "X-NCP-APIGW-API-KEY": client_secret,
                                "Content-Type": "application/json"
                                }

        except FileNotFoundError:
            with open("api_info.txt", "w") as f:
                f.write("Replace this line with your client_id(example: oawv4qurkm)\nReplace this line with your client_secret(example: x2gds3M35LT419asdsadqtggZhSq6gBojKQwVY)")
                print("You need Naver API client. I'll make you a info file. Fill the file with content and try again.")

    def init_data(self):
        language = "ko" # Language of document (ko, ja )
        model = "news" # Model used for summaries (general, news)
        tone = "2" # Converts the tone of the summarized result. (0, 1, 2, 3)
        summaryCount = "3" # This is the number of sentences for the summarized document.

        self.data = {
            "document": {
                "title": "",
                "content" : ""
                    },

            "option": {
                "language": language,
                "model": model,
                "tone": tone,
                "summaryCount" : summaryCount
                    }
        }

    def init_bot(self):
        try:
            with open("bot_info.txt", "r") as f:
                bot_id = f.readline().replace("\n","")
                self.chat_id = f.readline().replace("\n","")
                self.bot = telegram.Bot(bot_id)

        except FileNotFoundError:
            with open("bot_info.txt", "w") as f:
                f.write("Replace this line with your bot_id(example: 1111111111:AA3SD1AS6D1Q5W23S1CZ8XV1531A3)\nReplace this line with your client_secret(example: 2353214773)")
                print("You need Telegram API client. I'll make you a info file. Fill the file with content and try again.")

    def fetch_contents(self, url):
        html = requests.get(url).text
        bs_object = BeautifulSoup(html, "html.parser")

        self.data["document"]["title"] = bs_object.select(PARSER["electimes"]["title_selector"])[0].text.strip()

        news_raw_text = bs_object.select(PARSER["electimes"]["content_selector"])[0].text.strip()
        self.data["document"]["content"] = re.sub("\n+"," ",news_raw_text)

    def send_data_to_telegram(self, url):
        response = requests.post(REQUEST_URL, data=json.dumps(self.data), headers=self.headers)
        if response.status_code == 200:
            summarized_text = json.loads(response.text)["summary"]
            pretty_text = "{}{}".format("- ", summarized_text.replace("\n", "\n\n- "))

            contents = "{}\n\n{}\n\n{}".format(self.data["document"]["title"], pretty_text, url)

            self.bot.sendMessage(chat_id=self.chat_id, text=contents)


bot = SummarizerBot()

electimes_url = "https://www.electimes.com/news/articleList.html?view_type=sm"
html = requests.get(electimes_url).text
bs_object = BeautifulSoup(html, "html.parser")
links = bs_object.select("#section-list > ul > li")

electimes_base_url = "https://www.electimes.com"
for link in links:
    url = electimes_base_url + str(link.find('a')['href'])
    bot.summarize(url)



