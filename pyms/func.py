import requests
import re
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}


def getGupsik(school):
    return requests.get(f'http://52.79.217.253:5000/menu/{school}').text.split()


def getSchedule(school, grade, cls):
    return requests.get(f'http://52.79.217.253:5000/schedule/{school}/{grade}/{cls}', verify=False).text


def shortschool(school_name):
    if school_name[-4:] == "초등학교" or school_name[-4:] == "고등학교":
        return school_name[:-4]
    elif school_name[-3:] == "중학교":
        return school_name[:-3]
    elif school_name[-1] == "초" or school_name[-1] == "중" or school_name[-1] == "고":
        return school_name[:-1]
    else:
        return school_name




# 초등학교, 중학교, 고등학교
# 초, 중, 고