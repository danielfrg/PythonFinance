import unittest
import numpy as np
import pandas as pd
import numpy.testing as np_test
import pandas.util.testing as pd_test
from datetime import datetime
from finance.utils import DataAccess

class MultipleEventTest(unittest.TestCase):

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(MultipleEventTest('test_1'))
        suite.addTest(MultipleEventTest('test_2'))
        return suite

    def test_1(self):
        '''
        Tests one event on one Symbol
        '''

        # 1. Find the event
        from finance.evtstudy import EventFinder
        evtf = EventFinder('./data')
        evtf.symbols = ['AMD']
        evtf.start_date = datetime(2008, 1, 1)
        evtf.end_date = datetime(2008, 10, 28)
        evtf.function = evtf.went_below(3)
        evtf.search()
        # Test: number of events found = 1
        self.assertEqual(evtf.num_events, 1)
        # Test: date of the event is 2008-10-27
        self.assertEqual(evtf.matrix['AMD'][evtf.matrix['AMD'] == 1].index, [datetime(2008,10,27)])

        # 2. Assess the event
        from finance.evtstudy import MultipleEvents
        mevt = MultipleEvents('./data')
        mevt.matrix = evtf.matrix
        mevt.market = 'SPY'
        mevt.lookback_days = 20
        mevt.lookforward_days = 20
        mevt.estimation_period = 200
        mevt.run()

        # Test: Values and indexes on the event window
        sol = [[4.29],[5.25],[4.74],[4.14],[4.53],[4.23],[4.59],[4.05],[4.04],[3.81],[4.21],[4.27],[3.91],[4.12],[4.21],[4.11],[3.91],[3.62],[3.28],[3.03],[2.94],[2.84],[2.98],[3.56],[3.5],[3.61],[3.8],[3.55],[3.17],[3.16],[3.04],[2.96],[2.57],[2.7],[2.43],[2.5],[2.5],[2.12],[1.91],[1.82],[1.86]]
        np_test.assert_equal(mevt.equities_window.values, sol)
        np_test.assert_equal(mevt.equities_window.index, range(-20, 21))

        # Test: Values and indexes on the estimation period
        head = mevt.equities_estimation.head()
        sol_head = [[9.07], [8.97],[8.84],[8.43],[7.95]]
        np_test.assert_equal(head.values, sol_head)

        tail = mevt.equities_estimation.tail()
        sol_tail = [[4.99],[4.94],[4.88],[5.23],[5.16]]
        np_test.assert_equal(tail.values, sol_tail)

        np_test.assert_equal(mevt.equities_estimation.index, range(-220, -20))

        # Test: estimation periord linear regression values
        self.assertAlmostEqual(mevt.reg_estimation['Slope'][0], 1.51, 4)
        self.assertAlmostEqual(mevt.reg_estimation['Intercept'][0], -0.0007, 4)
        self.assertAlmostEqual(mevt.reg_estimation['Std Error'][0], 0.16, 1)

        print(mevt.expected_returns)
        sol = [[ -7.02070203e-04], [  6.17949225e-02], [  1.55261205e-04], [ -5.53973384e-02], [ -2.11501520e-02], [ -7.76088393e-02], [ -6.82830163e-02], [ -3.88094510e-02], [ -1.06085767e-01], [ -3.74299651e-02], [  2.18603935e-01], [ -2.31058340e-02], [ -1.49266599e-01], [  6.20784489e-02], [ -9.71674487e-03], [  9.01638863e-02], [ -4.58206393e-02], [ -8.29990795e-02], [  1.68523562e-02], [ -7.73431604e-02], [ -5.42106496e-02], [  1.75591749e-01], [ -1.16623694e-02], [  5.16509531e-02], [  7.55895402e-03], [  3.74830454e-03], [  5.04975134e-02], [ -6.40883636e-02], [ -8.44403796e-02], [  4.92801368e-02], [ -2.06547411e-02], [ -4.72255991e-02], [ -6.71670046e-02], [  9.33499300e-02], [ -7.59680470e-02], [ -2.07926519e-02], [  2.78040064e-02], [ -9.75779979e-02], [ -1.12760731e-01], [  8.07973783e-02], [  1.03927783e-01]]

    def test_2(self):
        '''
        Tests various events
        '''

if __name__ == '__main__':
    suite = MultipleEventTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    #DataAccess('./data').empty_dirs(delete=True)