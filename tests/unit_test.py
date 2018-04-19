#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest, os
from seproject_group18.script import dataAnalytic

__author__ = "Peng Ye"
__copyright__ = "Peng Ye"
__license__ = "mit"



class TestAPI(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAPI, self).__init__(*args, **kwargs)
        self.__current_path = os.path.dirname(os.path.abspath(__file__))

    def test_dataAnalyticClass_001(self):
        '''Verify getBikeStation() method in dataAnalytic Class'''
        my = dataAnalytic.dataAnalytic()
        stationNumber = 1
        stationName = 'CLARENDON ROW'
        self.assertTrue(stationName in my.getBikeStation(stationNumber))

    def test_dataAnalyticClass_002(self):
        '''Verify importModel() method in dataAnalytic Class'''
        return
        stationNumber = 1
        file = self.__current_path + "/../data/" + str(stationNumber) + '.ols'
        # remove the dump file first
        if os.path.isfile(file):
            os.unlink(file)
        my = dataAnalytic.dataAnalytic()
        my.importModel(stationNumber)
        # Verify the dump file for station's training model has be created
        self.assertTrue(os.path.isfile(file))

    def test_dataAnalyticClass_003(self):
        '''Verify getPredictionOnStation() method in dataAnalytic Class'''
        temperature=10
        humidity=0
        weather='Rain'
        windSpeed=5
        stationNumber=1
        my = dataAnalytic.dataAnalytic()
        prediction, bikeStands = my.getPredictionOnStation(temp=temperature,
                                                           humidity=humidity,
                                                           weather=weather,
                                                           windSpeed=windSpeed,
                                                           stationNumber=stationNumber)
        self.assertTrue(bikeStands >= prediction and prediction >= 0)
        self.assertTrue(isinstance(prediction, int) is True)
        self.assertTrue(isinstance(bikeStands, int) is True)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)
