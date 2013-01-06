PythonFinance
=============

basic Finance Utilities for Python

Requirements
------------

1. Python >= 3
2. numpy
3. scipy
4. pandas

Features
--------

1. Data Manager 
	- Automatic download data from Yahoo! Finance
	- Get only interested information: dates and fields (Adj Close, Volume, ...)
	- Serialization (pickle) of data with custom names
2. Calculator Utils
	- Present Value, Future Value
	- Rates (Annual Rate)
	- Efective Annual Return
	- Number of Periods
	- Total return
	- Daily returns
	- Sharpe ratio
3. Date Utils: to handle open NYSE Dates
	- open dates between two dates + back and forward windows
	- add and substract dates
4. Market Simulator: Simulates a list of orders
	- Automatically download necessary data
	- Can load the trades from a CSV file
	- Can use custom list of orders (usually from the EventFinder)

### Event Study ###

1. PastEvent: Analysis of an specific event:
	- Allows specific event window and estimation period
	- Expected Returns
	- Abnormal Returns
	- Cumulative Abnormal Returns

2. EventFinder: Find events on data

3. MultipleEvent: Analysis of a list of events
	- Allows specific event window and estimation period
	- Expected Returns
	- Abnormal Returns
	- Cumulative Abnormal Returns
	- Plot with error bars


How to use it
-------------

The easiest way is to look at the examples folder (some are .py files, some are ipython notebooks) this folder is ussualy updated. Also note that the most most updated examples are the test of each module.

For more information (but possible un-updated) can see my blog: [ctrl68.wordpress.com](http://ctrl68.wordpress.com/category/python/pythonfinance/)
