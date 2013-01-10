from datetime import datetime
import matplotlib.pyplot as plt
from finance.utils import Calculator
from finance.sim import MarketSimulator

# from finance.utils import DataAccess
# DataAccess.path = 'data'

sim = MarketSimulator()
sim.initial_cash = 1000000
sim.load_trades("MarketSimulator_orders.csv")
sim.simulate()

print(sim.portfolio[0:10])

print('Total Return:', Calculator.ret(sim.portfolio))
print(Calculator.sharpe_ratio(sim.portfolio))

sim.portfolio.plot()
# plt.grid(True)
plt.show()