#Base64 after encrypting with a repeating key XOR
#Cracking the vignere cipher based on the hamming distance property
from base64 import b64decode

#Global Literals
FILE_NAME="6.txt"



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


def HammingDistance(str1,str2):
	#print(str1)
	#print(str2)
	bstr1 = ''.join(format(ord(x),'08b') for x in str1)
	bstr2 = ''.join(format(ord(x),'08b') for x in str2)
	count=0
	for i in range(len(bstr1)):
		if bstr1[i]!=bstr2[i]:
			count+=1
	return count

def extractCipher():
	with open(FILE_NAME) as input_file:
		cipherFile = b64decode(input_file.read()).decode("utf-8")
	return cipherFile

def keySizeGuess(cipher):
	min=0
	probKey=[]
	for i in range(2,41):
		hdist1=HammingDistance(cipher[:i],cipher[i:2*i])
		hdist2=HammingDistance(cipher[i:2*i],cipher[2*i:3*i])
		hdist3=HammingDistance(cipher[2*i:3*i],cipher[3*i:4*i])
		hdist4=HammingDistance(cipher[3*i:4*i],cipher[4*i:5*i])
		hdistNorm=(hdist1+hdist2+hdist3+hdist4)/(4*i)
		probKey.append((i,hdistNorm))
	probKey=sorted(probKey,key=lambda x : x[1])
	#Top 2-3 probable keys
	return probKey[:3]

def xorBrute(string):
	p=""
	z=0
	minscore=99999
	guessKey=""
	while z<=255:
		p=""
		for i in range(len(string)):
			p=p+str(chr(ord(string[i])^(z)))
		score=EnglishScore(p)
		if score < minscore:
			minscore=score
			guessKey=chr(z)
			guessPT=p
		#print(p)
		z=z+1
	return (guessPT,guessKey)


def crackVignere():
	cipher=extractCipher()
	keySizes=keySizeGuess(cipher)
	candidatePT=[]
	candidateKey=[]
	#print(keySizes)
	
	plainText=""
	#iterting thorugh all the keysizes
	for i in keySizes:
		key=i[0]
		transCipher=[]
		
		#Must be run for every key,dividing CT based on key
		for i in range(key):
			#Transpose the ciphertext
			ciphColumn=''
			ciphColumn=''.join(cipher[k] for k in range(len(cipher)) if (k-i)%key==0)
			transCipher.append(ciphColumn)
		#Brute force each individual column (Will be encrypted with the same character)
		keyG=""
		plainText=""
		#Guessing the key
		for string in transCipher:
			ans=xorBrute(string)
			plainText+=ans[0]
			keyG+=ans[1]
		#To avoid the hassle of rerranging plaintext, we might as well xor the key to ciphertext
		candidateKey.append(keyG)
		candidatePT.append(decryptSimple(cipher,keyG))
	minscore=99999
	index=0	

	for i in range(len(candidatePT)):
		score=EnglishScore(candidatePT[i])
		if score < minscore:
			minscore=score
			index=i
	with open("output.txt","w+") as input_file:
		input_file.write("Key Guess : {} \n".format(candidateKey[index]))
		input_file.write("PlainText Guess------------------------------\n")
		input_file.write(candidatePT[index])
		input_file.close()
	print("Output stored in output.txt")

	


def decryptSimple(pt,key):
	ptlen= len(pt)
	fkey=""
	qot= int(ptlen/len(key))
	rem = ptlen%len(key)
	for i in range(qot):
		fkey+=key
	#final padding blocks
	fkey+=key[:rem]
	if len(fkey)!=ptlen:
		print("Error in keylength")
	#XOR time
	cipher=""
	for i in range(ptlen):
		cipher+=str(chr(ord(pt[i])^ord(fkey[i])))
	return cipher	

	#crackCipher



def main():
	crackVignere()
if __name__=="__main__":
	main()