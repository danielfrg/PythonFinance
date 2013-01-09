import unittest

from finance.test.utils.DateUtils import DateUtilsTest
from finance.test.utils.CalculatorTypes import CalculatorTypesTest
from finance.test.utils.CalculatorValues import CalculatorValuesTest
from finance.test.utils.FileManager import FileManagerTest
from finance.test.utils.DataAccess import DataAccessTest

from finance.test.sim.MarketSimulator import MarketSimulatorTest

from finance.test.events.PastEvent import PastEventTest
from finance.test.events.EventFinder import EventFinderTest
from finance.test.events.MultipleEvents import MultipleEventsTest

suite = unittest.TestSuite()

suite.addTest(DateUtilsTest().suite())
suite.addTest(CalculatorTypesTest().suite())
suite.addTest(CalculatorValuesTest().suite())
suite.addTest(FileManagerTest().suite())
suite.addTest(DataAccessTest().suite())

suite.addTest(MarketSimulatorTest().suite())

suite.addTest(PastEventTest().suite())
suite.addTest(EventFinderTest().suite())
suite.addTest(MultipleEventsTest().suite())

unittest.TextTestRunner(verbosity=2).run(suite)