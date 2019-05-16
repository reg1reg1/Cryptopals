cipher = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

pt=""
def EnglishScore(string):
	score=0
	#This matrix has been taken from online sources, it has letter frequency in English language
	
	wStatic = {
			'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339,
			'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881,
			'g': 0.0158610, 'h': 0.0492888, 'i': 0.0558094,
			'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490,
			'm': 0.0202124, 'n': 0.0564513, 'o': 0.0596302,
			'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563,
			's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,
			'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692,
			'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}
	totfreq= len(string)
	freqSt={}
	
	for i in range(len(string)):
		#Penalizing score if char not in alphabet
		if string[i] not in wStatic:
			score=score+0.05
		else:
			if string[i].lower() not in freqSt:
				freqSt[string[i].lower()]=1
			else:
				freqSt[string[i].lower()]+=1

	for key,value in freqSt.items():
		value/totfreq
	#score calculation
	for key,value in wStatic.items():
		if key in freqSt:
			score+=wStatic[key]-freqSt[key]
	return score



def hextoAscii(hexStr):
	ans=""
	i=0
	while i<len(hexStr):
		gg=int(hexStr[i:i+2],16)
		ans=ans+chr(gg)
		i=i+2
	return ans

def xorBrute(str1):
	ascistr=hextoAscii(str1)
	#print(ascistr)
	ascilen=len(ascistr)
	p=""
	z=0
	minscore=99999
	guessKey=""
	while z<=255:
		p=""
		for i in range(ascilen):
			p=p+str(chr(ord(ascistr[i])^(z)))
		score=EnglishScore(p)
		if score < minscore:
			minscore=score
			guessKey=chr(z)
			guessPT=p
		#print(p)
		z=z+1
	return (guessPT,guessKey)

def main():
	print(xorBrute(cipher))

if __name__=="__main__":
	main()