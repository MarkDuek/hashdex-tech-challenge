import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def assets():
    return ['HASH11', 'SOLH11', 'ETHE11']


@pytest.fixture
def asset_allocations(assets):
    return {asset: np.random.randint(10000, 100000) for asset in assets}


@pytest.fixture
def n_times():
    return 1000


@pytest.fixture
def n_nan_values():
    return 100


@pytest.fixture
def nan_values(n_times, n_nan_values):
    nan_mask = np.full(n_times, False, dtype=bool)
    nan_mask[:n_nan_values] = True
    return {'SOLH11': nan_mask}


@pytest.fixture
def asset_df(assets, n_times, nan_values):
    df = pd.DataFrame(columns=assets)
    for asset in assets:
        df[asset] = np.random.rand(n_times)
        if asset in nan_values:
            df[asset].iloc[nan_values[asset]] = np.nan
    return df


@pytest.fixture
def df_returns(asset_df):
    return asset_df.pct_change().fillna(0)
