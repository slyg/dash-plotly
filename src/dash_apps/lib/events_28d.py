import json
import os.path as path
import time
from datetime import datetime

import pandas as pd

data_set_file = 'data/events_28d.pkl'
meta_file = 'data/events_28d.json'

creation_time = time.ctime(path.getctime(data_set_file))

with open(meta_file) as json_file:
    data = json.load(json_file)
    branch = data['branch']
    start_date = data['start_date']
    days_in_past = data['days_in_past']

events = dict(df=pd.read_pickle(data_set_file),
              creation_time=creation_time,
              creation_time_iso=datetime.strptime(
                  creation_time, "%a %b %d %H:%M:%S %Y"),
              branch=branch,
              start_date=start_date,
              days_in_past=days_in_past)
