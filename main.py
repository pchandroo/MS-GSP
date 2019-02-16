import operator
from collections import OrderedDict

def readInput():
	
	#Reading Sequence file
	S = []
	Slines = []
	with open ('data-1.txt', 'rt') as Sfile:
	    for line in Sfile:
	        Slines.append(line.rstrip('\n'))
	lstrip = []
	for line in Slines:
	    lstrip.append(line[2:-2])
	lbrace = []
	for i in lstrip:
	    lbrace.append(i.split("}{"))
	for i in lbrace:
	    temp = []
	    for j in i:
	        temp.append(j.split(', '))    
	    S.append(temp)

	#Reading requirements file
	MIS = {}
	file = open('para1-1.txt','r')
	text = file.read().split('\n')
	for line in text:
		if line.find("SDC") == -1:
			if(len(line.strip()) != 0):
				index = int(BetweenBracket(line,'(',')').strip())
				value = float(AfterEqualTo(line, '=').strip())
				MIS[index] = value
		elif(len(line.strip()) != 0):
				SDC = float(AfterEqualTo(line, '=').strip())
	#print("S:\n", S)
	#print("MIS\n", MIS)
	#print("SDC\n", SDC)

	return S, MIS, SDC

def MsGsp(S, MIS, SDC):

	M = []	
	seqCount = 0
	L = []
	CountMap = {}
	LMap = {}
	F1 = []

	for i in sorted(MIS, key=MIS.get, reverse=False) :
		M.append(i)

	seqCount = len(S)

	for i in M:
		count = 0
		for row in S:
			for elem in row:
				if(elem.count(str(i))):
					count = count + 1
					CountMap[i] = count
					break

	for i in M:
		if i not in CountMap: 
			M.remove(i)

	#print("M\n", M)

	L = init_pass(M,CountMap,seqCount,MIS,LMap)

	#print("L\n", L)

	for i in range(len(L)):
		support = float(L[i][1])/seqCount
		if(support >= MIS[L[i][0]]):
			 F1.append(L[i][0])

	#print("F1\n", F1)


def init_pass(M,CountMap,seqCount,MIS,LMap):

	counter = 0
	for i in M:
		support = float(CountMap[i])/float(seqCount)
		if(support < MIS[i]):
			counter = counter + 1
		else:
			break

	checkMIS = MIS[M[counter]]
	LMap[M[counter]] = CountMap[M[counter]]		

	for i in M[counter+1:]:
		support = float(CountMap[i])/float(seqCount)
		if(support>=checkMIS):
			LMap[i] = CountMap[i]

	add_to_L = [ [k,v] for k, v in LMap.items() ]
	return add_to_L		


#below function need L(list of tuple with (item,count)), MIS(dict{(item:MIS)}), n, sdc 
def level_2():
	for i in range(0, len(L)):
		C2.append([[L[i][0]], [L[i][0]]])
		C2.append([[L[i][0], L[i][0]]])
		if (L[i][1]/n) >= MIS[L[i][0]]:
			for j in range(i+1, len(L)):
				if ((L[j][1]/n) >= MIS[L[i][0]]) & (abs(L[j][1]/n - L[i][1]/n) <= sdc):
					if L[i][0] < L[j][0]:
						C2.append([[L[i][0], L[j][0]]])
					else:
						C2.append([[L[j][0], L[i][0]]])
					C2.append([[L[i][0]], [L[j][0]]])
					C2.append([[L[j][0]], [L[i][0]]])
	return C2


def BetweenBracket(text, a, b):
	pos_a = text.find(a)
	if pos_a == -1: return ""
	pos_b = text.rfind(b)
	if pos_b == -1: return ""
	adjusted_pos_a = pos_a + len(a)
	if adjusted_pos_a >= pos_b: return ""
	return text[adjusted_pos_a:pos_b]

def AfterEqualTo(text, a):
	pos_a = text.rfind(a)
	if pos_a == -1: return ""
	adjusted_pos_a = pos_a + len(a)
	if adjusted_pos_a >= len(text): return ""
	return text[adjusted_pos_a:]

if __name__ == '__main__':
	S, MIS, SDC = readInput()
	MsGsp(S, MIS, SDC)