import datetime
import json
from os import path

import azure.cosmos.cosmos_client as cosmos_client
import pandas as pd
from cosmos_client import client, collection_link

print("🐶 180 days CI events fetch")

today = datetime.date.today()
one_day = datetime.timedelta(days=1)
one_week = datetime.timedelta(days=7)

# Number of days we want to go back in
days_in_past = 180

reversed_last_days = [(today - (i * one_day)).isoformat()
                      for i in range(days_in_past + 1)]

last_days = reversed_last_days[::-1]

first_day, *tail_days = last_days

query = {
    "query": """
     SELECT c.id, c.build_tag, c.job_name, c.build_id, c.current_build_current_result, c.correlation_id, c.stage_timestamp, c._ts, c.current_build_scheduled_time
     FROM c
     WHERE c.current_build_scheduled_time > '{0}00:01:00.000Z'
         and c.branch_name = 'master'
    """.format(first_day)
}

query_results = list(client.QueryItems(collection_link, query))

df = pd.DataFrame(query_results)

panda_record_filename = path.splitext(path.basename(__file__))[0]

df.to_pickle('data/{0}.pkl'.format(panda_record_filename))
with open('data/{0}.json'.format(panda_record_filename), 'w') as outfile:
    json.dump({
        'days_in_past': str(days_in_past),
        'last_days': [str(date) for date in last_days]
    }, outfile)
