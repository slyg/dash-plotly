def select_project(df, project):
    if project == 'all':
        return df
    else:
        return df[df['job_name'].str.contains(project) == True]


nightly_flag = "HMCTS_Nightly"


def select_type(df, pipeline_type):
    if pipeline_type == 'nightly':
        return df[df['job_name'].str.contains(nightly_flag) == True]
    elif pipeline_type == 'non-nightly':
        return df[df['job_name'].str.contains(nightly_flag) == False]
    else:
        return df


def select(df, pipeline_type, project):
    return select_project(select_type(df, pipeline_type), project)
