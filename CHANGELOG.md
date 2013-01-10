PythonFinance
=============

v0.04 - Dev
-----------
- new Condition class to mark events on the Finder
- new FinaceTest to easier testing
- Rename BasicUtils to Calculator
- Add more utils to the Calculator:
	- Future Value
	- Present Value
	- Rates (Annual rate)
	- Number of periods (n)
	- Efective annual return
	- Improve total_return to give return by position
	- Rename daily_returns to just returns
	- Add Continusly compouding to total_return and returns
- Calculator Tests based on CSV files
- A lot of more examples

v0.035
------
- Integration between the EventFinder and MarketSimulator
- MultipleEvents:
	- Add: Plot with error bars

v0.03
-----
- Bug fixes on FileManager and DataAccess
- Create DateUtils:
	- Get dates from NYSE
	- Ask for more specific dates
	- Ask for dates between a date
- Create ListUtils:
	- Dates from NYSE
	- S&P 500 symbols for some years
- Create PastEvent: Analysis of an specific event:
	- Allows specific event window and estimation period
	- Expected Returns
	- Abnormal Returns
	- Cumulative Abnormal Returns
- Create EventFinder: Find events on data
- Create MultipleEvent: Analysis of a list of events: std, mean
	- Allows specific event window and estimation period
	- Expected Returns
	- Abnormal Returns
	- Cumulative Abnormal Returns

v0.02
-----
- Create MarketSimulator: Simulate orders of trades
- Data Access
	- CHANGE: index of the DataFrame to DatetimeIndex not string
	- Moved the module folder from ‘./data/’ to ‘./utils/’
- Create Basic Utils:
	- Total Return
	- Daily Return
	- Sharpe Ratio

v0.01
-----
- Create FileManager: Download information from Yahoo! Finance
- Create DataAccess: Manage the downloaded information
	- Ask for specific dates and fields of the data
	- Returns pandas.DataFrame
	- Serialization of the data