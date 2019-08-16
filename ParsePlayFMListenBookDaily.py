import requests
from bs4 import BeautifulSoup
import urllib
import urllib.parse as urlparse
from urllib.parse import urlencode
import json
import ssl
import os.path
from os import path


def download_mp3_file(mp3_url, mp3_title):
    urllib.request.urlretrieve(mp3_url, mp3_title)

def generate_episodes_url(base_url, data_offset):
    url_parts = list(urlparse.urlparse(base_url))
    params = {'episode_offset': data_offset}
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    print(urlparse.urlunparse(url_parts))
    return urlparse.urlunparse(url_parts)

def get_base_json_url():
    response = requests.get("https://player.fm/series/series-1516573")
    # print(response.text);
    soup = BeautifulSoup(response.text, "html.parser");
    href = soup.find_all("section", class_="series-episodes-list")[0]
    return  href

def get_episodes(offset_url):
    json_response = requests.get(offset_url)
    json_data = json.loads(json_response.text)
    episodes = json_data["episodes"]
    return episodes

def refact_file_name(file_name):
    temps = file_name.split(" ")
    print(temps)


    return temps[len(temps)-1]+" "+temps[0]+".mp3"
print("start")
ssl._create_default_https_context = ssl._create_unverified_context

href = get_base_json_url()
json_url = "https://player.fm/" + href["data-url"]

data_limit = int(href["data-limit"])
data_offset = 700
    # int(href["data-offset"])

while True:
    offset_url = generate_episodes_url(json_url, data_offset)
    episodes = get_episodes(offset_url);
    if(len(episodes) == 0):
        break
    for episode in episodes:
        mp3_url = episode["url"]

        mp3_title = refact_file_name(episode["title"].replace("|", "").replace("/",""))


        print("Downloading" + mp3_title +" from "+mp3_url)
        if not(path.exists(mp3_title)):
           download_mp3_file(mp3_url, mp3_title)
    data_offset += data_limit
    print(data_offset)

print("The end")




