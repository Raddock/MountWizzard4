############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
###########################################################
# standard libraries
import unittest
# external packages
import PyQt5.QtCore
# local import
import mw4_main
import mw4_global


class MainTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_app = PyQt5.QtWidgets.QApplication([])

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        mw4_global.work_dir = '/Users/mw/PycharmProjects/MountWizzard4'
        mw4_global.config_dir = '/Users/mw/PycharmProjects/MountWizzard4/config'
        main = mw4_main.MountWizzard4()

    def tearDown(self):
        pass

    #
    #
    # testing main
    #
    #

    def test_loadConfig_ok1(self):
        filePath = '/Users/mw/PycharmProjects/MountWizzard4/config/config0.cfg'

        suc = main.loadConfig(filePath=filePath)
        self.assertEqual(True, suc)
        self.assertEqual('4.0', main.config['version'])

    def test_loadConfig_ok2(self):
        filePath = '/Users/mw/PycharmProjects/MountWizzard4/config/config0.cfg'

        suc = main.loadConfig(filePath=filePath)
        self.assertEqual(True, suc)
        self.assertEqual('4.0', main.config['version'])

    def test_loadConfig_ok3(self):

        suc = main.loadConfig()
        self.assertEqual(True, suc)

    def test_loadConfig_not_ok1(self):
        filePath = '/Users/mw/PycharmProjects/MountWizzard4/config/config_nok1.cfg'

        suc = main.loadConfig(filePath=filePath)
        self.assertEqual(True, suc)

    def test_loadConfig_not_ok2(self):
        filePath = '/Users/mw/PycharmProjects/MountWizzard4/config/config_nok2.cfg'

        suc = main.loadConfig(filePath=filePath)
        self.assertEqual(False, suc)

    def test_loadConfig_not_ok3(self):
        filePath = '/Users/mw/PycharmProjects/MountWizzard4/config/config_nok3.cfg'

        suc = main.loadConfig(filePath=filePath)
        self.assertEqual(False, suc)

    def test_loadConfig_not_ok4(self):
        filePath = '/Users/mw/PycharmProjects/MountWizzard4/config/config_nok4.cfg'

        suc = main.loadConfig(filePath=filePath)
        self.assertEqual(False, suc)

    def test_loadConfig_not_ok5(self):
        filePath = '/Users/mw/PycharmProjects/MountWizzard4/config/config_nok5.cfg'

        suc = main.loadConfig(filePath=filePath)
        self.assertEqual(False, suc)

    def test_saveConfig_ok1(self):
        filePath = '/Users/mw/PycharmProjects/MountWizzard4/config/test.cfg'

        suc = main.saveConfig(filePath=filePath)
        self.assertEqual(True, suc)
