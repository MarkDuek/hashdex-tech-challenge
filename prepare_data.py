import subprocess
import os
import constants
import pandas as pd


def download_and_unzip(years, download_dir="data"):
    base_url = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{}.ZIP"

    # Create the data directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for year in years:
        # Construct the URL for the specified year
        url = base_url.format(year)

        # Define the file paths
        zip_file_path = os.path.join(download_dir, f"COTAHIST_A{year}.ZIP")
        unzip_dir = os.path.join(download_dir, str(year))

        # Download the file using wget with --no-check-certificate
        try:
            print(f"Downloading data for {year}...")
            subprocess.run(
                ["wget", "--no-check-certificate", url, "-O", zip_file_path], check=True
            )
            print(f"Downloaded {zip_file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading file for {year}: {e}")
            continue

        # Unzip the downloaded file
        if not os.path.exists(unzip_dir):
            os.makedirs(unzip_dir)

        try:
            print(f"Unzipping data for {year}...")
            subprocess.run(["unzip", "-o", zip_file_path, "-d", unzip_dir], check=True)
            print(f"Unzipped {zip_file_path} to {unzip_dir}")
        except subprocess.CalledProcessError as e:
            print(f"Error unzipping file for {year}: {e}")
            continue


def read_data(years, data_dir="data"):
    # Define the fixed widths for each field according to the layout:
    widths = constants.widths
    col_names = constants.col_names

    all_data = []

    for year in years:
        # Define the path to the unzipped directory for the year
        unzip_dir = os.path.join(data_dir, str(year))

        if os.path.exists(unzip_dir):
            # List all TXT files in the directory (case insensitive)
            txt_files = [f for f in os.listdir(unzip_dir) if f.upper().endswith(".TXT")]

            for txt_file in txt_files:
                file_path = os.path.join(unzip_dir, txt_file)
                print(f"Reading {file_path}...")

                try:
                    # Read the fixed-width file using the defined widths and column names
                    df = pd.read_fwf(
                        file_path, widths=widths, names=col_names, dtype=str
                    )

                    # Optionally, filter for only data records ("01") if header ("00") and trailer ("99") are included:
                    df = df[df["TIPREG"] == "01"].copy()

                    all_data.append(df)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue
        else:
            print(f"No data found for year {year} at {unzip_dir}")

    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)

        # Optional: Convert fields to proper data types
        # Convert date field (DATA_PREGAO) from string to datetime
        combined_data["DATA_PREGAO"] = pd.to_datetime(
            combined_data["DATA_PREGAO"], format="%Y%m%d"
        )

        # Convert numeric fields (prices, volumes, etc.)
        # Prices are stored with an implicit two decimal places (V99 format)
        price_cols = [
            "PREABE",
            "PREMAX",
            "PREMIN",
            "PREMED",
            "PREULT",
            "PREOFC",
            "PREOFV",
            "PREEXE",
            "PTOEXE",
        ]
        for col in price_cols:
            # Convert to numeric and adjust by dividing by 100 to get the proper decimal value
            combined_data[col] = (
                pd.to_numeric(combined_data[col], errors="coerce") / 100
            )

        # Convert integer fields
        int_cols = ["TOTNEG", "FATCOT", "DISMES"]
        for col in int_cols:
            combined_data[col] = pd.to_numeric(
                combined_data[col], errors="coerce", downcast="integer"
            )

        # If desired, convert QUATOT and VOLTOT (which are large numbers) to numeric
        for col in ["QUATOT", "VOLTOT"]:
            combined_data[col] = pd.to_numeric(combined_data[col], errors="coerce")

        return combined_data
    else:
        print("No data was loaded.")
        return None


def get_filtered_history(df, assets_allocation):
    # Filter the dataframe using the keys of assets_allocation
    filtered_df = df[df['CODNEG'].isin(assets_allocation.keys())].copy()

    # Pivot dataframe to get DATA_PREGAO as index
    pivot_df = filtered_df.pivot(index='DATA_PREGAO', columns='CODNEG', values='PREULT')
    pivot_df.sort_index(inplace=True)
    pivot_df = pivot_df.reindex(sorted(pivot_df.columns), axis=1)

    return pivot_df

