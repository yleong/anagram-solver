#!/usr/bin/python
DEBUG=False

def solve(clue, lengths):
	WORK_FACTOR=2 #memory-efficient solver is about twice as slow..
	print 'pattern: ', clue, ' estimated running time: ', prettyPrintDuration(WORK_FACTOR*estimateRuntime(clue))
	answers=set()
	lengths.insert(0, 0)
	lengths.append(len(clue)+1)
	if len(mydict) == 0: readDict()
	permIterate('', clue, lengths, answers)
	for ans in answers:
		print ans
#instead of generating the entire list of permutations, generate them
#singly one at a time so that we don't need o(n!) space complexity
#but how can we do that? 
#basically we will do a DFS on a tree
#the tree's root node is the empty string
#the tree's leaf nodes are all the permutations
#the edges connect a "next" word to a previous word, where
#the next has 1 letter more than the previous
# ********************************************************************
# POSSIBLE OPTIMIZATION: we can prune the search tree to get rid of 
# entire subtrees that would not work, e.g. the subtree with path of 
# "qzzta..." will never result in any match because no word in english
# starts with qzzta or even qz for that matter.
def permIterate(wordSoFar, lettersRemaining, wordLengths, answers):
	if len(lettersRemaining) == 0: 
		checkWord(wordSoFar, wordLengths, answers)
		#we have reached the leaf node
		#check if wordSoFar is a word and if so add it to answers
	else:
		#proceed to next branch until you reach the leaf
		#need to use set() to prevent repeated paths
		for letter in set(lettersRemaining):
			#need to use list() to restore the repetitions. it would be incorrect otherwise to omit them!
			newLettersRemaining = list(lettersRemaining)	
			newLettersRemaining.remove(letter)
			permIterate(wordSoFar+letter, newLettersRemaining, wordLengths, answers)

#determines if a number is a leading zero in the year/day/hour/minute/seconds format
def isLZ(currnum, prevAllLZ, isLastNum):
	#we shall call numYears, numDays, numHours, numMinutes, secs as numbers
	#a number is a leading zero (LZ) if
	#the number is a zero && 
	#the previous numbers were all leading zeros &&
	#it is not the last number (i.e. secs)

	return currnum == 0 and prevAllLZ and not isLastNum

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
def solveOld(clue, spaces):
	print 'pattern: ', clue, ' estimated running time: ', prettyPrintDuration(estimateRuntime(clue))
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

#given a string and a lost of the cumulative word lengths (except last word's length)
#check if it is concatenation of valid english words
#e.g. applebee, [5] should return yes
#or johnkilledtom, [4, 10] should return yes
def checkWord(phrase, spaces, answers):
	matches = 0
	toprint = []
	lmydict = mydict
	for i in range(len(spaces)-1):
		currCandidate = phrase[spaces[i]:(spaces[i+1])]
		if currCandidate in lmydict:
			matches = matches + 1
			toprint.append(currCandidate)
		else:
			return #first word already failed, so don't bother
	if matches == len(spaces)-1:
		import string
		answers.add(string.joinfields(toprint, ' '))

#given a word prefix, e.g. "th", check if there exists
#any word in English that begins with the prefix. In this case
#the answer is True because of words like "there", "the" etc.
#this is a helper function designed to help us prune away subtrees
#that leads to leaves that are not English words, e.g. "qz..." trees
#will obviously not work so we don't waste time DFS-ing it to the end
def checkWordPrefix(prefix):

#given a duration in seconds, return a nice string representation
#e.g. xx seconds, or yy minutes xx seconds, or zz hours yy minutes xx seconds
#given the factorial nature of the time complexity, we shall support up to years
#for simplicity, we do not account for leap year/seconds
def prettyPrintDuration(secs):
	subSeconds = secs - int(secs)
	secs = int(secs)
	SECSINMINUTE = 60
	SECSINHOUR = SECSINMINUTE * 60
	SECSINDAY = SECSINHOUR * 24
	SECSINYEAR = SECSINDAY * 365

	numYears = secs / SECSINYEAR
	secs = secs % SECSINYEAR
	numDays = secs / SECSINDAY
	secs = secs % SECSINDAY
	numHours = secs / SECSINHOUR
	secs = secs % SECSINHOUR
	numMinutes = secs / SECSINMINUTE
	secs = secs % SECSINMINUTE
	if subSeconds > 0.00000001: secs = secs + subSeconds

	#we want to express the duration as years, days, hours, minutes, seconds
	#but we want to skip zero values
	#0 years 0 days 0 hours 25 minutes 3 seconds
	#should simply be 25 minutes 3 seconds without the leading 0 years 0 days 0 hours
	timestr = ""
	nums = [numYears, numDays, numHours, numMinutes, secs]
	labels = [" years ", " days ", " hours ", " minutes ", " seconds "]

	for i in range(0, len(nums)):
		currnum = nums[i]
		currlabel = labels[i]
		if currnum != 0: timestr = timestr + str(currnum) + currlabel

	return timestr

def test():
	solve("agtdrkaoone", [4, 5]) 
	solve('pieceachance', [5,6])
	solve('loadsoffun', [5,7])
	solve('camellot', [5])

def testOld():
	solveOld("agtdrkaoone", [4, 5]) 
	solveOld('pieceachance', [5,6])
	solveOld('loadsoffun', [5,7])
	solveOld('camellot', [5])
# prob = 'atofererrigr'
# permIterate('', prob)
# test()

# solve('tiomuishrfed', [6,9])
