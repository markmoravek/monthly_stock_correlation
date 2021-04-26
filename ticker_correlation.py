import numpy as np
import pandas as pd
import pandas_datareader.data as web


class TickerCorrelation:
	"""Manages program"""

	def __init__(self):
		"""Initializes program and creates resources"""
		df = pd.DataFrame()
		corr_df = pd.DataFrame()
		df_master = pd.DataFrame()
		stock1 = ''
		stock2 = ''


	def run_program(self):
		print("In progress...")
		self.input_tickers()
		self.get_stock_data()
		self.first_df_format()
		self.calculate_correlation()
		self.second_df_format()
		self.pct_change_calc()
		self.replace_nan_values()
		self.column_index_sort()
		self.merge_dataframes()
		self.print_to_excel()


	def input_tickers(self):
		"""Prompts for user to input the first stock"""
		self.stock1 = input("Enter the first stock ticker: ")
		self.stock2 = input("Enter the second stock ticker: ")

	
	def get_stock_data(self):
		"""Prompts user to input stocks"""
		#API to get data from Yahoo
		stock_data = {ticker: web.get_data_yahoo(ticker) for ticker in [self.stock1, self.stock2]}
		self.df = pd.DataFrame({ticker: data['Adj Close'] for ticker, data in stock_data.items()})


	def use_test_data(self):
		"""Test data to avoid overusing API"""
		#Sample stock data stored in pickle
		price_pickle = pd.read_pickle('price')
		df = price_pickle
		stock1 = 'AAPL'
		stock2 = 'MSFT'


	def first_df_format(self):
		"""Format data for the first set of calculations"""
		#Convert the index to date
		self.df.index = pd.to_datetime(self.df.index)

		#Create month and year columns
		self.df['tempdate'] = self.df.index
		self.df['MonthTemp'] = self.df['tempdate'].dt.strftime('%b')
		del self.df['tempdate']
		self.df['Day'] = self.df.index.day
		self.df['Year'] = self.df.index.year
		self.df['Month'] = self.df.index.astype(str).str[:7]

		#Create separator column
		self.df['|'] = '|'


	def calculate_correlation(self):

		#Calculate Monthly Correlation
		self.df['dailychange1'] = self.df[self.stock1].pct_change()
		self.df['dailychange2'] = self.df[self.stock2].pct_change()
		self.df['TotalCorrelation'] = self.df['dailychange1'].corr(self.df['dailychange2'])

		#Correlation test section
		self.corr_df = self.df.groupby('Month')[[self.stock1, self.stock2]].corr()
		self.corr_df = self.corr_df.sort_index(ascending=False)
		col1 = self.df.columns[0]
		col2 = self.df.columns[1]
		self.corr_df['MonthlyCorrelation'] = self.corr_df[col1]+self.corr_df[col2] -1
		del self.corr_df[col1]
		del self.corr_df[col2]


	def second_df_format(self):

		#Format index
		self.corr_df = self.corr_df.reset_index(level=1, drop=True).astype(str)
		self.corr_df = self.corr_df.rename_axis('dateindex')

		#add date column to correlation df
		self.corr_df['Month'] = self.corr_df.index

		#del extra columns
		del self.df['dailychange1']
		del self.df['dailychange2']


	def pct_change_calc(self):
		#Create Change % columns
		self.df['Change1'] = self.df[self.stock1].pct_change()
		self.df['Change2'] = self.df[self.stock2].pct_change()

	def replace_nan_values(self):
		#Remove NaN values
		self.df = self.df.replace(np.nan, '', regex=True)

	def column_index_sort(self):
		#Can be used to sort the columns and index
		self.df = self.df.sort_index(ascending=False)

	def merge_dataframes(self):
		#Merge the original dataframe with the calculated correlation dataframe
		self.df_master = pd.merge(self.df, self.corr_df)
		self.df_master = self.df_master.drop_duplicates(['Month'])
		self.df_master = self.df_master[['Month', 'Day', self.stock1, self.stock2,
		'TotalCorrelation', 'MonthlyCorrelation']]

	def print_to_excel(self):
		#Sends the data to excel, returns an error if the target spreadsheet is open.
		try:
			self.df_master.to_csv('TickerCorrelation.csv')
			print("Data printed to 'TickerCorrelation.csv'")
		except PermissionError:
			print(f"\nERROR: Please close 'TickerCorrelation.csv' and try again. :)")

if __name__ == '__main__':
	# Make a game instance, and run the game.
	tc = TickerCorrelation()
	tc.run_program()