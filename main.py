import copy
import operator
from collections import OrderedDict
import math
from copy import deepcopy

def readInput():
	
	#Reading Sequence file
	S = []
	Slines = []
	with open ('data.txt', 'rt') as Sfile:
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
	    temp1 = []
	    for j in i:
	        temp1.append(j.split(', '))
	        for x in temp1:
	        	x = list(map(int, x))
	        temp.append(x)
	        temp1 = []
	        #print("Temp", temp)
	    S.append(temp)

	#Reading requirements file
	MIS = {}
	file = open('para.txt','r')
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
	F = []

	for i in sorted(MIS, key=MIS.get, reverse=False) :
		M.append(i)


	seqCount = len(S)

	for i in M:
		count = 0
		for row in S:
			for elem in row:
				if(elem.count(i)):
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
	
#	F = Generation(L, MIS, seqCount, S, F1, SDC)



	#print("L", L)
	#print("MIS", MIS)
	#print("seqCount", seqCount)
	#print("SDC", SDC)
	#print("S", S)
	#print("F1", F1)
	#print("M", M)

#def Generation(L, MIS, seqCount, S, F1, SDC):
	#for f in F1:
	#	F.append([[f]])
	output_file = open("Output_GS-MSP.txt", "w")
	output_file.write("The number of length 1 sequential pattern is " +str(len(F1))+"\n")
	for f in F1:
		print_s = "Pattern : <{" + str(f) + " }"
		print_s += ">"
		output_file.write(print_s+"\n")



	k = 2
	
	Ck = []

	while(True):
		#print("K", k)
		if k == 2:
			Ck = level_2(L, MIS, seqCount, SDC)
		else:
			Ck = MScandidateGen(Fk, M, CountMap, SDC, MIS)

		#print("C", Ck)
		#print("Length of C", len(Ck))
		SupCount = [0] * len(Ck)
		for c in range(len(Ck)):
			temp_count = 0
			for s in S:
				if Sub(Ck[c], s):
					temp_count += 1
			SupCount[c] = temp_count

		#print("Count",SupCount)
		Fk = []
		for c in range(len(Ck)):
			if SupCount[c]/seqCount >= MinMIS(Ck[c], MIS):
				Fk.append(Ck[c])
		#F.extend(Fk)
		#print("Fk", Fk)
		#print("Length of Fk", len(Fk))
		Fk = Remove_duplicate(Fk)

		if(len(Fk) == 0):
			break

		output_file.write("The number of length: "+ str(k) +" sequential pattern is " +str(len(Fk))+"\n")
		for f in Fk:
			print_s = "Pattern : <"
			for s in f:
				print_s += "{"
				for i in s:
					print_s += str(i) + " "
				print_s += "}"
				print_s += ">"
			output_file.write(print_s+"\n")
		k += 1

def Remove_duplicate(d): 
    final = [] 
    for n in d: 
        if n not in final: 
            final.append(n) 
    return final

def Subset(Ck, s):
    if len(list(set(Ck))) != len(Ck):
        return False
    for i in Ck:
        if i not in s:
            return False
    return True

def Sub(Ck, s):
    m = {}
    counter = 0
    for i in Ck:
        isThere = False
        j = counter
        while j < len(s):
            if j in m:
                continue
            else:
                if Subset(i, s[j]):
                    m[j] = True
                    isThere = True
                    counter = j+1
                    break
            j += 1
        if not isThere:
            return False
    return True
    
