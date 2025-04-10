import pytest
import numpy as np
from compute_metrics import compute_sigma_daily


@pytest.mark.parametrize("initial_sigma", [0.0])
@pytest.mark.parametrize("ewma_decay", [0.2])
def test_sigma_daily_nan_values(asset_df, df_returns, ewma_decay, initial_sigma, asset_allocations, nan_values):
    subset = list(set(asset_allocations.keys()) - set(nan_values.keys()))
    null_mask = list(nan_values.values())[0]

    sub_assets_allocation = {asset: allocation for asset, allocation in asset_allocations.items() if asset in subset}
    sub_df = asset_df[subset]
    sub_df_returns = df_returns[subset]

    sigma_daily_sub = compute_sigma_daily(sub_assets_allocation, sub_df, sub_df_returns, ewma_decay, initial_sigma)
    sigma_daily_full = compute_sigma_daily(asset_allocations, asset_df, df_returns, ewma_decay, initial_sigma)

    assert np.allclose(sigma_daily_sub[null_mask], sigma_daily_full[null_mask])
