import json
import re
import urllib
import xml.etree.ElementTree as et
from csv import DictWriter
from os import environ
from time import sleep

import numpy as np
import pandas as pd
from requests import get
from utils import THROTTLING_DELAY

GITHUB_TOKEN = environ['githubtoken']
API_CODE_SEARCH_BASE = "https://api.github.com/search/code"
QUERY_DOCKER_BASE_IMAGES = "org:hmcts+path:/+filename:Dockerfile+FROM+node"

print("🐶 nodeJS apps versions search")


def get_repos_for_code_search(query):
    sleep(THROTTLING_DELAY)
    url = "{}?q={}".format(API_CODE_SEARCH_BASE, query)
    response = get(url, headers={
        "Authorization": "token {}".format(GITHUB_TOKEN)})
    def lens(item): return {'name': item['repository']['name'], 'raw_url': item['html_url'].replace(
        'github.com', 'raw.githubusercontent.com').replace('/blob', '')}
    if response.status_code == 200:
        data = response.json()
        return map(lens, data['items'])
    else:
        print("received {0} response from {1}".format(
            response.status_code, url))
        return []


def extract_node_version(project):
    sleep(THROTTLING_DELAY)
    response = get(project['raw_url'])
    name = project['name']
    regex = r"hmctspublic.azurecr.io/base/node[/:](.*?)[:\s]|node[/:](.*?)[:\s]"
    search_result = re.findall(regex, response.text)
    try:
        version = next(v for v in list(search_result[0]) if v)
        return {'name': name, 'version': version}
    except:
        return None


def remove_none_elements(list):
    return [e for e in list if e != None]


js_projects = list(get_repos_for_code_search(QUERY_DOCKER_BASE_IMAGES))
results = remove_none_elements(list(map(extract_node_version, js_projects)))
df = pd.DataFrame.from_records(results).sort_values(by='version')

df.to_csv('data/node-versions.csv', sep=',',
          encoding='utf-8', index=False)