def MinMIS(Ck, MIS):
    minMIS = math.inf
    #print(minMIS)
    for i in Ck:
        for j in i:
            if MIS[j] < minMIS:
                minMIS = MIS[j]
    #print(minMIS)
    return minMIS

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
def level_2(L, MIS, n, sdc):
	C2 = []
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
	#F[2] = [[[20, 30]], [[20], [30]], [[20, 70]], [[20], [70]], [[20], [80]], [[30], [30]], [[30, 70]], [[30], [70]], [[30, 80]], [[30], [80]], [[70], [70]], [[70, 80]], [[80], [70]], [[10, 40]], [[10], [40]], [[40], [40]]]
	# F[2] = [[[20, 30, 40]], [[40], [70]]]
	#print(F)
	C = []
	for i in F:
	    for j in F:
	        s1 = i
	        s2 = j
	        first_s1 = getFirstItem(s1)
	        last_s1 =  getLastItem(s1)
	        first_s2 = getFirstItem(s2)
	        last_s2 =  getLastItem(s2)
	        MIS_least_seq = getMISofSequence(s1,MIS,first_s1)
	        #print(s1)
	        #print(s2)

	        if( MIS[first_s1] < MIS_least_seq ):
	            if( (removeItem(s1,1) == removeItem(s2,Length(s2)-1)) & (MIS[last_s2] > MIS[first_s1]) ):
	                if(Size(LastElement(s2)) == 1):
	                    c1 = []
	                    c1 = s1.copy()
	                    c1.append([getLastItem(s2)])
	                    C.append(c1)

	                    if( (Length(s1) == 2 & Size(s1) == 2) & (MIS[last_s2] > MIS[last_s1]) ):
	                        c2 = []
	                        c2 = s1.copy()
	                        last_c2 = LastElement(c2).copy()
	                        last_c2.append(getLastItem(s2))
	                        # c2 = removeItem(c2,Length(c2)-1)
	                        del(c2[-1])
	                        c2.append(last_c2)
	                        C.append(c2)
	                        
	                elif( ((Length(s1) == 2 & Size(s1) == 1) & (MIS[last_s2] > MIS[last_s1])) | ( Length(s1) > 2 ) ):
	                    c2 = []
	                    c2 = s1.copy()
	                    #last_item_s2 = getLastItem(s2)
	                    last_c2 = LastElement(c2).copy()
	                    last_c2.append(getLastItem(s2))
	                    # c2 = removeItem(c2,Length(c2)-1)
	                    del(c2[-1])
	                    c2.append(last_c2)
	                    C.append(c2)

	        elif( MIS[last_s2] <  getMISofSequence(s2,MIS,last_s2) ):
	            if( (removeItem(s2,1) == removeItem(s1,Length(s1)-1)) & (MIS[first_s1] > MIS[last_s2]) ):
	                if(Size(FirstElement(s1)) == 1):
	                    c1 = []
	                    c1 = s2.copy()
	                    c1.append([getFirstItem(s1)])
	                    C.append(c1)

	                    if( (Length(s2) == 2 & Size(s2) == 2) & (MIS[first_s1] > MIS[first_s2]) ):
	                        c2 = []
	                        c2 = s2.copy()
	                        last_c2 = FirstElement(c2).copy()
	                        last_c2.append(getFirstItem(s1))
	                        # c2 = removeItem(c2,0)
	                        del(c2[0])
	                        c2.append(last_c2)
	                        C.append(c2)
	                elif( ((Length(s2) == 2 & Size(s2) == 1) & (MIS[first_s1] > MIS[first_s2])) | ( Length(s2) > 2 ) ):
	                    c2 = []
	                    c2 = s2.copy()
	                    #last_item_s1 = getFirstItem(s1)
	                    last_c2 = FirstElement(c2).copy()
	                    last_c2.append(getFirstItem(s1))
	                    # c2 = removeItem(c2,0)
	                    del(c2[0])
	                    c2.append(last_c2)
	                    C.append(c2)

	        else:
	            if(removeItem(s1,0) == removeItem(s2,Length(s2)-1)):
	                if(Size(LastElement(s2)) == 1):
	                    c1 = []
	                    c1 = s1.copy()
	                    c1.append([getLastItem(s2)])
	                    C.append(c1)
					
	                else:
	                    c1 = []
	                    c1 = s1.copy()
	                    #last_item_s2 = getLastItem(s2)
	                    last_c1 = LastElement(c1).copy()
	                    last_c1.append(getLastItem(s2))
	                    # c1 = removeItem(c1,Length(c1)-1)
	                    del(c1[-1])
	                    c1.append(last_c1)
	                    C.append(c1)


	prune_c = PruneC(C,F,MIS)
	return prune_c


def PruneC(Can_Seq,F,M):
    count = 0;
    final_Can_Seq = []
    for Can_Seq_Item in Can_Seq:
        count = 0
        temp_Can_Seq = deepcopy(Can_Seq_Item)
        temp_list = []
        for Can_Seq_Si,Can_Seq_Item_Seq in enumerate(Can_Seq_Item):
            min_MS_Can_Seq_Item = ''
            min_MS_Can_Seq_Item = Can_Seq_Item_Seq[0]
            for e_item in Can_Seq_Item_Seq:
                if(M[e_item] < M[min_MS_Can_Seq_Item]):
                    min_MS_Can_Seq_Item = e_item
            for Can_Seq_Ii,Can_Seq_Item_item in enumerate(Can_Seq_Item_Seq):
                temp_Can_Seq = deepcopy(Can_Seq_Item)
                if(temp_Can_Seq[Can_Seq_Si][Can_Seq_Ii] != min_MS_Can_Seq_Item):
                    del temp_Can_Seq[Can_Seq_Si][Can_Seq_Ii]
                    temp_Can_Seq = list(filter(None, temp_Can_Seq))
                    temp_list.append(temp_Can_Seq)
        temp = 0
        for each_temp_list in temp_list:
            if(not any(each_temp_list == each_items for each_items in F)):
                temp += 1
        if(temp == 0):
            final_Can_Seq.append(Can_Seq_Item)
    return final_Can_Seq

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


def getMISofSequence(s,MIS,item):
	temp = []
	MIS_array = []
	for i in s:
		for j in range(len(i)):
			temp.append(i[j])

	temp.remove(item)		
			
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