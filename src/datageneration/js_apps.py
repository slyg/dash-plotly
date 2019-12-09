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
API_ISSUES_SEARCH_BASE = "https://api.github.com/search/issues"

OUTPUT_FILE = "reports/js-apps-snyk-report.csv"
QUERY_ALL_JS = "org:hmcts+path:/+filename:package.json"
QUERY_WITH_SNYK = "org:hmcts+path:/+filename:package.json+snyk"
QUERY_WITH_NSP = "org:hmcts+path:/+filename:package.json+nsp"
QUERY_DEPENDABOT = "org:hmcts+dependabot"

print("🐶 JS apps security search")


def get_repos_for_code_search(query):
    url = "{}?q={}".format(API_CODE_SEARCH_BASE, query)
    data = get(url, headers={
               "Authorization": "token {}".format(GITHUB_TOKEN)}).json()

    def lens(item): return {'name': item['repository']['name']}
    return map(lens, data['items'])


def get_repos_for_issues_search(query):
    url = "{}?q={}".format(API_ISSUES_SEARCH_BASE, query)
    data = get(url, headers={
               "Authorization": "token {}".format(GITHUB_TOKEN)}).json()

    def lens(item): return {'name': item['repository_url'].rsplit('/', 1)[1]}
    return map(lens, data['items'])


js_projects = np.array(
    list(get_repos_for_code_search(QUERY_ALL_JS)))
sleep(THROTTLING_DELAY)
js_projects_with_snyk = np.array(
    list(get_repos_for_code_search(QUERY_WITH_SNYK)))
sleep(THROTTLING_DELAY)
js_projects_with_nsp = np.array(
    list(get_repos_for_code_search(QUERY_WITH_NSP)))
sleep(THROTTLING_DELAY)
js_projects_with_dependabot = np.array(
    list(get_repos_for_issues_search(QUERY_DEPENDABOT)))


all_concatenated = np.concatenate((
    js_projects,
    js_projects_with_snyk,
    js_projects_with_nsp,
    js_projects_with_dependabot
))

all_projects_sorted = sorted([dict(t) for t in {tuple(d.items()) for d in all_concatenated}],
                             key=lambda item: item['name'])

rows = list(map(lambda item: {
    'Reference': item['name'],
    'nsp (deprecated)': 1 if (item in js_projects_with_nsp) else 0,
    'Dependabot': 1 if (item in js_projects_with_dependabot) else 0,
    'Snyk': 1 if (item in js_projects_with_snyk) else 0
}, all_projects_sorted))

df = pd.DataFrame.from_records(rows)

df.to_csv('data/js_apps_sec_checks.csv',
          sep=',', encoding='utf-8', index=False)
