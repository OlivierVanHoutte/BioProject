
# mapping voor bitwise conversion
mappings = {}
mappings['00'] = 'A'
mappings['01'] = 'T'
mappings['10'] = 'C'
mappings['11'] = 'G'

# bitwise conversion
def string_to_DNA_Bitwise(str):
	result = ''
	for i in str:
		bits = bin(ord(i))[2:]
		bits = '00000000'[len(bits):] + bits
		print(i, '->', bits)
		for k in range(int(len(bits)/2)):
			DNA_Char = mappings[bits[2*k] + bits[2*k+1]]
			print(bits[2*k] + bits[2*k+1], '->', DNA_Char)
			result += DNA_Char
	return result

# mogenlijke Stuff in geval van 1 DNA character per real character (15 opties)
mix = {}
mix['A'] = [['A']]
mix['B'] = [['A', 'T']]
mix['C'] = [['C']]
mix['D'] = [['A', 'C']]
mix['E'] = [['A', 'T', 'C']]
mix['F'] = [['A', 'C', 'G']]
mix['G'] = [['G']]
mix['H'] = [['A', 'G']]
mix['I'] = [['A', 'T', 'G']]
mix['J'] = [['C', 'G']]
mix['K'] = [['T', 'C']]
mix['L'] = [['T', 'C', 'G']]
mix['M'] = [['T', 'G']]
mix['N'] = [['A', 'T', 'C', 'G']]
mix['O'] = ['#']
mix['P'] = ['#']
mix['Q'] = ['#']
mix['R'] = ['#']
mix['S'] = ['#']
mix['T'] = [['T']]
mix['U'] = ['#']
mix['V'] = ['#']
mix['W'] = ['#']
mix['X'] = ['#']
mix['Y'] = ['#']
mix['Z'] = ['#']
mix[' '] = ['#']

# Old
def _genMix(left, count, mixchar):
	DNA_char_r = {'A', 'C', 'T', 'G'}
	while (len(DNA_char_r)  > 0 ):
		r = DNA_char_r.pop()
		DNA_char_r.add(r)
		cright = [r]
		for j in DNA_char_r.copy():
			if j not in cright:
				cright.append(j)
			t = left.copy()
			t.append(cright.copy())
			if count == 0:
				mix[next(mixchar)] = t
			else:
				_genMix(t ,count-1, mixchar)
		DNA_char_r.remove(r)

# New (and improved?)
def _genMix2(mixchar, count = 1, l = []):

	import itertools
	x = ['A', 'C', 'T', 'G']
	for i1 in range(len(x)):
		for c1 in [c1 for c1 in itertools.combinations(x, i1+1)]:
			l1 = list(c1), [i1 for i1 in x if not i1 in c1]
			l2 = l.copy()
			l2.append(l1[0])
			if count == 0:
				mix[next(mixchar)] = l2
			else:
				_genMix2(mixchar, count-1, l2)
		
def genMix(count):	
	mixchar = iter(mix.keys())
	try:
		_genMix2(mixchar, count-1)
	except Exception as e:
		print('-- 2 per character --', e)
	for i in mix:
		print(i, mix[i])

# Generate a list of DNA strings fitting the given string
def genDNAStrings(_str, _amount):
	results = []
	while _amount > 0:
		results.append(genDNAString(_str))
		_amount -= 1
	return results

# Generate a DNA string fitting the given string 
def genDNAString(_str):
	import random
	result = ''
	for i in _str.upper():
		for l in mix[i]:
			index = random.randint(0, len(l)-1)
			result += l[index]
	return result

# Convert DNA codons to possible characters
def getPossibleInput(koppels):
	import math
	total_score = -math.inf
	choice = '#'
	for i in mix:
		found = True
		score = 0
		for c in mix[i][0]:
			cFound = False
			for koppel in koppels:
				if koppel[0] not in mix[i][0]:
					found = False
					break	
				if c == koppel[0]:
					cFound = True
			if not cFound:
				score -= 1
			if not found:
				break
			
		if len(koppels[0]) == 2:
			for c in mix[i][1]:
				cFound = False
				for koppel in koppels:
					if koppel[1] not in mix[i][1]:
						found = False
						break	
					if c == koppel[1]:
						cFound = True
				if not cFound:
					score -= 1
				if not found:
					break
		
		if found:
			if score > total_score:
				choice = i
				total_score = score
	return choice		

if __name__ == "__main__":
	print(string_to_DNA_Bitwise("Hallo ik ben Olivier")) #TAATTAACTAAGTATATATTTATCTATGTACATACTTACCTACGTAGATAGTTAGCTAGGTTAATTTA
	koppelSize = 2
	genMix(koppelSize)
	res = genDNAStrings("Hallo ik ben Olivier", 80)
	print(res)
	result = ''
	i = 0
	while i < len(res[0]):
		koppels = []
		for j in res:
			s = ''
			for k in range(koppelSize):
				s += j[i+k]
			koppels.append(s)
		result += getPossibleInput(koppels)
		i += 1 + k

	print(result)



