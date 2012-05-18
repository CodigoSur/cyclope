import re
import time
import unittest

import nohang

class TestNohang(unittest.TestCase):
    data = "95756, KURN , 20110311, 2130, -34.00, 151.21, 260, 06.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999.0, -9999, -9999, 07.0, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -9999, -"

    def test_creation(self):

        def function(arg1, arg2, arg3=3):
            return arg1, arg2, arg3

        result, success = nohang.run(function, args=("1", "2"), kwargs={"arg3":"foo"},
                                     wait=0.5)
        self.assertTrue(success)
        self.assertEqual(result[0], "1")
        self.assertEqual(result[1], "2")
        self.assertEqual(result[2], "foo")

        result, success = nohang.run(function, args=("1", "2"), wait=0.1)

        self.assertTrue(success)
        self.assertEqual(result[0], "1")
        self.assertEqual(result[1], "2")
        self.assertEqual(result[2], 3)

    def test_simple(self):
        wait, SLEEP = 0.5, 5
        start = time.time()
        result, success = nohang.run(time.sleep, (SLEEP, ), wait=wait)

        interval = time.time() - start
        self.assertFalse(success)
        self.assertTrue(result is None)

        self.assertTrue(interval < SLEEP)
        self.assertTrue(interval > wait)

    def test_c_code(self):
        rgex = re.compile('^(\d{5}), .+?, (\d{8}), (\d{4}), .+?, .+?,' + 37 * ' (.*?),' + ' (.*?)$')

        result, success = nohang.run(rgex.match, args=(self.data, ), wait=0.1)
        self.assertFalse(success)



