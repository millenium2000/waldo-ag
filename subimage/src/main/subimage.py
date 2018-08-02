import sys, os, argparse
import cv2
import itertools as it
import math
import numpy as np
import numpy.linalg as linal


def jpegSave(fname, img, quality=95):
	#TODO: make sure all needed sub-folders exist and file can be written
	cv2.imwrite(fname, img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
	return


def jpegLoad(fname):
	#read into ndarray with shape (Y, X, 3) and convert dtype to int16
	# the last dimension is not RGB but BGR order
	img = cv2.imread(fname)
	if img is None:
		raise Exception("could not read '{}' file (pwd is '{}')".format(fname, os.getcwd()))
	#convert into signed integers
	img = np.int16(img)
	return img


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


def drawRectangle(p, img, rect):
	yFrom,xFrom = p
	yTo = yFrom+rect[0]
	xTo = xFrom+rect[1]
	img[yFrom,xFrom:xTo,2] = 255
	img[yTo,xFrom:xTo,2] = 255
	img[yFrom:yTo,xFrom,2] = 255
	img[yFrom:yTo,xTo,2] = 255
	return


def findLargest(img1, img2):
	Y1, X1, _ = img1.shape
	Y2, X2, _ = img2.shape
	if Y1==Y2:
		if X1<X2:
			return (img2, img1, True)
		return (img1, img2, False)
	elif Y1>Y2:
		if X1<X2:
			return None
		return (img1, img2, False)
	else:
		if X1<=X2:
			return (img2, img1, True)
		return None


def run(fname1:str, fname2:str, similarity:float=0.95, fnameOut:str=None):
	#convert from similarity in % into max threshold in RGB distance
	if similarity<0.0 or similarity>1.0:
		raise Exception("invalid similarity provided '{}' must be between 0.0 and 1.0".format(similarity))
	threshold = math.ceil(255.0*math.sqrt(3)*(1.0-similarity))
	
	#load files into (Y, X, 3) arrays
	img1 = jpegLoad(fname1)
	img2 = jpegLoad(fname2)
	
	#find the biggest image (if exists) and put it into img1
	tpl = findLargest(img1, img2)
	if tpl is None:
		return None
	img1, img2, _ = tpl
	
	#how many comparisons along Y and X axes
	DY = img1.shape[0]-img2.shape[0]+1
	DX = img1.shape[1]-img2.shape[1]+1
	
	for p in it.product(range(DY), range(DX)):
		delta0 = computePoint0Delta(p, img1, img2)
		if delta0 <= threshold:
			deltaMax = computeMaxDelta(p, img1, img2)
			if deltaMax <= threshold:
				if fnameOut is not None:
					drawRectangle(p, img1, img2.shape)
					jpegSave(fnameOut, img1, 100)
				similar = 1.0 - deltaMax / (255.0*math.sqrt(3))
				return p+(similar, deltaMax)
	return None


def main():
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('file1',
		help='first input jpeg image file name')
	parser.add_argument('file2',
		help='second input jpeg image file name')
	parser.add_argument('-s', '--similarity', type=float, default=0.95, metavar="FROM_0.0_TO_1.0",
		help='minimum similarity threshold')
	parser.add_argument('-o', '--out', type=str, default=None, metavar="FILE_NAME",
		help='filename of the image to save (with bounding rectangle around found sub-image location)')
	opts = parser.parse_args()
	
	res = run(opts.file1, opts.file2, opts.similarity, opts.out)
	
	if res is None:
		print("not found")
		return 1
	print("found {:0.4f} similarity at (x,y) = ({},{})".format(res[2], res[1], res[0]))
	return 0


if __name__ == "__main__":
	res = main()
	sys.exit(res)

