'''
Created on Jun 23, 2011

@author: kykamath
'''
import unittest, sys
sys.path.append('../')
from datetime import datetime, timedelta
from classes import GeneralMethods, TwoWayMap, PatternMap, UNIQUE_LIBRARY_KEY

test_time = datetime.now()

class GeneralMethodsTests(unittest.TestCase):
    def test_callMethodEveryInterval(self):
        self.numberOfTimesInMethod, currentTime, final_time = 1, test_time, test_time+timedelta(minutes=60)
        def method(arg1, arg2): 
            self.numberOfTimesInMethod+=1
            self.assertEqual(test_time+timedelta(minutes=15*self.numberOfTimesInMethod), arg2+timedelta(minutes=arg1))
        while currentTime<=final_time:
            GeneralMethods.callMethodEveryInterval(method, timedelta(minutes=15), currentTime, arg1=15, arg2=currentTime)
            currentTime+=timedelta(minutes=1)

class PatternMapTests(unittest.TestCase):
    def test_basicOperation(self):
        pm = PatternMap()
        pm[UNIQUE_LIBRARY_KEY+str(10)]=12
        pm.setdefault(UNIQUE_LIBRARY_KEY+str(12),12)
        self.assertEqual({'::ilab::12': 12, '::ilab::10': 12}, pm)
        
class TwoWayDictTests(unittest.TestCase):
    def setUp(self):
        self.twoWayMap = TwoWayMap()
        self.assertRaises(TypeError, self.twoWayMap.set, (5, 1, 2))
        self.twoWayMap.set(TwoWayMap.MAP_FORWARD, 'a', 'A')
        self.twoWayMap.set(TwoWayMap.MAP_REVERSE, 'B', 'b')
    def test_basicOperation(self):
        self.assertEqual('A', self.twoWayMap.get(TwoWayMap.MAP_FORWARD, 'a'))
        self.assertEqual('a', self.twoWayMap.get(TwoWayMap.MAP_REVERSE, 'A'))
        self.assertEqual('B', self.twoWayMap.get(TwoWayMap.MAP_FORWARD, 'b'))
        self.assertEqual('b', self.twoWayMap.get(TwoWayMap.MAP_REVERSE, 'B'))
        self.assertEqual({'::ilab::b': 'B', '::ilab::a': 'A'}, self.twoWayMap.getMap(self.twoWayMap.MAP_FORWARD))
        self.assertEqual({'::ilab::B': 'b', '::ilab::A': 'a'}, self.twoWayMap.getMap(self.twoWayMap.MAP_REVERSE))
    def test_delete(self):
        self.twoWayMap.remove(TwoWayMap.MAP_FORWARD, 'a')
        self.assertEqual({'::ilab::b': 'B'}, self.twoWayMap.getMap(self.twoWayMap.MAP_FORWARD))
        self.assertEqual({'::ilab::B': 'b'}, self.twoWayMap.getMap(self.twoWayMap.MAP_REVERSE))
    def test_length(self):
        self.assertEqual(2, len(self.twoWayMap))
        self.twoWayMap.set(TwoWayMap.MAP_REVERSE, 'C', 'c')
        self.assertEqual(3, len(self.twoWayMap))
if __name__ == '__main__':
    unittest.main()