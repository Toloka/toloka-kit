import re
from typing import Optional
import pandas as pd
from clearml import Dataset
from typing import List
import tempfile

url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def get_clearml_dataset(

    dataset_id: Optional[str] = None,
    dataset_project: Optional[str] = None,
    dataset_name: Optional[str] = None,
    alias: Optional[str] = None
):
    """
    Downloads a dataset from ClearML into ClearML Cache
    Users must specify either Dataset's ID, or Dataset's project and Dataset's name
    :param str dataset_id: ClearML Dataset's ID
    :param str dataset_project: ClearML Dataset's Project
    :param str dataset_name: ClearML Dataset's Name
    :param str alias: If provided, the Dataset will be saved in the ClearML Task's Hyperparameter section with the specified alias
    :return:
    """
    dataset = Dataset.get(
        dataset_id=dataset_id,
        dataset_project=dataset_project,
        dataset_name=dataset_name,
        alias=alias
    )
    folder = dataset.get_local_copy()

    return folder


def register_to_clearml(
    dataset_project: str,
    dataset_name: str,
    toloka_df: pd.DataFrame,
    parent_dataset_id: Optional[List[str]] = None,
    verbose: Optional[bool] = False
):
    """
    Registers a dataset obtained from Toloka to ClearML using clearml data
    :param str dataset_project: ClearML Project
    :param str dataset_name: ClearML Dataset Name
    :param df toloka_df: Dataframe representing the Dataset, as obtained from Toloka
    :param list parent_dataset_id: The Dataset's parents ID if it has any
    :param bool verbose: Controls Verbosity
    :return:
    """
    if not parent_dataset_id:
        dataset = Dataset.create(
            dataset_project=dataset_project,
            dataset_name=dataset_name
        )
    else:
        parent = Dataset.get(dataset_id=parent_dataset_id)
        dataset = Dataset.create(
            dataset_project=parent.project,
            dataset_name=parent.name,
            parent=parent_dataset_id
        )


    toloka_csv_file = '{}/toloka_ds_temp.csv'.format(tempfile.gettempdir())
    toloka_df.to_csv(toloka_csv_file, index=False)
    dataset.add_files(path=toloka_csv_file, verbose=verbose)

    for column_name in toloka_df.columns:
        if column_name.startswith('INPUT:') or column_name.startswith('GOLDEN:') or column_name.startswith('OUTPUT:'):
            sample_value = toloka_df[column_name].iloc[0]
            if isinstance(sample_value, str) and re.match(url_regex, sample_value) is not None:
                dataset.add_external_files(source_url=toloka_df[column_name].dropna().tolist(), recursive=False, verbose=verbose)

    dataset.finalize(verbose=verbose, auto_upload=True)