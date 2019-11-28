import pandas as pd
import plotly.express as px

df = pd.read_csv('data/cve_suppressions.csv')


def get_fig():

    stuff = df.groupby('Team')['CVE'].nunique().sort_values(ascending=False)
    stuff_df = pd.DataFrame({'Team': stuff.index, 'Count': stuff.values})

    return px.bar(stuff_df, x='Team', y='Count')
