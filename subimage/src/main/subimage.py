import sys
import cv2
import itertools as it
import math
import numpy as np
import numpy.linalg as linal

#default threshold (max = 255*sqrt(3) )
threshold_percent = 0.015
threshold_percent = 0.05
threshold = math.ceil(255*math.sqrt(3)*threshold_percent) #6

_asdf = 10


def savejpeg(fname, img, quality=95):
	cv2.imwrite(fname, img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
	return


# p : (y, x)
def computeMaxDelta(p:(int,int), img1, img2):
	yFrom,xFrom = p
	yTo = yFrom + img2.shape[0]
	xTo = xFrom + img2.shape[1]
	img = img1[yFrom:yTo, xFrom:xTo, :]
	deltas = linal.norm(img-img2, axis=2)
	return np.amax(deltas)


def computePoint0Delta(p:(int,int), img1, img2):
	return linal.norm(img1[p] - img2[0,0])


def findMatch(img1, img2):
	#how many comparisons along Y and X axes
	DY = img1.shape[0]-img2.shape[0]+1
	DX = img1.shape[1]-img2.shape[1]+1
	
	for p in it.product(range(DY), range(DX)):
		delta0 = computePoint0Delta(p, img1, img2)
		if delta0 <= threshold:
			deltaMax = computeMaxDelta(p, img1, img2)
			if deltaMax <= threshold:
				return p+(deltaMax,)
	
	return None
	

def drawRectangle(p, img1, img2):
	yFrom,xFrom = p
	yTo = yFrom+img2.shape[0]
	xTo = xFrom+img2.shape[1]
	img1[yFrom,xFrom:xTo,2] = 255
	img1[yTo,xFrom:xTo,2] = 255
	img1[yFrom:yTo,xFrom,2] = 255
	img1[yFrom:yTo,xTo,2] = 255
	savejpeg("../target/tmp.jpg", img1, 100)
	return


def main(f1, f2):
	#at this point the caller must ensure that sizes f1 >= f2
	
	#read into ndarray with shape (Y, X, 3) and convert dtype to int16
	#note: the last dimension is not RGB but BGR order
	img1 = np.int16(cv2.imread(f1))
	img2 = np.int16(cv2.imread(f2))
	
	p = findMatch(img1, img2)
	
	if p is None:
		print("not found")
	else:
		print("found at (x,y) = ("+str(p[1])+","+str(p[0])+")")
		print("max delta: "+str(p[2]))
		drawRectangle(p[:2], img1, img2)
		#drawRectangle((147,412), img1, img2)
	return



if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])
	print("done")

