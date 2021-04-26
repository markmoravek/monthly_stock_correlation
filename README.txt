**Make sure you are using the most recent version of pandas

pip install numpy
pip install pandas
pip install pandas_datareader
run ticker_correlation.py from cmd or terminal

Summary
-Accepts user input of two stock tickers and fetches price data from Yahoo Finance into a dataframe.
-Dataframe is then split into groups to calculate the monthly price change correlation between the two.
-Dataframes are then merged to show the last recorded stock price of the month along with the monthly correlation information.
-Used for analysis to forecast stock movement.
