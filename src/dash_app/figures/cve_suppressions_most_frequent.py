import pandas as pd
import plotly.express as px

df = pd.read_csv('data/cve_suppressions.csv')


def get_fig():
    cve_stuff = df.groupby(
        'CVE')['Team'].nunique().sort_values(ascending=False)
    cve_df = pd.DataFrame({'CVE': cve_stuff.index, 'Count': cve_stuff.values})
    return px.bar(cve_df, x='CVE', y='Count')
