import unittest
import warnings

import pandas as pd
import pandas.testing as pd_testing
from dash_apps.lib.filters import select_project, select_type


class TestSelectProject(unittest.TestCase):

    def createTestDataFrames(self):
        data = {'job_name': ['SSCS', 'Platform', 'DIV'],
                'data': ['10', '10', '10'], }
        data_subset = {'job_name': ['SSCS'], 'data': ['10']}
        return (pd.DataFrame(data), pd.DataFrame(data_subset))

    def test_it_will_return_the_initial_df_when_selecting_all(self):
        (df, _) = self.createTestDataFrames()
        pd_testing.assert_frame_equal(
            select_project(df, 'all').reset_index(drop=True),
            df.reset_index(drop=True)
        )

    def test_it_will_return_the_selected_df_subset(self):
        (df, df_subset) = self.createTestDataFrames()
        pd_testing.assert_frame_equal(
            select_project(df, 'SSCS').reset_index(drop=True),
            df_subset.reset_index(drop=True)
        )


class TestSelectType(unittest.TestCase):

    def createTestDataFrames(self):
        data = {
            'job_name': ['HMCTS/SSCS', 'HMCTS_Nightly/SSCS', 'HMCTS/DIV', 'HMCTS_Nightly/DIV'],
            'data': ['10', '10', '10', '10']}
        data_subset_non_nightly = {
            'job_name': ['HMCTS/SSCS', 'HMCTS/DIV'],
            'data': ['10', '10']}
        data_subset_nightly = {
            'job_name': ['HMCTS_Nightly/SSCS', 'HMCTS_Nightly/DIV'],
            'data': ['10', '10']}
        return (pd.DataFrame(data),
                pd.DataFrame(data_subset_nightly),
                pd.DataFrame(data_subset_non_nightly)
                )

    def test_it_will_return_the_nightly_jobs(self):
        (df, df_nightly, _) = self.createTestDataFrames()
        pd_testing.assert_frame_equal(
            select_type(df, 'nightly').reset_index(drop=True),
            df_nightly.reset_index(drop=True)
        )

    def test_it_will_return_the_selected_df_subset(self):
        (df, _, df_non_nightly) = self.createTestDataFrames()
        pd_testing.assert_frame_equal(
            select_type(df, 'non-nightly').reset_index(drop=True),
            df_non_nightly.reset_index(drop=True)
        )
