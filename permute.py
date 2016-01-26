#!/usr/bin/python

#returns a list of all permutations of mystr
def perm(mystr):
	if len(mystr) == 1: return mystr
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
			output.add(currstr)
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
	spaces.insert(0, 0)
	spaces.append(len(clue)+1)
	if len(mydict) == 0: readDict()
	myperms = perm(clue.lower())
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
			print toprint

# solve('agtdrkaoone', [4,5])
