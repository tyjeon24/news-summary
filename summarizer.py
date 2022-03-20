#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests


import json
import re
import sys

PARSER = {
	"electimes" : {
		"title_selector" : "#article-view > div > header > div.heading-group > h3",
		"content_selector" : "#article-view-content-div"
	}
}

# TODO 1 : 리팩토링(클래스화)
# TODO 3 : 전기신문 리스트에서 링크 뽑아오기 - > 그 링크에서 TODO 2에 해당하는 작업을 수행하는 거임
# TODO 4 : 텔레그램봇 연결해서 보내기.

try:
	with open("api_info.txt", "r") as f:
		client_id = f.readline().replace("\n","")
		client_secret = f.readline().replace("\n","")

except FileNotFoundError:
	with open("api_info.txt", "w") as f:
		f.write("Replace this with your client_id(example: oawv4qurkm)\nReplace this with your client_secret(example: x2gds3M35LT419asdsadqtggZhSq6gBojKQwVY)")
		print("You will need Naver API client. I'll make you a info file. Fill the file with content and try again.")



headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json"
}
language = "ko" # Language of document (ko, ja )
model = "news" # Model used for summaries (general, news)
tone = "2" # Converts the tone of the summarized result. (0, 1, 2, 3)
summaryCount = "3" # This is the number of sentences for the summarized document.
url= "https://naveropenapi.apigw.ntruss.com/text-summary/v1/summarize" 


news_test_url = "https://www.electimes.com/news/articleView.html?idxno=302222"
html = requests.get(news_test_url).text
title = BeautifulSoup(html, "html.parser").select(PARSER["electimes"]["title_selector"])[0].text.strip()

news_raw_text = BeautifulSoup(html, "html.parser").select(PARSER["electimes"]["content_selector"])[0].text.strip()
content = re.sub("\n+"," ",news_raw_text)

data = {
    "document": {
    "title": title,
    "content" : content
    },
    "option": {
    "language": language,
    "model": model,
    "tone": tone,
    "summaryCount" : summaryCount
    }
}
response = requests.post(url, data=json.dumps(data), headers=headers)
rescode = response.status_code
if(rescode == 200):
    print (response.text)
else:
    print("Error : " + response.text)
