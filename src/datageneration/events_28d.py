import datetime
import json
from os import path

import azure.cosmos.cosmos_client as cosmos_client
import pandas as pd
from cosmos_client import client, collection_link

today = datetime.date.today()
one_day = datetime.timedelta(days=1)

# Number of days we want to go back in
days_in_past = 28
branch = 'master'
start_date = (today - (days_in_past * one_day)).isoformat()

query = {
    "query": """
     SELECT c.id, c.build_tag, c.job_name, c.build_id, c.current_build_current_result, c.stage_timestamp, c._ts, c.current_build_scheduled_time
     FROM c
     WHERE c.current_build_scheduled_time > '{0}00:01:00.000Z'
         and c.branch_name = '{1}'
    """.format(start_date, branch)
}

query_results = list(client.QueryItems(collection_link, query))

df = pd.DataFrame(query_results)

panda_record_filename = path.splitext(path.basename(__file__))[0]

df.to_pickle('data/{0}.pkl'.format(panda_record_filename))
with open('data/{0}.json'.format(panda_record_filename), 'w') as outfile:
    json.dump({
        'days_in_past': days_in_past,
        'start_date': str(start_date),
        'branch': branch
    }, outfile)
