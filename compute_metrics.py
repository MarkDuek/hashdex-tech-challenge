import pandas as pd
import numpy as np
from scipy.stats import norm

def compute_sigma_daily(assets_allocation: dict, df: pd.DataFrame, df_returns: pd.DataFrame, ewma_decay, initial_sigma=0.0):
    # Initialize the omega DataFrame
    omega = pd.DataFrame()
    for asset, allocation in assets_allocation.items():
        omega[asset] = allocation * df[asset]

    n_times, n_assets = df.shape
    cov = np.zeros((n_assets, n_assets, n_times))

    # Set the initial covariance for all asset pairs
    cov[:, :, 0] = initial_sigma

    # Compute the covariance matrix using EWMA
    for t in range(n_times-1):
        for i in range(n_assets):
            for j in range(n_assets):
                # Only compute covariance for valid returns (not NaN)
                if not np.isnan(df_returns.iloc[t, i]) and not np.isnan(df_returns.iloc[t, j]):
                    cov[i, j, t+1] = ewma_decay * cov[i, j, t] + (1-ewma_decay) * df_returns.iloc[t, i] * df_returns.iloc[t, j]

    # Now compute sigma_daily for all days (even if some values are NaN)
    cols = [col for col in df.columns]

    omega_array = omega[cols].to_numpy()  # shape: (n_times, n_assets)
    sigma_daily = np.zeros(n_times)

    for t in range(n_times):
        # Mask out NaN values for each day
        valid_assets = ~np.isnan(omega_array[t])  # Get boolean array of valid (non-NaN) assets
        omega_valid = omega_array[t, valid_assets]  # Only consider valid omega values
        cov_valid = cov[valid_assets, :, t][:, valid_assets]  # Submatrix of cov for valid assets

        # Calculate portfolio risk for the valid assets
        sigma_daily[t] = omega_valid.T @ cov_valid @ omega_valid

    return np.sqrt(sigma_daily)


def compute_daily_var(sigma_daily, alpha):
    # bilateral
    z_alpha_bilateral = norm.ppf(1 - alpha / 2)
    return z_alpha_bilateral * sigma_daily