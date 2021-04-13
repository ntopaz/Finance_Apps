# Finance_Apps
Collection of scripts for analyzing and backtesting financial data

## Compare strategy of lump sum investing on first of each month versus spending same monthly investment over course of the first occuring X red days

compare_dca_lumpsum.py
```
usage: compare_dca_lumpsum.py [-h] [-b STARTING_BALANCE] [-a MONTHLY_INVESTMENT] [-t RED_DAY_THRESHOLD] [-m MAX_TIMES_TO_INVEST_EACH_MONTH] -s STOCK [-i INTEREST]

Compare investing strategy of buying on 1st of month versus on first occuring red days

optional arguments:
  -h, --help            show this help message and exit
  -b STARTING_BALANCE, --starting_balance STARTING_BALANCE
                        Starting amount (default=0)
  -a MONTHLY_INVESTMENT, --monthly_investment MONTHLY_INVESTMENT
                        Dollar amount to invest each month (default=500)
  -t RED_DAY_THRESHOLD, --red_day_threshold RED_DAY_THRESHOLD
                        Red day threshold - invest if security drops at least this much in percentage (default=0.5%)
  -m MAX_TIMES_TO_INVEST_EACH_MONTH, --max_times_to_invest_each_month MAX_TIMES_TO_INVEST_EACH_MONTH
                        Invest money over the course of the first occuring N red days (default=2)
  -s STOCK, --stock STOCK
                        Stock or ETF to run this analysis for (from Yahoo finance API)
  -i INTEREST, --interest INTEREST
                        Assumed annual savings interest rate to keep money in while waiting to invest it (default=1%)
```
