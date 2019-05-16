#Repeating key XOR
#Key to be used 

plaintext = "Burning 'em, if you ain't quick and nimble \n I go crazy when I hear a cymbal"
key= "ICE"

def encryptSimple(pt,key):
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

#XOR encryption and decryption function are indentical
def decryptSimple(ct,key):
	return encryptSimple(ct,key)

def main():
	#Proof of concept Comparing the decrypted value of encrypted to original
	#Should print true if correct
	print(decryptSimple(encryptSimple(plaintext,key),key)==plaintext)
if __name__=="__main__":
	main()