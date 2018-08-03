
import datetime

import sys
sys.path.append('src')
import main.subimage as si


similarity = 0.95

subdir = "img/img-01/"

fname = "target/TestImg01Permutations.html"

masterFiles = [
	"img-01-050.jpg",
	"img-01-055.jpg",
	"img-01-060.jpg",
	"img-01-065.jpg",
	"img-01-070.jpg",
	"img-01-075.jpg",
	"img-01-080.jpg",
	"img-01-085.jpg",
	"img-01-090.jpg",
	"img-01-095.jpg",
	"img-01-100.jpg",
]

cropTests = [
	{"fname":"img-01-smpl-01-050.jpg", "expect":(147, 413)},
	{"fname":"img-01-smpl-01-055.jpg", "expect":(147, 413)},
	{"fname":"img-01-smpl-01-060.jpg", "expect":(147, 413)},
	{"fname":"img-01-smpl-01-065.jpg", "expect":(147, 413)},
	{"fname":"img-01-smpl-01-070.jpg", "expect":(147, 413)},
	{"fname":"img-01-smpl-01-075.jpg", "expect":(147, 413)},
	{"fname":"img-01-smpl-01-080.jpg", "expect":(147, 413)},
	{"fname":"img-01-smpl-01-085.jpg", "expect":(147, 413)},
	{"fname":"img-01-smpl-01-090.jpg", "expect":(147, 413)},
	{"fname":"img-01-smpl-01-095.jpg", "expect":(147, 413)},
	{"fname":"img-01-smpl-01-100.jpg", "expect":(147, 413)},
	
	{"fname":"img-01-smpl-02-050.jpg", "expect":(380, 335)},
	{"fname":"img-01-smpl-02-055.jpg", "expect":(380, 335)},
	{"fname":"img-01-smpl-02-060.jpg", "expect":(380, 335)},
	{"fname":"img-01-smpl-02-065.jpg", "expect":(380, 335)},
	{"fname":"img-01-smpl-02-070.jpg", "expect":(380, 335)},
	{"fname":"img-01-smpl-02-075.jpg", "expect":(380, 335)},
	{"fname":"img-01-smpl-02-080.jpg", "expect":(380, 335)},
	{"fname":"img-01-smpl-02-085.jpg", "expect":(380, 335)},
	{"fname":"img-01-smpl-02-090.jpg", "expect":(380, 335)},
	{"fname":"img-01-smpl-02-095.jpg", "expect":(380, 335)},
	{"fname":"img-01-smpl-02-100.jpg", "expect":(380, 335)},
	
	{"fname":"img-01-smpl-03-n-050.jpg"},
	{"fname":"img-01-smpl-03-n-055.jpg"},
	{"fname":"img-01-smpl-03-n-060.jpg"},
	{"fname":"img-01-smpl-03-n-065.jpg"},
	{"fname":"img-01-smpl-03-n-070.jpg"},
	{"fname":"img-01-smpl-03-n-075.jpg"},
	{"fname":"img-01-smpl-03-n-080.jpg"},
	{"fname":"img-01-smpl-03-n-085.jpg"},
	{"fname":"img-01-smpl-03-n-090.jpg"},
	{"fname":"img-01-smpl-03-n-095.jpg"},
	{"fname":"img-01-smpl-03-n-100.jpg"},
	{"fname":"img-01-smpl-04-n-050.jpg"},
	{"fname":"img-01-smpl-04-n-055.jpg"},
	{"fname":"img-01-smpl-04-n-060.jpg"},
	{"fname":"img-01-smpl-04-n-065.jpg"},
	{"fname":"img-01-smpl-04-n-070.jpg"},
	{"fname":"img-01-smpl-04-n-075.jpg"},
	{"fname":"img-01-smpl-04-n-080.jpg"},
	{"fname":"img-01-smpl-04-n-085.jpg"},
	{"fname":"img-01-smpl-04-n-090.jpg"},
	{"fname":"img-01-smpl-04-n-095.jpg"},
	{"fname":"img-01-smpl-04-n-100.jpg"},
]


def msg(exp, act):
	if act is None:
		s = "expecting {}; actual None".format(exp)
	else:
		s = "expecting {}; actual {} with similarity {:0.4f}".format(exp, act[:2], act[2])
	return s


def main():
	dtsStart = datetime.datetime.now()
	isPassAll = True
	resultsTable = []
	for tc in cropTests:
		resultsRow = []
		for f1 in masterFiles:
			f2 = tc["fname"]
			expectPoint = tc.get("expect")
			expectToFind = expectPoint is not None
			print("testing {} and {} files".format(f1,f2))
			
			res = si.run(subdir+f1, subdir+f2, similarity)
			
			#verify
			isPass = None
			if res is None:
				isPass = not expectToFind
			else:
				if expectToFind:
					isPass = expectPoint==res[:2]
				else:
					isPass = False
			
			#update global isPassAll and resultsTable
			if not isPass:
				isPassAll = False
			
			#append result row
			resultsRow.append( (f1, f2, isPass, msg(expectPoint, res)) )
		
		resultsTable.append(resultsRow)
	
	dtsStop = datetime.datetime.now()
	
	#create an output HTML
	s = formatAllCasesHtml(resultsTable, isPassAll, dtsStart, dtsStop)
	with open(fname, "w") as f : f.write(s)
	print("Overall status : "+("Pass" if isPassAll else "Fail"))
	print("Look for detailed results in \n    "+fname+"")
	
	return isPassAll
	
	
	
def formatAllCasesHtml(resultsTable, isPassAll, dtsStart, dtsStop):
	def pcls(isPass):
		return "x-pass" if isPass else "x-fail"
	def ptxt(isPass, sPass=None, sFail=None):
		res = sPass if isPass else sFail
		return res if res is not None else ""
	def row(resultsRow):
		ss = []
		fname = None
		for _,f2,isPass,msg in resultsRow:
			fname = f2
			ss.append("<td class='{0}'>{1}</td>".format(pcls(isPass), ptxt(isPass,msg,msg)))
		return "<tr><td>"+fname+"</td>" + "".join(ss) + "</tr>"
		
	data = {
		"dtsStart" : str(dtsStart),
		"dtsStop" : str(dtsStop),
		"gCStat" : pcls(isPassAll),
		"gTStat" : ptxt(isPassAll, "Pass", "Fail"),
		"dHDR" : "<td></td>"+"".join(["<td>"+x+"</td>" for x in masterFiles]),
		"dBODY" : "\n\t\t\t\t\t".join([row(x) for x in resultsTable])
	}
	return '''
		<!DOCTYPE html>
		<html>
		<head>
			<style>
				table, th, td {{ border: 1px solid black; }}
				table {{width:100%%}}
				.x-pass {{background:lightgreen;}}
				.x-fail {{background: lightcoral;}}
			</style>
			<title>TestImg01Permutations</title>
		</head>
		
		<body>
		<h1>TestImg01Permutations</h1>
		<div>Status: <span class='{gCStat}'>{gTStat}</span></div>
		<div>Started: <span>{dtsStart}</span></div>
		<div>Finished: <span'>{dtsStop}</span></div>
		<table>
			<thead>
				<tr>{dHDR}</tr>
			</thead>
			<tbody>
				{dBODY}
			</tbody>
		</table>
		</body>
		</html>
	'''.format(**data)


if __name__ == '__main__':
	started = datetime.datetime.now()
	print("Starting : "+str(started))
	res = main()
	print("Started : "+str(started))
	print("Finished : "+str(datetime.datetime.now()))
	sys.exit(0 if res else 1)



