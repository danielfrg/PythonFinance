from datetime import datetime
from finance.utils.BasicUtils import *
from finance.sim import MarketSimulator

sim = MarketSimulator('../sim/test/data')
sim.initial_cash = 1000000
sim.simulate("MarketSimulator_orders.csv")

print(sim.portfolio[0:10])
#print(sim.portfolio.ix[datetime(2011, 2, 18)])

print('Total Return:', total_return(sim.portfolio))
print(sharpe_ratio(sim.portfolio, extraAnswers=True))

print('Total Return:', total_return(sim.portfolio, 'Portfolio'))
print(sharpe_ratio(sim.portfolio, 'Portfolio', extraAnswers=True))