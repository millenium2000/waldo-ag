import unittest

import sys
sys.path.append('src')
import main.subimage as si


class TestImg01(unittest.TestCase):
	
	def testOneCase(self):
		res = si.run("img/img-01/img-01-100.jpg", "img/img-01/img-01-smpl-01-100.jpg")
		self.assertTrue(res, "should not be None")
		#found 0.9885 similarity at (x,y) = (413,147)
		self.assertEqual((413,147), (res[1], res[0]), "should be found")



if __name__ == '__main__':
	unittest.main()
