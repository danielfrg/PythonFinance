import unittest
import numpy as np
import pandas as pd
import numpy.testing as np_test
import pandas.util.testing as pd_test
from datetime import datetime
from finance.utils import DataAccess

from finance.evtstudy import PastEvent

class PastEventTest(unittest.TestCase):
    def setUp0(self):
        self.da = DataAccess('./data')
        self.da.empty_dirs()
        self.setUp1()

    def setUp1(self):
        self.evt = PastEvent('./data')
        self.evt.symbol = 'AAPL'
        self.evt.market = "^gspc"
        self.evt.lookback_days = 10
        self.evt.lookforward_days = 10
        self.evt.estimation_period = 252
        self.evt.date = datetime(2009, 1, 5)
        self.evt.run()

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(PastEventTest('test_success'))
        return suite

    def test_success(self):
        self.setUp1()

        # Test: Series names
        self.assertEquals(self.evt.er.name, 'Expected Return')
        self.assertEquals(self.evt.ar.name, 'Abnormal Return')
        self.assertEquals(self.evt.car.name, 'Cumulative Abnormal Return')
        self.assertEquals(self.evt.t_test.name, 't test')
        self.assertEquals(self.evt.prob.name, 'Probability')
        # Test: Index values
        self.assertEquals(self.evt.er.index[0].to_pydatetime(), datetime(2008, 12, 18))
        self.assertEquals(self.evt.er.index[-1].to_pydatetime(), datetime(2009, 1, 20))

        # TODO: Test the evt_windows_data + its indexes

        # Test: Values
        ans_er = [-0.0212234, 0.00230225, -0.0184308, -0.0100507, 0.00507867, 0.00466393, -0.0043450, 0.02326106, 0.01325643, 0.03029057, -0.0051219, 0.00706623, -0.0298596, 0.00275149, -0.0213603, -0.0225914, 0.00115150, -0.0332277, 0.00073280, 0.00681676, -0.0521229]
        ans_ar = [0.02416528, 0.00412824, -0.0288732, 0.01746335, -0.0206124, 0.00435256, 0.01375131, -0.0269885, -0.0241298, 0.03294819, 0.04736761, -0.0235995, 0.00827612, 0.01576086, -0.0014955, 0.00142864, -0.0118479, 0.00608256, -0.0235514, -0.0193999, 0.00188397]
        ans_car = [0.02416528, 0.02829353, -0.0005797, 0.01688362, -0.0037288, 0.00062375, 0.01437507, -0.0126134, -0.0367432, -0.0037950, 0.04357256, 0.01997299, 0.02824911, 0.04400998, 0.04251447, 0.04394312, 0.03209521, 0.03817778, 0.01462634, -0.0047736, -0.0028896]
        ans_t_test = [0.36922576, 0.43230205, -0.0088576, 0.25796807, -0.0569730, 0.00953051, 0.21963940, -0.1927228, -0.5614067, -0.0579851, 0.66575327, 0.30517111, 0.43162348, 0.67243666, 0.64958648, 0.67141503, 0.49038869, 0.58332538, 0.22347857, -0.0729367, -0.0441511]
        ans_prob = [0.64402027, 0.66723905, 0.49646633, 0.60178422, 0.47728333, 0.50380206, 0.58692400, 0.42358801, 0.28726015, 0.47688021, 0.74721559, 0.61988208, 0.66699245, 0.74934712, 0.74202031, 0.74902191, 0.68807056, 0.72016286, 0.58841847, 0.47092823, 0.48239196]
        np_test.assert_almost_equal(self.evt.er.values, np.array(ans_er))
        np_test.assert_almost_equal(self.evt.ar.values, np.array(ans_ar))
        np_test.assert_almost_equal(self.evt.car.values, np.array(ans_car))
        np_test.assert_almost_equal(self.evt.t_test.values, np.array(ans_t_test))
        np_test.assert_almost_equal(self.evt.prob.values, np.array(ans_prob))

if __name__ == '__main__':
    suite = PastEventTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    DataAccess('./data').empty_dirs(delete=True)