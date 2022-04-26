#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


import json
import re
import sys

REQUEST_URL = "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize"
PARSER = {
    "electimes" : {
        "title_selector" : "#article-view > div > header > div.heading-group > h3",
        "content_selector" : "#article-view-content-div"
    }
}

# TODO 3 : 전기신문 리스트에서 링크 뽑아오기 - > 그 링크에서 TODO 2에 해당하는 작업을 수행하는 거임
# TODO 4 : 텔레그램봇 연결해서 보내기.

class SummarizerBot():
    def __init__(self, client_id, client_secret):
        self.headers = {
                        "X-NCP-APIGW-API-KEY-ID": client_id,
                        "X-NCP-APIGW-API-KEY": client_secret,
                        "Content-Type": "application/json"
                        }
        self.init_data()

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

    def fetch_contents(self, url):

        html = requests.get(news_test_url).text
        bs_object = BeautifulSoup(html, "html.parser")

        self.data["document"]["title"] = bs_object.select(PARSER["electimes"]["title_selector"])[0].text.strip()

        news_raw_text = bs_object.select(PARSER["electimes"]["content_selector"])[0].text.strip()
        self.data["document"]["content"] = re.sub("\n+"," ",news_raw_text)


    def send_data_to_telegram(self):
        response = requests.post(REQUEST_URL, data=json.dumps(self.data), headers=self.headers)
        if(response.status_code == 200):
            print (response.text)



try:
    with open("api_info.txt", "r") as f:
        client_id = f.readline().replace("\n","")
        client_secret = f.readline().replace("\n","")
        bot = SummarizerBot(client_id, client_secret)

except FileNotFoundError:
    with open("api_info.txt", "w") as f:
        f.write("Replace this with your client_id(example: oawv4qurkm)\nReplace this with your client_secret(example: x2gds3M35LT419asdsadqtggZhSq6gBojKQwVY)")
        print("You will need Naver API client. I'll make you a info file. Fill the file with content and try again.")

news_test_url = "https://www.electimes.com/news/articleView.html?idxno=302222"
bot.fetch_contents(news_test_url)
bot.send_data_to_telegram()









