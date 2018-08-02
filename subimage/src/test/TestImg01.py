import unittest
import main.subimage as si

class OneBasicTest(unittest.TestCase):
	
	def test_test(self):
		si.main("../img/img-01/img-01-100.jpg", "../img/img-01/img-01-smpl-01-100.jpg")
		self.assertEqual(1, 2, "one equals 1")
