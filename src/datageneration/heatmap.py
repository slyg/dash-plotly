import json
from datetime import datetime, timedelta
from os import environ, path

import azure.cosmos.cosmos_client as cosmos_client
import numpy as np
import pandas as pd

client = cosmos_client.CosmosClient(url_connection=environ['endpoint'], auth={
                                    'masterKey': environ['masterKey']})

database_link = 'dbs/' + environ['databaseId']
collection_link = database_link + '/colls/{}'.format(environ['containerId'])

now = datetime.now()
one_hour = timedelta(hours=1)

# Number of hours we want to go back in
hours_in_past = 24 * 7 * 4

reversed_last_hours = [(now - (i * one_hour)).isoformat()
                       for i in range(hours_in_past + 1)]

last_hours = reversed_last_hours[::-1]

first_hour, *tail_hours = last_hours

query = {
    "query": """
     SELECT c.job_name, c.current_build_current_result, c.stage_timestamp
     FROM c
     WHERE c.current_build_scheduled_time > '{0}Z'
         and c.branch_name = 'master'
    """.format(first_hour)
}

query_results = list(client.QueryItems(collection_link, query))

df = pd.DataFrame(query_results)

panda_record_filename = path.splitext(path.basename(__file__))[0]

df.to_pickle('data/{0}.pkl'.format(panda_record_filename))
with open('data/{0}.json'.format(panda_record_filename), 'w') as outfile:
    json.dump({
        'now': str(now),
        'last_hours': [str(date) for date in last_hours]
    }, outfile)
