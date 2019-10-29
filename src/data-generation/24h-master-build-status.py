import datetime
import os

import azure.cosmos.cosmos_client as cosmos_client
import pandas as pd

client = cosmos_client.CosmosClient(url_connection=os.environ['endpoint'], auth={
                                    'masterKey': os.environ['masterKey']})

database_link = 'dbs/' + os.environ['databaseId']
collection_link = database_link + '/colls/{}'.format(os.environ['containerId'])

oneDayAgo = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()

query = {
    "query": """
     SELECT c.job_name, c.build_id, c.current_build_current_result, c.stage_timestamp, c._ts
     FROM c
     WHERE c.current_build_scheduled_time > '{0}Z'
         and c.branch_name = 'master'
    """.format(oneDayAgo)
}

query_results = list(client.QueryItems(collection_link, query))

df = pd.DataFrame(query_results)

last_builds = pd.DataFrame(
    df
    .sort_values(by='stage_timestamp')
    .drop_duplicates('job_name', keep='last')
)

df.to_pickle('data/24h-master-build-status.pkl')
