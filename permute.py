#!/usr/bin/python
DEBUG=False

#estimates the number of operations = n! / r! q! for each r and q that has repetition
def estimateRuntime(mystr):
	n = len(mystr)
	numops = fact(n)
	mystrsorted = sorted(mystr)

	prevchar = mystrsorted[0]
	count = 1
	for i in range(1, n):
		mychar = mystrsorted[i]
		if prevchar == mychar:
			count = count + 1
		else:
			numops = numops / fact(count)
			count = 1
		prevchar = mychar
	numops = numops / fact(count)
	# 350k ops per sec  for high number of ops
	speed_highops = 350000.0
	# 110k ops per sec  for small number of ops
	speed_lowops = 110000.0
	# 200k ops and below are considered small number of ops
	lowops_threshold = 200000

	time = 0
	if numops < lowops_threshold:
		time = numops / 110000.0
	else:
		time = numops / 350000.0
	return time

def fact(n):
	if n == 1: return 1
	else: return (n * fact(n-1))

#returns a list of all permutations of mystr
def perm(mystr):
	if DEBUG: print 'permuting: ', mystr
	if len(mystr) == 1: return set(mystr)
	if DEBUG: print 'combining: ', mystr[0], ' with permutation of ', mystr[1:]
	return combine(mystr[0], perm(mystr[1:]))

#given a char and a list of strs, put char into each slot
#of each str, and return each as a new str in a list
#where a slot is defined as the gap between 2 characters 
#or a gap between a word ending and a character
def combine(mychar, mystrArr):
	output = set() 
	for mystr in mystrArr:
		for i in range(len(mystr)+1):
			currstr = mystr[:i] + mychar + mystr[i:]
			try:
				output.add(currstr)
			except Exception as e:
				print type(e)
				print e.args
				print e
				for arg in e.args:
					print arg
				print 'error, currstr is ', currstr
				print 'size of output is ', len(output)
				import sys
				sys.exit()
	return output

mydict=set()
#builds the dictionary to filter permutations for legitimate words
def readDict():
	dictfile = open('mydict', 'r')
	for word in dictfile:
		mydict.add(word.strip().lower())

#given a permuted word/clue, solve for the original word
def solveOne(clue):
	if len(mydict) == 0: readDict()
	myperms = perm(clue.lower())
	for candidate in myperms:
		if candidate in mydict:
			print candidate

#given a permutation of a concatenanted phrase of words and the indices of the
#compenent words' boundaries, solve for the original phrase
#e.g. if the solution is "took a gander" then we can call 
# solve("agtdrkaoone", [4, 5]) 
def solve(clue, spaces):
	print 'estimated running time: ', estimateRuntime(clue) ,' seconds'
	spaces.insert(0, 0)
	spaces.append(len(clue)+1)
	if len(mydict) == 0: readDict()
	myperms = perm(clue.lower())
	answers = set()
	for candidate in myperms:
		matches = 0
		for i in range(len(spaces)-1):
			currCandidate = candidate[spaces[i]:(spaces[i+1])]
			if currCandidate in mydict:
				matches = matches + 1
		if matches == len(spaces)-1:
			toprint = ""
			for i in range(len(spaces)-1):
				currCandidate = candidate[spaces[i]:(spaces[i+1])]
				toprint = toprint + currCandidate + ' '
			#print toprint
			answers.add(toprint)

	for myans in sorted(answers):
		print myans

solve("agtdrkaoone", [4, 5]) 
solve('pieceachance', [5,6])
solve('loadsoffun', [5,7])
solve('camellot', [5])
