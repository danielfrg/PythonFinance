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
        ans_er = [-0.021366671,0.0022274462,-0.0185659691,-0.0101614522,0.0050119435,0.0045959898,-0.0044392278,0.0232472168,0.0132134872,0.0302971666,-0.0052183242,0.0070052827,-0.0300279835,0.00267799,-0.021504018,-0.0227386992,0.001073346,-0.0334058711,0.0006534355,0.0067550817,-0.0523560148]
        ans_ar = [0.0243085131,0.0042030592,-0.0287381448,0.017574089,-0.0205456973,0.0044205009,0.0138454594,-0.0269746484,-0.024086865,0.0329416041,0.0474640163,-0.023538616,0.0084444694,0.0158343701,-0.001351881,0.0015758567,-0.0117697502,0.0062607135,-0.0234720687,-0.0193382638,0.0021170735]
        ans_car = [0.0243085131,0.0285115723,-0.0002265725,0.0173475164,-0.0031981809,0.00122232,0.0150677793,-0.0119068691,-0.0359937341,-0.00305213,0.0444118863,0.0208732703,0.0293177397,0.0451521097,0.0438002287,0.0453760854,0.0336063353,0.0398670487,0.01639498,-0.0029432838,-0.0008262103]
        # Note: STD Error is different from excel than scipy
        ans_t_test_excel = [0.9080919655,0.1570134829,-1.0735695078,0.6565144048,-0.7675246381,0.1651364416,0.5172241672,-1.0076906573,-0.8998118696,1.2305979363,1.7731109972,-0.8793309585,0.315459641,0.59152381,-0.0505021549,0.0588692034,-0.4396819969,0.233881176,-0.8768449541,-0.7224186015,0.0790874135]
        ans_t_test = [ 0.36922577,0.06307629,-0.44115974,0.26682576,-0.31494112,0.06650357,0.21010889,-0.41236226,-0.36868387,0.50342153,0.72373847,-0.36058215,0.12645236,0.24081318,-0.02285018,0.02182855,-0.18102633,0.09293668,-0.35984681,-0.29641529,0.02878559]
        ans_prob = [ 0.64402027,0.52514712,0.32954868,0.60519834,0.37640318,0.52651154,0.58320866,0.34003696,0.35618169,0.69266603,0.76538684,0.35920592,0.55031307,0.59515004,0.49088489,0.50870764,0.42817345,0.53702307,0.35948085,0.38345648,0.5114822 ]
        np_test.assert_almost_equal(self.evt.er.values, np.array(ans_er), 3)
        np_test.assert_almost_equal(self.evt.ar.values, np.array(ans_ar), 3)
        np_test.assert_almost_equal(self.evt.car.values, np.array(ans_car), 2)
        np_test.assert_almost_equal(self.evt.t_test.values, np.array(ans_t_test), 3)
        np_test.assert_almost_equal(self.evt.prob.values, np.array(ans_prob))

if __name__ == '__main__':
    suite = PastEventTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    #DataAccess('./data').empty_dirs(delete=True)