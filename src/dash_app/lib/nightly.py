def select(selection, df):
    if selection == 'nightly':
        return df[df['job_name'].str.contains(
            "HMCTS_Nightly") == True]
    elif selection == 'non-nightly':
        return df[df['job_name'].str.contains(
            "HMCTS_Nightly") == False]
    else:
        return df
