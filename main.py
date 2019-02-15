import operator
from collections import OrderedDict

def MsGsp():
	
	file = open('para1-1.txt','r')
	text = file.read().split('\n') 
	MIS = {}
	M = []
	S = []
	seqCount = 0

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


	for line in text:
		if line.find("SDC") == -1:
			if(len(line.strip()) != 0):
				index = int(BetweenBracket(line,'(',')').strip())
				value = float(AfterEqualTo(line, '=').strip())
				MIS[index] = value
		elif(len(line.strip()) != 0):
				SDC = float(AfterEqualTo(line, '=').strip())


	for i in sorted(MIS, key=MIS.get, reverse=False) :
		M.append(i)

	seqCount = len(S)


	# L = init_pass(M, S);	

def level-2():
	for i in range(0, len(L)):
	    #print(MIS[L[i][0]])
	    if (L[i][1]/n) >= MIS[L[i][0]]:
	        for j in range(i+1, len(L)):
	            temp = []
	            temp1 = []
	            temp2 = []
	            if ((L[j][1]/n) >= MIS[L[i][0]]) & (abs(L[j][1]/n - L[i][1]/n) <= sdc):
	                temp.append(L[i][0])
	                temp.append(L[j][0])
	                C2.append(temp)
	                temp1.append(L[i][0])
	                temp2.append(L[j][0])
	                temp = []
	                temp.append(temp1)
	                temp.append(temp2)
	                C2.append(temp)

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
    MsGsp()