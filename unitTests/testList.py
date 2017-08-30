#!/usr/bin/python	
import unittest
import inspect
 
class TestLists(unittest.TestCase):
 
    def setUp(self):
        self.logPoint()
        self.myList = [1, 2, 3, 4]
 
    def test_len(self):
        self.logPoint()
        self.assertEqual( len(self.myList), 4 )
        self.myList.append(-1)
        self.assertEqual( len(self.myList), 5 )
 
    def test_min(self):
        self.logPoint()
        self.assertEqual( min(self.myList) , 1 )
 
    def tearDown(self):
        self.logPoint()
 
    def logPoint(self):
        currentTest = self.id().split('.')[-1]
        callingFunction = inspect.stack()[1][3]
        print 'in %s - %s()' % (currentTest, callingFunction)
    
if __name__ == '__main__':
    unittest.main()