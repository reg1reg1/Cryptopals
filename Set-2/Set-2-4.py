import os
import sys
import binascii
from Crypto.Cipher import AES
import base64

#Globals
constantString= b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg' \
				b'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq' \
				b'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg' \
				b'YnkK'
constKey="YELLOW SUBMARINE"
#BlockSize has to be equal to the key size, or else you will have to pad the key
blocksize=16
def detectOracle():
	#Chosen plaintext adversary
	plaintext= b"\x00"*100
	#Validation is stored and verified with the answer
	ciphertext = EncryptionOracle(plaintext)
	answer=0
	for blocks in [ciphertext[i:i+16] for i in range(len(ciphertext) - 16)]:
		if ciphertext.count(blocks) > 1:
			answer=1
			break
	
	if answer==1:
		print("Predicted Encryption was ECB")
	else:
		print("Predicted Encryption was CBC")


def guessBlockLength():
	plaintext=b""
	ciphertext= EncryptionOracle(plaintext)
	init = len(ciphertext)
	curr = init
	count =0
	while curr==init:
		plaintext+=b"A"
		ciphertext = EncryptionOracle(plaintext)
		curr =len(ciphertext)
	return curr-init

def padPKS7(inp,block_size):
	padding = block_size - len(inp) % block_size
	pkcs7 = b"\x04"
	for i in range(padding):
		inp+=pkcs7
	return inp

def AES_ENCRYPT_BLOCK(enc,key):
	aes = AES.new(key.encode("utf-8"), AES.MODE_ECB)
	return aes.encrypt(enc)


def EncryptionOracle(plaintext):
	global constKey
	global blocksize
	consistentSecret = base64.b64decode(constantString.decode())
	paddedPT = padPKS7(plaintext + consistentSecret, blocksize)
	cipher= AES_ENCRYPT_BLOCK(paddedPT,constKey)
	return cipher

'''
# Feed the oracle between 0 and (block_size - 1) known bytes, 
placing the next byte to be decrypted in the last
# position of its block
# Try encrypting block using all possible values of last byte, store results in dictionary
'''
def guessSecretByte(block_size,secret):
	length = (block_size - (1 + len(secret))) % block_size
	prefix = b'A' * length

	#cracklen will increase with the no of bytes being cracked
	#cracklen = length + len(secret) + 1
	#targetCipher = EncryptionOracle(prefix)
	#print("Target Cipher ",targetCipher)
	# For each possible character
	#print(prefix+b"::"+secret,cracklen,len(targetCipher))
	for i in range(256):
		#print(prefix+secret+bytes([i]))
		forgedCipher = EncryptionOracle(prefix + secret+bytes([i]))
		if forgedCipher[:cracklen] == targetCipher[:cracklen]:
			return bytes([i])
	return b""

def guessSecret():
	detectOracle()


	length=guessBlockLength()
	empty=b""
	
	emptycipher=EncryptionOracle(empty)
	ciphlen=len(emptycipher)
	secret = b''
	print("Length of prefix detected as {} bytes".format(ciphlen))


	for i in range(ciphlen):
		secret += guessSecretByte(length,secret)
	# Return the complete padding as bytes
	return secret


def main():
	print(guessSecret())

if __name__ == '__main__':
	main()