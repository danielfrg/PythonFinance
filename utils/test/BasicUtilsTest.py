import unittest

from finance.utils import DataAccess
from finance.utils import BasicUtils
from finance.sim import MarketSimulator

class TestBasicUtils(unittest.TestCase):
    def setUp0(self):
        self.da = DataAccess('./data')
        self.da.empty_dirs()

    def testBasicUtils(self):
        sim = MarketSimulator('./data')
        sim.initial_cash = 1000000
        sim.simulate("../../sim/test/orders.csv")

        # Test without giving the column
        tr1 = BasicUtils.total_return(sim.portfolio)
        sr1 = BasicUtils.sharpe_ratio(sim.portfolio, extraAnswers=True)
        self.assertEquals(tr1, 0.1332629999999999)
        self.assertEquals(sr1['sharpe_ratio'], 1.1825359272456812)
        self.assertEquals(sr1['std'], 0.0071658104790118396)
        self.assertEquals(sr1['mean'], 0.00054698326727656884)

        # Test giving the column we want to calculate
        tr2 = BasicUtils.total_return(sim.portfolio, 'Portfolio')
        sr2 = BasicUtils.sharpe_ratio(sim.portfolio, 'Portfolio', extraAnswers=True)
        self.assertEquals(tr2, 0.1332629999999999)
        self.assertEquals(sr2['sharpe_ratio'], 1.1825359272456812)
        self.assertEquals(sr2['std'], 0.0071658104790118396)
        self.assertEquals(sr2['mean'], 0.00054698326727656884)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasicUtils)
    unittest.TextTestRunner(verbosity=2).run(suite)

    DataAccess('./data').empty_dirs(delete=True)