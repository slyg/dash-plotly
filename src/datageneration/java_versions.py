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
QUERY_DOCKER_BASE_IMAGES = "org:hmcts+path:/+filename:Dockerfile+hmctspublic.azurecr.io/base/java"

print("🐶 JAVA apps versions search")


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


def extract_java_version(project):
    sleep(THROTTLING_DELAY)
    response = get(project['raw_url'])
    return {'name': project['name'], 'version': re.findall(r"hmctspublic.azurecr.io/base/java:(.*?)\s", response.text)[0]}


def infer_simple_version(raw_version):
    return re.findall(r'\d+', raw_version)[0]


projects = list(get_repos_for_code_search(QUERY_DOCKER_BASE_IMAGES))
results = list(map(extract_java_version, projects))
df = pd.DataFrame.from_records(results).sort_values(by='version')
df['simple version'] = df['version'].apply(infer_simple_version)

df.to_csv('data/java-versions.csv', sep=',', encoding='utf-8', index=False)
