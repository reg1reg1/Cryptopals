#Runs on python2


import base64
import binascii
from Crypto.Cipher import AES
#Globals
IV=b"\x00"
FILE_NAME="10.txt"
KEY="YELLOW SUBMARINE" 
#has to be of the block size
OUT_FILE="output-aes-cbc-encrypt.txt"
#Implement CBC mode AES
#blocksize in bytes

x=0
#byte-wise XOR
def XOR_Block(bytes1,bytes2):
    assert len(bytes1) == len(bytes2), "SIZE ERROR"
    return bytes().join([bytes([a ^ b]) for a, b in zip(bytes1, bytes2)])

def AES_ENCRYPT_BLOCK(enc,key):
	aes = AES.new(key.encode("utf-8"), AES.MODE_ECB)
	return aes.encrypt(enc)

def AES_DECRYPT_BLOCK(dec,key):
	aes = AES.new(key.encode("utf-8"), AES.MODE_ECB)
	return aes.decrypt(dec)

def padPKS7(inp,block_size):
	padding = block_size - len(inp) % block_size
	pkcs7 = b"\x04"
	for i in range(padding):
		inp+=pkcs7
	return inp


def CBC_AES_ENCRYPT(blockSize=16):
	global IV
	with open(FILE_NAME,"r") as input_file:
		plainText = base64.b64decode(input_file.read())

	#pad the plaintext, we will use pkcs7 padding
	plainText= padPKS7(plainText,blockSize)
	#break the plaintext into blocks
	blocks = [plainText[start:start+blockSize] for start in range(0, len(plainText), blockSize)]
	ctBytes=b""
	ivblock=b"\x00"*blockSize
	assert len(KEY) == len(ivblock), "Key and IV not same size"
	for block in blocks:
		cblock=AES_ENCRYPT_BLOCK(XOR_Block(block,ivblock),KEY)
		ctBytes+=cblock
		ivblock=cblock
	return ctBytes

def CBC_AES_DECRYPT(blockSize=16):
	global IV
	with open(FILE_NAME,"r") as input_file:
		cipherText = base64.b64decode(input_file.read())
	blocks = [cipherText[start:start+blockSize] for start in range(0, len(cipherText), blockSize)]
	pBytes=b""
	ivblock=b"\x00"*blockSize
	assert len(KEY) == len(ivblock), "Key and IV not same size"
	for block in blocks:
		pBytes+=XOR_Block(ivblock,AES_DECRYPT_BLOCK(block,KEY))
		ivblock=block
	with open(OUT_FILE,"w") as outFile:
		outFile.write(pBytes.decode("utf-8"))
	print("Output written to {}".format(OUT_FILE))

def main():
	CBC_AES_DECRYPT()
if __name__ == '__main__':
	main()