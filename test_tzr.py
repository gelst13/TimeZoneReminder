import unittest
import tzr_utils


class TestTimeKeeper(unittest.TestCase):  # a test case for the calculator.py module

    def test_calculate_time(self):
        # tests for the calculate_time() method
        time_point = (2022, 8, 4, 12, 50, 00, 3, 216, 0)  # 12:50 04-08-2022
        self.assertEqual(tzr_utils.TimeKeeper.calculate_time(time_point, [0, 10]), '13:00')
        self.assertEqual(tzr_utils.TimeKeeper.calculate_time(time_point, [1, 10]), '14:00')
        self.assertEqual(tzr_utils.TimeKeeper.calculate_time(time_point, [10, 10]), '23:00')


