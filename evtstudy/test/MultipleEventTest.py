import unittest
import numpy as np
import pandas as pd
import numpy.testing as np_test
import pandas.util.testing as pd_test
from datetime import datetime
from finance.utils import DataAccess

class MultipleEventTest(unittest.TestCase):
    def setUp1(self):
        from finance.evtstudy import EventFinder
        self.evtf = EventFinder('./data')
        self.evtf.symbols = ['AMD']
        self.evtf.start_date = datetime(2008, 1, 1)
        self.evtf.end_date = datetime(2008, 10, 28)
        self.evtf.function = self.evtf.went_below(3)
        self.evtf.search()
        
        from finance.evtstudy import MultipleEvents
        self.mevt = MultipleEvents('./data')
        self.mevt.matrix = self.evtf.matrix
        self.mevt.market = 'SPY'
        self.mevt.lookback_days = 20
        self.mevt.lookforward_days = 20
        self.mevt.estimation_period = 200
        self.mevt.run()

    def setUp2(self):
        from finance.evtstudy import EventFinder
        self.evtf = EventFinder('./data')
        self.evtf.symbols = ['AMD', 'CBG']
        self.evtf.start_date = datetime(2008, 1, 1)
        self.evtf.end_date = datetime(2009, 12, 31)
        self.evtf.function = self.evtf.went_below(3)
        self.evtf.search()
        
        from finance.evtstudy import MultipleEvents
        self.mevt = MultipleEvents('./data')
        self.mevt.matrix = self.evtf.matrix
        self.mevt.market = 'SPY'
        self.mevt.lookback_days = 20
        self.mevt.lookforward_days = 20
        self.mevt.estimation_period = 200
        self.mevt.run()


    def suite(self):
        suite = unittest.TestSuite()
        #suite.addTest(MultipleEventTest('test_data_values'))
        #suite.addTest(MultipleEventTest('test_analysis'))
        suite.addTest(MultipleEventTest('test_data_values_2'))
        return suite

    def test_data_values(self):
        '''
        One event on one Symbol
        Test the values of the equities and market
        Tests the values on the event windows and estimation period
        Tests the daily returns on the event windows and estimation period
        '''
        self.setUp1()

        evtf = self.evtf
        mevt = self.mevt

        # Test: Equities: Event window
        sol = [[4.29],[5.25],[4.74],[4.14],[4.53],[4.23],[4.59],[4.05],[4.04],[3.81],[4.21],[4.27],[3.91],[4.12],[4.21],[4.11],[3.91],[3.62],[3.28],[3.03],[2.94],[2.84],[2.98],[3.56],[3.5],[3.61],[3.8],[3.55],[3.17],[3.16],[3.04],[2.96],[2.57],[2.7],[2.43],[2.5],[2.5],[2.12],[1.91],[1.82],[1.86]]
        np_test.assert_equal(mevt.equities_window.values, sol)
        np_test.assert_equal(mevt.equities_window.index, range(-20, 21))

        # Test: Equities: Daily returns on the Event window
        sol = [[ -0.168605],[  0.223776],[ -0.097143],[ -0.126582],[  0.094203],[ -0.066225],[  0.085106],[ -0.117647],[ -0.002469],[ -0.056931],[  0.104987],[  0.014252],[ -0.084309],[  0.053708],[  0.021845],[ -0.023753],[ -0.048662],[ -0.074169],[ -0.093923],[ -0.076220], [-0.029703], [-0.034014], [ 0.049296], [ 0.194631], [-0.016854], [ 0.031429], [ 0.052632], [-0.065789], [-0.107042], [-0.003155], [-0.037975], [-0.026316], [-0.131757], [ 0.050584], [-0.100000], [ 0.028807], [ 0.000000], [-0.152000], [-0.099057], [-0.047120], [ 0.021978]]
        np_test.assert_almost_equal(mevt.dr_equities_window.values, sol, 5)
        np_test.assert_equal(mevt.dr_equities_window.index, range(-20, 21))

        # Test: Equities: Estimation period
        head = mevt.equities_estimation.head()
        sol_head = [[9.07], [8.97],[8.84],[8.43],[7.95]]
        np_test.assert_equal(head.values, sol_head)
        np_test.assert_equal(head.index, range(-221,-216))
        tail = mevt.equities_estimation.tail()
        sol_tail = [[4.99],[4.94],[4.88],[5.23],[5.16]]
        np_test.assert_equal(tail.values, sol_tail)
        np_test.assert_equal(tail.index, range(-25,-20))
        np_test.assert_equal(mevt.equities_estimation.index, range(-221, -20))

        # Test: Equities: Daily returns on the Estimation period
        head = mevt.dr_equities_estimation.head()
        sol_head = [[-0.011983], [-0.011025],[-0.014493],[-0.046380],[-0.056940]]
        np_test.assert_almost_equal(head.values, sol_head, 5)
        np_test.assert_equal(head.index, range(-221,-216))
        tail = mevt.dr_equities_estimation.tail()
        sol_tail = [[-0.079336],[-0.010020],[-0.012146],[0.071721],[-0.013384]]
        np_test.assert_almost_equal(tail.values, sol_tail, 5)
        np_test.assert_equal(tail.index, range(-25,-20))
        np_test.assert_equal(mevt.dr_equities_estimation.index, range(-221, -20))

        # Test: Market: Event window
        sol = [[101.48],[105.68],[105.74],[101.91],[100.53],[ 95.41],[ 91.14],[ 88.84],[ 82.64],[ 80.63],[ 92.34],[ 90.97],[ 82.02],[ 85.43],[ 84.92],[ 90.03],[ 87.34],[ 82.58],[ 83.54],[ 79.30], [76.49], [85.42], [84.80], [87.74], [88.22], [88.48], [91.48], [87.64], [82.78], [85.52], [84.39], [81.79], [78.19], [83.06], [78.92], [77.87], [79.34], [74.25], [68.74], [72.45], [77.47]]
        np_test.assert_equal(mevt.market_window.values, sol)
        np_test.assert_equal(mevt.market_window.index, range(-20, 21))

        # Test: Market: Daily retuns on the Event window
        sol = [[-0.0783761693],[0.0413874655],[0.0005677517],[-0.0362209192],[-0.01354136],[-0.0509300706],[-0.0447542186],[-0.0252359008],[-0.0697883836],[-0.0243223621],[0.1452313035],[-0.0148364739],[-0.0983840827],[0.0415752256],[-0.0059697998],[0.0601742817],[-0.0298789292],[-0.0544996565],[0.0116250908],[-0.0507541298],[-0.0354350567],[0.1167472872],[-0.0072582533],[0.0346698113],[0.0054707089],[0.0029471775],[0.0339059675],[-0.0419763883],[-0.0554541305],[0.0330997826],[-0.0132132834],[-0.0308093376],[-0.0440151608],[0.0622841796],[-0.0498434866],[-0.0133046123],[0.0188776165],[-0.0641542728],[-0.0742087542],[0.0539714868],[0.0692891649]]
        np_test.assert_almost_equal(mevt.dr_market_window.values, sol, 5)
        np_test.assert_equal(mevt.dr_market_window.index, range(-20, 21))

        # Test: Market: Estimation period
        head = mevt.market_estimation.head()
        sol_head = [[131.96], [133.26],[132.99],[131.3],[129.43]]
        np_test.assert_equal(head.values, sol_head)
        np_test.assert_equal(head.index, range(-221,-216))
        tail = mevt.market_estimation.tail()
        sol_tail = [[110.53],[108.01],[108.36],[110.05],[110.11]]
        np_test.assert_equal(tail.values, sol_tail)
        np_test.assert_equal(tail.index, range(-25,-20))
        np_test.assert_equal(mevt.market_estimation.index, range(-221, -20))

        # Test: Market: Daily returns on the estimation period
        head = mevt.dr_market_estimation.head()
        sol_head = [[-0.027417],[ 0.009851],[-0.002026],[-0.012708],[-0.014242]]
        np_test.assert_almost_equal(head.values, sol_head, 5)
        np_test.assert_equal(head.index, range(-221,-216))
        tail = mevt.dr_market_estimation.tail()
        sol_tail = [[-0.022637],[-0.022799],[ 0.003240],[ 0.015596],[ 0.000545]]
        np_test.assert_almost_equal(tail.values, sol_tail, 5)
        np_test.assert_equal(tail.index, range(-25,-20))
        np_test.assert_equal(mevt.dr_market_estimation.index, range(-221, -20))

    def test_analysis(self):
        '''
        Test the regression

        Note: Assumes test_data_values is OK.
        '''
        self.setUp1()

        evtf = self.evtf
        mevt = self.mevt

        # Test: Linear regression on the estimation period
        self.assertAlmostEqual(mevt.reg_estimation['Slope'][0], 1.48, 2)
        self.assertAlmostEqual(mevt.reg_estimation['Intercept'][0], -0.0007, 4)
        self.assertAlmostEqual(mevt.reg_estimation['Std Error'][0], 0.166, 1)

        # Test: expected returns
        sol = [[ -0.116949],[0.060677],[0.000136],[ -0.054427],[ -0.020790],[ -0.076242],[ -0.067083],[ -0.038135],[ -0.104212],[ -0.036780],[0.214691],[ -0.022711],[ -0.146623],[0.060955],[ -0.009560],[0.088540],[ -0.045021],[ -0.081537],[0.016535],[ -0.075981], [-0.053261], [ 0.172445], [-0.011471], [ 0.050714], [ 0.007407], [ 0.003665], [ 0.049581], [-0.062963], [-0.082952], [ 0.048385], [-0.020303], [-0.046401], [-0.065987], [ 0.091669], [-0.074631], [-0.020439], [ 0.027292], [-0.095856], [-0.110768], [ 0.079340], [ 0.102059]]
        np_test.assert_almost_equal(mevt.expected_returns.values, sol, 5)
        

    def test_data_values_2(self):
        '''
        Two events on one Symbol
        Test the values of the equities and market
        Tests the values on the event windows and estimation period
        Tests the daily returns on the event windows and estimation period
        '''
        self.setUp2()

        evtf = self.evtf
        mevt = self.mevt

if __name__ == '__main__':
    suite = MultipleEventTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    #DataAccess('./data').empty_dirs(delete=True)