
__all__ = [
    'register_to_clearml',
    'get_clearml_dataset'
]

import logging
import re
from typing import List, Optional

import pandas as pd

from clearml import Dataset
import tempfile

url_regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def get_clearml_dataset(
    dataset_id: Optional[str] = None,
    dataset_project: Optional[str] = None,
    dataset_name: Optional[str] = None,
    alias: Optional[str] = None
):
    """Gets a local copy of ClearML Dataset
    Args:
        dataset_id: Requested dataset ID
        dataset_project: Requested dataset project name
        dataset_name: Requested dataset name
        alias: Alias of the dataset. If set, the 'alias : dataset ID' key-value pair
            will be set under the hyperparameters section 'Datasets'
    Example:
        The example shows how to get a local copy of ClearML Dataset by dataset_id
        >>> get_clearml_dataset(dataset_id=dataset_id)
        ...
    """
    if not (all([dataset_project, dataset_name]) or dataset_id):
        raise ValueError("Either dataset_project and dataset_name or dataset_id should be provided")

    dataset = Dataset.get(
        dataset_id=dataset_id,
        dataset_project=dataset_project,
        dataset_name=dataset_name,
        alias=alias
    )
    folder = dataset.get_local_copy()

    return folder


def register_to_clearml(
    toloka_df: pd.DataFrame,
    toloka_dataset_path: Optional[str] = None,
    external_url_columns: Optional[List[str]] = None,
    dataset_project: Optional[str] = None,
    dataset_name: Optional[str] = None,
    parent_dataset_ids: Optional[List[str]] = None,
    verbose: bool = False
) -> None:
    """Registers a new Dataset to ClearML containing files annotated by Toloka
    Args:
        toloka_df: pandas Dataframe containing data from Toloka
        toloka_dataset_path: path to store `toloka_df` locally. This is a temp file used to register to clearml
        dataset_project: Project containing the dataset in ClearML.
        dataset_name: Naming the new dataset in ClearML
        parent_dataset_id: Parent dataset ID
        external_url_columns: columns containing external urls. If specified, the URLs in the columns will be added to the clearml Dataset
                              as links and can be retrieved when calling get_clearml_dataset
        verbose: If True print to console files added/modified
    Examples:
        The example shows how register  a new Dataset in ClearML.
        >>> answers_df = toloka_client.get_assignments_df(pool_id='1')
        >>> register_to_clearml(toloka_df=answers_df,
        >>>             dataset_project='ClearMLProject', dataset_name='TolokaDataset')
        ...
        The example shows how to register a new Dataset in ClearML as a child Dataset.
        >>> answers_df = toloka_client.get_assignments_df(pool_id='1')
        >>> parent_dataset_id = # id of Dataset from ClearML
        >>> register_to_clearml(parent_dataset_ids=parent_dataset_id, toloka_df=answers_df,
        >>>                     dataset_project='ClearMLProject', dataset_name='TolokaDataset')
        ...
    """
    if not (all([dataset_project, dataset_name]) or parent_dataset_ids):
        raise ValueError("Either dataset_project and dataset_name or parent_dataset_id should be provided")

    if not parent_dataset_ids:
        dataset = Dataset.create(
            dataset_project=dataset_project,
            dataset_name=dataset_name
        )
    else:
        parent = Dataset.get(dataset_id=parent_dataset_ids)
        dataset = Dataset.create(
            dataset_project=parent.project if not None else parent.project,
            dataset_name=parent.name if not None else parent.name,
            parent_datasets=[parent_dataset_ids]
        )

    toloka_csv_file = toloka_dataset_path if toloka_dataset_path is not None else '{}/toloka_ds_temp.csv'.format(tempfile.gettempdir())
    toloka_df.to_csv(toloka_csv_file, index=False)
    dataset.add_files(path=toloka_csv_file, verbose=verbose)

    if external_url_columns is not None:
        for column_name in toloka_df.columns:
            # if column_name.startswith('INPUT:') or column_name.startswith('GOLDEN:') or column_name.startswith('OUTPUT:'):
            if column_name in external_url_columns:
                sample_value = toloka_df[column_name].iloc[0]
                if isinstance(sample_value, str) and re.match(url_regex, sample_value) is not None:
                    dataset.add_external_files(source_url=toloka_df[column_name].dropna().tolist(), recursive=False, verbose=verbose)

    dataset.upload(verbose=verbose)
    dataset.finalize(verbose=verbose)

    logging.info('Dataset registered in ClearML.Dataset ID is:{}'.format(dataset.id))
