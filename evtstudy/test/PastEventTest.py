import unittest
import numpy as np
import pandas as pd
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

        # Test: Values
        ans_er = ['-0.0212234', '0.00230225', '-0.0184308', '-0.0100507', '0.00507867', '0.00466393', '-0.0043450', '0.02326106', '0.01325643', '0.03029057', '-0.0051219', '0.00706623', '-0.0298596', '0.00275149', '-0.0213603', '-0.0225914', '0.00115150', '-0.0332277', '0.00073280', '0.00681676', '-0.0521229']
        ans_ar = ['0.02416528', '0.00412824', '-0.0288732', '0.01746335', '-0.0206124', '0.00435256', '0.01375131', '-0.0269885', '-0.0241298', '0.03294819', '0.04736761', '-0.0235995', '0.00827612', '0.01576086', '-0.0014955', '0.00142864', '-0.0118479', '0.00608256', '-0.0235514', '-0.0193999', '0.00188397']
        ans_car = ['0.02416528', '0.02829353', '-0.0005797', '0.01688362', '-0.0037288', '0.00062375', '0.01437507', '-0.0126134', '-0.0367432', '-0.0037950', '0.04357256', '0.01997299', '0.02824911', '0.04400998', '0.04251447', '0.04394312', '0.03209521', '0.03817778', '0.01462634', '-0.0047736', '-0.0028896']
        ans_t_test = ['0.93826998', '1.09855833', '-0.0225090', '0.65554389', '-0.1447789', '0.02421877', '0.55814377', '-0.4897438', '-1.4266368', '-0.1473509', '1.69180043', '0.77549544', '1.09683395', '1.70878414', '1.65071766', '1.70618799', '1.24616708', '1.48233614', '0.56789979', '-0.1853454', '-0.1121960']
        ans_prob = ['0.82594716', '0.86401961', '0.49102096', '0.74394118', '0.44244271', '0.50966094', '0.71162689', '0.31215756', '0.07684230', '0.44142751', '0.95465798', '0.78097652', '0.86364300', '0.95625452', '0.95060188', '0.95601345', '0.89364846', '0.93087456', '0.71494849', '0.42647903', '0.45533397']
        self.assertEquals([str(x)[0:10] for x in self.evt.er.values.tolist()], ans_er)
        self.assertEquals([str(x)[0:10] for x in self.evt.ar.values.tolist()], ans_ar)
        self.assertEquals([str(x)[0:10] for x in self.evt.car.values.tolist()], ans_car)
        self.assertEquals([str(x)[0:10] for x in self.evt.t_test.values.tolist()], ans_t_test)
        self.assertEquals([str(x)[0:10] for x in self.evt.prob.values.tolist()], ans_prob)

        # Test: Compare results of equal events
        evt2 = PastEvent('./data')
        evt2.symbol = 'AAPL'
        evt2.market = "^gspc"
        evt2.lookback_days = 10
        evt2.lookforward_days = 10
        evt2.estimation_period = 252
        evt2.date = datetime(2009, 1, 5)
        evt2.run()

        self.assertListEqual([str(x)[0:10] for x in self.evt.er.values.tolist()], [str(x)[0:10] for x in evt2.er.values.tolist()])
        self.assertEqual([str(x)[0:10] for x in self.evt.ar.values.tolist()], [str(x)[0:10] for x in evt2.ar.values.tolist()])
        self.assertListEqual([str(x)[0:10] for x in self.evt.car.values.tolist()], [str(x)[0:10] for x in evt2.car.values.tolist()])
        self.assertListEqual([str(x)[0:10] for x in self.evt.t_test.values.tolist()], [str(x)[0:10] for x in evt2.t_test.values.tolist()])
        self.assertListEqual([str(x)[0:10] for x in self.evt.prob.values.tolist()], [str(x)[0:10] for x in evt2.prob.values.tolist()])


if __name__ == '__main__':
    suite = PastEventTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    DataAccess('./data').empty_dirs(delete=True)