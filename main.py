import copy
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
	F = {}

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

	MScandidateGen(F,M,CountMap,SDC,MIS)


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


def MScandidateGen(F,M,CountMap,SDC,MIS):
	F[2] = [[[20, 30]], [[20], [30]], [[20, 70]], [[20], [70]], [[20], [80]], [[30], [30]], [[30, 70]], [[30], [70]], [[30, 80]], [[30], [80]], [[70], [70]], [[70, 80]], [[80], [70]], [[10, 40]], [[10], [40]], [[40], [40]]]
	# F[2] = [[[20, 30, 40]], [[40], [70]]]
	C = []
	for i in range(len(F[2])):
		for j in range(len(F[2])):
			s1 = F[2][i]
			s2 = F[2][j]
			first_s1 = getFirstItem(s1)
			last_s1 =  getLastItem(s1)
			first_s2 = getFirstItem(s2)
			last_s2 =  getLastItem(s2)
			MIS_least_seq = getMISofSequence(s1,MIS)
			
			if( MIS[first_s1] < MIS_least_seq ):
				if( (removeItem(s1,1) == removeItem(s2,Length(s2)-1)) & (MIS[last_s2] > MIS[first_s1]) ):
					if(Size(LastElement(s2)) == 1):	
						c1 = []		
						c1 = s1
						c1.append(LastElement(s2))
						C.append(c1)

						if( (Length(s1) == 2 & Size(s1) == 2) & (getLastItem(s2) > getLastItem(s1)) ):
							c2 = []
							c2 = s1
							last_c2 = LastElement(c2)
							last_c2.extend(getLastItem(s2))
							# removeItem(c2,Length(c2)-1)
							C.append(c2)
					elif( ((Length(s1) == 2 & Size(s1) == 1) & (getLastItem(s2) > getLastItem(s1))) | ( Length(s1) > 2 ) ):
						c2 = []
						c2 = s1	
						last_item_s2 = getLastItem(s2)	
						last_c2 = LastElement(c2)
						last_c2.append(last_item_s2)
						C.append(c2)

			elif( MIS[getLastItem(s2)] <  getMISofSequence(s2,MIS) ):	
				if( (removeItem(s2,1) == removeItem(s1,Length(s1)-1)) & (MIS[first_s1] > MIS[last_s2]) ):
					if(Size(FirstElement(s1)) == 1):	
						c1 = []		
						c1 = s2
						c1.append(FirstElement(s1))
						C.append(c1)
							
						if( (Length(s2) == 2 & Size(s2) == 2) & (getFirstItem(s1) > getFirstItem(s2)) ):
							c2 = []
							c2 = s2
							last_c2 = FirstElement(c2)
							last_c2.extend(getFirstItem(s1))
							# removeItem(c2,0)
							C.append(c2)
					elif( ((Length(s2) == 2 & Size(s2) == 1) & (getFirstItem(s1) > getFirstItem(s2))) | ( Length(s2) > 2 ) ):
						c1 = []
						c1 = s2	
						last_item_s1 = getFirstItem(s1)	
						last_c1 = FirstElement(c1)
						last_c1.append(last_item_s1)
						C.append(c1)

			else:					
				if(removeItem(s1,0) == removeItem(s2,Length(s2)-1)):
					if(Size(LastElement(s2)) == 1):	
						c1 = []
						c1 = s1
						c1.append(LastElement(s2))
						C.append(c1)
					if(Size(LastElement(s2)) > 1):
						c1 = []
						c1 = s1	
						last_item_s2 = getLastItem(s2)	
						last_c1 = LastElement(c1)
						last_c1.extend(last_item_s2)
						# removeItem(c1,Length(c1)-1)
						C.append(c1)

	return C					


def getFirstItem(s):
	first = 0
	for i in s:
		first =i[0]
		break
	return first

def getLastItem(s):
	last = 0
	for i in s:
		last = i[-1]
	return last	


def removeItem(s,index):

		seqnew = copy.deepcopy(s)
		length = Length(s)
		if index < 0 or index >= length:
			return []
		count = 0
		for element in seqnew:
			if count + len(element) <= index:
				count += len(element)
			else:
				del element[index - count]
				break
		return [element for element in seqnew if len(element) > 0]


def getMISofSequence(s,MIS):
	temp = []
	MIS_array = []
	for i in s:
		for j in range(len(i)):
			temp.append(i[j])

	for elem in temp:
		MIS_array.append(MIS[elem])

	return min(MIS_array)	


def Size(s):
   return len(s)


def Length(s):
   l = 0
   for i in s:
       l += len(i)
   return l

def LastElement(s):
   last = s[-1]
   return last

def FirstElement(s):
   first = s[0]
   return first   

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