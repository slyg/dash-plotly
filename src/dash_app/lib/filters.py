def select(df, pipeline_type, project):

    if pipeline_type == 'nightly':
        df = df[df['job_name'].str.contains(
            "HMCTS_Nightly") == True]
    elif pipeline_type == 'non-nightly':
        df = df[df['job_name'].str.contains(
            "HMCTS_Nightly") == False]
    else:
        df = df

    if project == 'all':
        return df
    else:
        return df[df['job_name'].str.contains(project) == True]
