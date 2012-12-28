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
        self.evtf.end_date = datetime(2009, 12, 31)
        self.evtf.function = self.evtf.went_below(3)
        self.evtf.search()
        
        from finance.evtstudy import MultipleEvents
        self.mevt = MultipleEvents('./data')
        self.mevt.list = self.evtf.list
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
        self.mevt.list = self.evtf.list
        self.mevt.market = 'SPY'
        self.mevt.lookback_days = 20
        self.mevt.lookforward_days = 20
        self.mevt.estimation_period = 200
        self.mevt.run()


    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(MultipleEventTest('test_1_event'))
        suite.addTest(MultipleEventTest('test_2_events'))
        return suite

    def test_1_event(self):
        '''
        One event on one Symbol
        Test the values of the equities and market
        Tests the values on the event windows and estimation period
        Tests the daily returns on the event windows and estimation period
        '''
        self.setUp1()
        evtf = self.evtf
        mevt = self.mevt

        # ----------------- TEST EQUITIES VALUES -----------------------

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
        sol_head = [[8.97],[8.84],[8.43],[7.95],[7.68]]
        np_test.assert_equal(head.values, sol_head)
        np_test.assert_equal(head.index, range(-220,-215))
        tail = mevt.equities_estimation.tail()
        sol_tail = [[4.99],[4.94],[4.88],[5.23],[5.16]]
        np_test.assert_equal(tail.values, sol_tail)
        np_test.assert_equal(tail.index, range(-25,-20))
        np_test.assert_equal(mevt.equities_estimation.index, range(-220, -20))

        # Test: Equities: Daily returns on the Estimation period
        head = mevt.dr_equities_estimation.head()
        sol_head = [[-0.011025],[-0.014493],[-0.046380],[-0.056940], [-0.033962]]
        np_test.assert_almost_equal(head.values, sol_head, 5)
        np_test.assert_equal(head.index, range(-220,-215))
        tail = mevt.dr_equities_estimation.tail()
        sol_tail = [[-0.079336],[-0.010020],[-0.012146],[0.071721],[-0.013384]]
        np_test.assert_almost_equal(tail.values, sol_tail, 5)
        np_test.assert_equal(tail.index, range(-25,-20))
        np_test.assert_equal(mevt.dr_equities_estimation.index, range(-220, -20))

        # ----------------- TEST MARKET VALUES -----------------------

        # Test: Market: Event window
        sol = [[101.48],[105.68],[105.74],[101.91],[100.53],[ 95.41],[ 91.14],[ 88.84],[ 82.64],[ 80.63],[ 92.34],[ 90.97],[ 82.02],[ 85.43],[ 84.92],[ 90.03],[ 87.34],[ 82.58],[ 83.54],[ 79.30], [76.49], [85.42], [84.80], [87.74], [88.22], [88.48], [91.48], [87.64], [82.78], [85.52], [84.39], [81.79], [78.19], [83.06], [78.92], [77.87], [79.34], [74.25], [68.74], [72.45], [77.47]]
        np_test.assert_equal(mevt.market_window.values, sol)
        np_test.assert_equal(mevt.market_window.index, range(-20, 21))

        # Test: Market: Daily returns on the Event window
        sol = [[-0.0783761693],[0.0413874655],[0.0005677517],[-0.0362209192],[-0.01354136],[-0.0509300706],[-0.0447542186],[-0.0252359008],[-0.0697883836],[-0.0243223621],[0.1452313035],[-0.0148364739],[-0.0983840827],[0.0415752256],[-0.0059697998],[0.0601742817],[-0.0298789292],[-0.0544996565],[0.0116250908],[-0.0507541298],[-0.0354350567],[0.1167472872],[-0.0072582533],[0.0346698113],[0.0054707089],[0.0029471775],[0.0339059675],[-0.0419763883],[-0.0554541305],[0.0330997826],[-0.0132132834],[-0.0308093376],[-0.0440151608],[0.0622841796],[-0.0498434866],[-0.0133046123],[0.0188776165],[-0.0641542728],[-0.0742087542],[0.0539714868],[0.0692891649]]
        np_test.assert_almost_equal(mevt.dr_market_window.values, sol, 5)
        np_test.assert_equal(mevt.dr_market_window.index, range(-20, 21))

        # Test: Market: Estimation period
        head = mevt.market_estimation.head()
        sol_head = [[133.26],[132.99],[131.3],[129.43],[130.15]]
        np_test.assert_equal(head.values, sol_head)
        np_test.assert_equal(head.index, range(-220,-215))
        tail = mevt.market_estimation.tail()
        sol_tail = [[110.53],[108.01],[108.36],[110.05],[110.11]]
        np_test.assert_equal(tail.values, sol_tail)
        np_test.assert_equal(tail.index, range(-25,-20))
        np_test.assert_equal(mevt.market_estimation.index, range(-220, -20))

        # Test: Market: Daily returns on the estimation period
        head = mevt.dr_market_estimation.head()
        sol_head = [[ 0.009851],[-0.002026],[-0.012708],[-0.014242],[0.00556]]
        np_test.assert_almost_equal(head.values, sol_head, 5)
        np_test.assert_equal(head.index, range(-220,-215))
        tail = mevt.dr_market_estimation.tail()
        sol_tail = [[-0.022637],[-0.022799],[ 0.003240],[ 0.015596],[ 0.000545]]
        np_test.assert_almost_equal(tail.values, sol_tail, 5)
        np_test.assert_equal(tail.index, range(-25,-20))
        np_test.assert_equal(mevt.dr_market_estimation.index, range(-220, -20))

        # ----------------- TEST REGRESSION -----------------------

        # Test: Linear regression on the estimation period
        self.assertAlmostEqual(mevt.reg_estimation['Slope'][0], 1.503154, 5)
        self.assertAlmostEqual(mevt.reg_estimation['Intercept'][0], -0.000837, 5)
        self.assertAlmostEqual(mevt.reg_estimation['Std Error'][0], 0.167677, 5)

        # Test: expected returns
        sol = [[-0.1186486542],[0.0613746287],[1.62798190468245E-005],[-0.0552827876],[-0.0211918992],[-0.0773929192],[-0.0681096576],[-0.0387706044],[-0.1057398829],[-0.0373974142],[0.2174679925],[-0.0231386559],[-0.1487236453],[0.0616568611],[-0.0098106722],[0.0896141216],[-0.0457497949],[-0.0827585593],[0.0166371722],[-0.0771284528],[-0.0541015146],[0.1746521067],[-0.0117474172],[0.0512769545],[0.0073861835],[0.0035929252],[0.0501287789],[-0.0639341485],[-0.0841932815],[0.0489169582],[-0.0206987494],[-0.0471483427],[-0.0669987392],[0.0927856248],[-0.0757596152],[-0.0208360307],[0.0275388411],[-0.0972709421],[-0.1123843842],[0.0802903607],[0.1033152022]]
        np_test.assert_almost_equal(mevt.expected_returns.values, sol, 5)
        

    def test_2_events(self):
        '''
        Two events on two different equities
        '''
        self.setUp2()
        evtf = self.evtf
        mevt = self.mevt

        # ----------------- TEST EVENT WINDOW VALUES -----------------------

        # Test: Equites: Event Window
        sol_amd = [4.29,5.25,4.74,4.14,4.53,4.23,4.59,4.05,4.04,3.81,4.21,4.27,3.91,4.12,4.21,4.11,3.91,3.62,3.28,3.03,2.94,2.84,2.98,3.56,3.5,3.61,3.8,3.55,3.17,3.16,3.04,2.96,2.57,2.7,2.43,2.5,2.5,2.12,1.91,1.82,1.86]
        sol_cbg = [3.82,3.6,3.51,3.54,3.95,3.91,4.36,4.37,3.77,4.21,4.05,3.76,3.43,3.58,3.26,3.33,3.18,3.47,3.24,3.05,2.89,2.53,2.66,2.78,2.57,2.52,2.71,3.39,2.99,3.28,3.06,2.61,2.78,3.05,2.7,2.36,2.95,3,4.92,5.01,4.25]
        np_test.assert_equal(mevt.equities_window['AMD 2008-10-27'].values, sol_amd)
        np_test.assert_equal(mevt.equities_window['CBG 2009-02-27'].values, sol_cbg)

        # Test: Market: Event Window
        sol_amd = [101.48,105.68,105.74,101.91,100.53,95.41,91.14,88.84,82.64,80.63,92.34,90.97,82.02,85.43,84.92,90.03,87.34,82.58,83.54,79.3,76.49,85.42,84.8,87.74,88.22,88.48,91.48,87.64,82.78,85.52,84.39,81.79,78.19,83.06,78.92,77.87,79.34,74.25,68.74,72.45,77.47]
        sol_cbg = [77.66,76.08,75.85,76.91,76.54,77.68,79.89,80,76.34,76.79,76.84,76.01,72.76,72.59,71.81,71.11,68.57,71.16,70.6,69.46,67.9,64.85,64.36,65.88,63.19,63.3,62.56,66.29,66.72,69.35,69.89,69.68,71.81,73.42,72.51,70.96,76.06,74.56,75.35,76.88,75.49]
        np_test.assert_equal(mevt.market_window['AMD 2008-10-27'].values, sol_amd)
        np_test.assert_equal(mevt.market_window['CBG 2009-02-27'].values, sol_cbg)

        # ----------------- TEST ESTIMATION PERIOD VALUES -----------------------

        # Test: Equities: Daily Return Estimation Window
        ans_amd = mevt.dr_equities_estimation['AMD 2008-10-27'].head().values
        sol_amd = [-0.0110,-0.0145,-0.0464,-0.0569,-0.0340]
        ans_cbg = mevt.dr_equities_estimation['CBG 2009-02-27'].head().values
        sol_cbg = [0.0030395137,0.0661616162,0.0023685457,0.0047258979,0.0747883349]
        np_test.assert_almost_equal(ans_amd, sol_amd, 4)
        np_test.assert_almost_equal(ans_cbg, sol_cbg)

        # Test: Equities: Daily Return Estimation Window
        ans_amd = mevt.dr_equities_estimation['AMD 2008-10-27'].tail().values
        sol_amd = [-0.0793,-0.0100,-0.0121,0.0717,-0.0134]
        ans_cbg = mevt.dr_equities_estimation['CBG 2009-02-27'].tail().values
        sol_cbg = [-0.0185185185,0.0296495957,0.0130890052,0.015503876,0.1399491094]
        np_test.assert_almost_equal(ans_amd, sol_amd, 4)
        np_test.assert_almost_equal(ans_cbg, sol_cbg)

        # ----------------- TEST REGRESSION -----------------------

        # Test: Linear regression AMD
        self.assertAlmostEqual(mevt.reg_estimation['Slope'][0], 1.503154, 5)
        self.assertAlmostEqual(mevt.reg_estimation['Intercept'][0], -0.000837, 5)
        self.assertAlmostEqual(mevt.reg_estimation['Std Error'][0], 0.167677, 5)
        # Test: Linear regression CBG
        self.assertAlmostEqual(mevt.reg_estimation['Slope'][1], 2.114477, 5)
        self.assertAlmostEqual(mevt.reg_estimation['Intercept'][1], 0.000245, 5)
        self.assertAlmostEqual(mevt.reg_estimation['Std Error'][1], 0.175613, 1)

        # ----------------- RETURNS -----------------------

        sol = [-0.0935778889,0.0093005253,-0.0030652004,-0.0127437001,-0.0155592992,-0.0228269283,-0.0038534967,-0.0178067635,-0.1011157829,-0.0123437872,0.1095452261,-0.0228664344,-0.1194439107,0.0284810802,-0.0161428311,0.0346239878,-0.0605159022,-0.0013228235,0.0001213843,-0.055512954,-0.0506724172,0.0399587789,-0.0137392637,0.050730282,-0.0393530541,0.0037597183,0.0128277175,0.031191257,-0.0351158694,0.0662560438,-0.0019942561,-0.026628046,-0.0010585301,0.0702192315,-0.0508608599,-0.0328951008,0.0898775683,-0.069362732,-0.0448673915,0.061735504,0.0326654253]
        np_test.assert_almost_equal(mevt.mean_expected_return, sol)

        sol = [-0.064385151,0.0737917751,-0.0580062281,-0.0462739349,0.120570353,-0.0153489456,0.1039514453,-0.0398699769,0.0312313294,0.0422338783,-0.0760541631,-0.005810144,0.0334063652,0.020239029,-0.0176275762,-0.0357642761,0.0136624794,0.0098359088,-0.0802239206,-0.0119177897,0.0095914239,-0.1192493187,0.0640788506,0.0691415452,-0.0068436964,0.0022269409,0.0511864847,0.0613752608,-0.0774023075,-0.0193383475,-0.050529671,-0.0600592605,-0.0322527985,0.0036337483,-0.0565161893,-0.01566457,0.0351224317,0.0018373083,0.3153390896,-0.0761493719,-0.0975247177]
        np_test.assert_almost_equal(mevt.mean_abnormal_return, sol)

        ans_amd = mevt.cumulative_abnormal_returns['AMD 2008-10-27']
        sol_amd = [-0.049955997,0.1124455981,0.0152864611,-0.0560130297,0.0593817681,0.0705495217,0.2237655622,0.1448891078,0.2481598549,0.228626576,0.1161454602,0.1535358975,0.2179504093,0.2100019881,0.2416573205,0.1282902297,0.1253782241,0.1339679855,0.0234081613,0.024317102,0.0487156463,-0.1599500658,-0.0989068739,0.044447044,0.020206928,0.0480425742,0.0505453742,0.0486900491,0.0258410771,-0.0262304553,-0.0435063895,-0.0226738363,-0.0874318538,-0.129633821,-0.1538742058,-0.1042315907,-0.1317704318,-0.1864994897,-0.1731717093,-0.3005824888,-0.381919669]
        ans_cbg = mevt.cumulative_abnormal_returns['CBG 2009-02-27']
        sol_cbg = [-0.0788143049,-0.0936323499,-0.1124856691,-0.133734048,-0.0079881398,-0.0498537847,0.0048330653,0.0039695659,-0.0368385224,0.067162513,0.0275353027,-0.0214754226,-0.019077204,0.0293492752,-0.0375612096,0.004277329,0.0345142935,0.0455963496,-0.0042916675,-0.0290361876,-0.0342518841,-0.0640848093,0.0030297,-0.0020411276,0.0085115957,-0.0148701687,0.0850000007,0.2096058474,0.0776502044,0.0910450417,0.0072616339,-0.1336894403,-0.1334370198,-0.0839675559,-0.1727595498,-0.2537313048,-0.1559476003,-0.0975439258,0.5198064729,0.4949185086,0.3812062534]
        np_test.assert_almost_equal(ans_amd, sol_amd, 4)
        np_test.assert_almost_equal(ans_cbg, sol_cbg)

        sol = [-0.064385151,0.0094066241,-0.048599604,-0.0948735389,0.0256968141,0.0103478685,0.1142993137,0.0744293368,0.1056606662,0.1478945445,0.0718403814,0.0660302375,0.0994366027,0.1196756317,0.1020480554,0.0662837794,0.0799462588,0.0897821675,0.0095582469,-0.0023595428,0.0072318811,-0.1120174376,-0.047938587,0.0212029582,0.0143592618,0.0165862028,0.0677726875,0.1291479482,0.0517456408,0.0324072932,-0.0181223778,-0.0781816383,-0.1104344368,-0.1068006885,-0.1633168778,-0.1789814477,-0.143859016,-0.1420217078,0.1733173818,0.0971680099,-0.0003567078]
        np_test.assert_almost_equal(mevt.mean_cumulative_abnormal_return, sol)


if __name__ == '__main__':
    suite = MultipleEventTest().suite()
    unittest.TextTestRunner(verbosity=2).run(suite)

    DataAccess('./data').empty_dirs(delete=True)