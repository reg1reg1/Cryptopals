import base64
import binascii
import collections

#Global filename
FILE_NAME="8.txt"

def detectAESECB():
	c1=0
	c2=0
	with open(FILE_NAME,"r",encoding="utf-8") as input_file:
		enc = [binascii.unhexlify(line.strip()) for line in input_file.readlines()]
	for item in enc:
		blocks = [item[start:start+16] for start in range(0, len(item), 16)]
		c1+=1
		c2=0
		for block in blocks:
			c2+=1
			if blocks.count(block) > 1:
				print("Same block in Ciphertext")
				print("ECB mode detected in CipherText {} and Block number {}".format(c1,c2))
				return item
def main():
	detectAESECB()
if __name__=="__main__":
	main()