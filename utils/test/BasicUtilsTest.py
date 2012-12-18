from datetime import datetime
from finance.utils.BasicUtils import *
from finance.sim import MarketSimulator


class TestMarketSimulator(unittest.TestCase):
    def setUp0(self):
        self.da = DataAccess('./data')
        self.da.empty_dirs()
        self.sim = MarketSimulator('./data')

    def setUp1(self):
        self.da = DataAccess('./data')

    def setUp2(self):
        self.sim = MarketSimulator('./data2')

    def testSimulation1(self):
        setUp0()

        sim.initial_cash = 1000000
        sim.simulate("orders.csv")

        print('Total Return:', total_return(sim.portfolio))
        print(sharpe_ratio(sim.portfolio, extraAnswers=True))

        print('Total Return:', total_return(sim.portfolio, 'Portfolio'))
        print(sharpe_ratio(sim.portfolio, 'Portfolio', extraAnswers=True))



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMarketSimulator)
    unittest.TextTestRunner(verbosity=2).run(suite)

    da = DataAccess('./data')
    da.empty_dirs(delete=True)