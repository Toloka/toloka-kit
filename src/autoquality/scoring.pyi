__all__ = [
    'default_calc_scores',
    'default_calc_ranks',
]
import pandas
import toloka.client
import typing


def default_calc_scores(
    toloka_client: toloka.client.TolokaClient,
    pool_id: str,
    label_field: str
) -> typing.Dict[str, typing.Any]:
    """Calculate default scores for Autoquality.

    Args:
        toloka_client: `TolokaClient` instance to interact with requester's account
        pool_id: Pool ID to calculate scores for
        label_field: Target output field

    Returns:
        typing.Dict: Dict with scores
    """
    ...


def default_calc_ranks(scores_df: pandas.DataFrame) -> pandas.DataFrame:
    """Calculate default pool ranks for autoquality

    Args:
        scores_df: pandas.DataFrame with `pool_id` column and columns with scores from `default_calc_scores`

    Returns:
        pandas.DataFrame: input DataFrame with an additional ranks columns
    """
    ...
