# hashdex-tech-challenge
# Risk Controls and ETF VaR Calculation Project

This project calculates the parametric Value-at-Risk (VaR) and creates a control report for market, credit, and liquidity metrics for a portfolio of ETFs.
This is the portfolio we are working with:

| **Asset**  | **Allocation** |
|--------|------------|
| HASH11 | 20000      |
| SOLH11 | 30000      |
| ETHE11 | 10000      |

## Project Overview

The goal of this project is to:
- Automatically extract historical prices for ETFs from the B3 website.
- Calculate the daily VaR for a portfolio of ETFs using a parametric approach.
- Create a report for control metrics for market, credit, and liquidity risk.

## Data Sources & References

### Historical Data Extraction
- **B3 Historical Series:**  
  Extract historical prices for ETFs by downloading the annual series files from [B3 Market Data](http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-avista/series-historicas/).  
- **Example (2024):**  
  [COTAHIST_A2024.ZIP](http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2024.ZIP)
- **File Layout Info:**  
  [SeriesHistoricas Layout PDF](http://www.b3.com.br/data/files/C8/F3/08/B4/297BE410F816C9E492D828A8/SeriesHistoricas_Layout.pdf)


## Project Structure

```plaintext
├── README.md
├── requirements.txt
├── asset_risk_analysis.ipynb     # Main notebook for running the project
├── compute_metrics.py            # Risk metric functions
├── constants.py                  # B3 Data layout constants
├── data/                         # Folder to store downloaded historical files
├── images/                       # Folder to save images 
└── tests/                       
    ├── conftest.py               # Script to declare test fixtures
    └── test_var.py               # Script testing metrics functions
``` 