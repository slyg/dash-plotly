import json
import re
import urllib
import xml.etree.ElementTree as et
from csv import DictWriter
from os import environ

import numpy as np
import pandas as pd
from requests import get

GITHUB_TOKEN = environ['githubtoken']
API_CODE_SEARCH_BASE = "https://api.github.com/search/code"
SUPPRESSIONS_QUERY = "org:hmcts+path:/+filename:dependency-check-suppressions.xml"


def get_repos_for_code_search(query):
    url = "{}?q={}".format(API_CODE_SEARCH_BASE, query)
    return get(url, headers={"Authorization": "token {}".format(GITHUB_TOKEN)}).json()


def get_cves_from_url(url):
    response = urllib.request.urlopen(url).read()
    xtree = et.ElementTree(et.fromstring(response))
    cve_nodes = xtree.findall(
        './/{https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.1.xsd}cve')
    return [node.text for node in cve_nodes]


def suppressions_lens(item):
    full_name = item['repository']['full_name']
    file_url = 'https://raw.githubusercontent.com/{0}/master/dependency-check-suppressions.xml'.format(
        full_name)
    return {'team': re.match(r'(?P<org>\w+)/(?P<team>\w+)', full_name).group('team'),
            'full_name': full_name,
            'cve_suppressions': get_cves_from_url(file_url)
            }


def item_unfold(item):
    return [
        {'Team': item['team'],
         'Project': item['full_name'],
         'CVE': cve_suppression
         } for cve_suppression in item['cve_suppressions']
    ]


data = get_repos_for_code_search(SUPPRESSIONS_QUERY)
search_results = list(map(suppressions_lens, data['items']))

df = pd.DataFrame.from_records(np.concatenate(
    [item_unfold(i) for i in search_results], axis=0))
df.to_csv('data/cve_suppressions.csv', sep=',', encoding='utf-8', index=False)
