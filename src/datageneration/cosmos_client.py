from os import environ

import azure.cosmos.cosmos_client as cosmos_client

client = cosmos_client.CosmosClient(url_connection=environ['endpoint'], auth={
                                    'masterKey': environ['masterKey']})

database_link = 'dbs/' + environ['databaseId']
collection_link = database_link + '/colls/{}'.format(environ['containerId'])
