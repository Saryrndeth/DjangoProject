import requests
import re
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}


def getGupsik(school):
    return requests.get(f'http://52.79.217.253:5000/menu/{school}').text.split()

# def getGupsik(school):
#     if school == "선린인터넷고등학교":
#         page = requests.get("https://sunrint.sen.hs.kr/index.do",  verify=False)
#         soup = BeautifulSoup(page.text, "html.parser")
#
#         element = soup.select(
#             '#index_board_mlsv_03_195699 > div > div > div > div > ul:nth-child(1) > li > dl > dd > p.menu')
#
#         result = str(element).replace(' ', '').replace('   ', '')
#
#         result = result[result.find(">") + 1:result.rfind("<")]
#
#         result = result[13:-22]
#         result = re.sub("[0-9]+\.", "", result)
#
#         if result == '':
#             return False
#         return result
#     else:
#         return "개발중"