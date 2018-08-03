import unittest

import sys
sys.path.append('src')
import main.subimage as si


class TestImg01(unittest.TestCase):


	def testOneCase(self):
		#found 0.9885 similarity at (x,y) = (413,147)
		res = si.run("img/img-01/img-01-100.jpg", "img/img-01/img-01-smpl-01-100.jpg")
		self.assertTrue(res, "should not be None")
		self.assertEqual((147, 413), res[:2])
		return


	def testSameImage(self):
		#found 1.0000 similarity at (x,y) = (0,0)
		res = si.run("img/img-01/img-01-100.jpg", "img/img-01/img-01-100.jpg")
		self.assertTrue(res, "should not be None")
		self.assertEqual((0,0), res[:2])
		return


if __name__ == '__main__':
	unittest.main()
