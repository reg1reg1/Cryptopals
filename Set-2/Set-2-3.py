#Encryption mode detector

import binascii
import base64
from Crypto.Cipher import AES
import os
import random

def XOR_Block(bytes1,bytes2):
	assert len(bytes1) == len(bytes2), "SIZE ERROR"
	return bytes().join([bytes([a ^ b]) for a, b in zip(bytes1, bytes2)])


def AES_ENCRYPT_BLOCK(enc,key):
	aes = AES.new(key, AES.MODE_ECB)
	return aes.encrypt(enc)

def CBC_AES_ENCRYPT(plaintext,key,blockSize=16):
	#plaintext supplied is already padded
	#break the plaintext into blocks
	blocks = [plaintext[start:start+blockSize] for start in range(0, len(plaintext), blockSize)]
	ctBytes=b""
	ivblock=os.urandom(16)
	assert len(key) == len(ivblock), "Key and IV not same size"
	for block in blocks:
		cblock=AES_ENCRYPT_BLOCK(XOR_Block(block,ivblock),key)
		ctBytes+=cblock
		ivblock=cblock
	return ctBytes

def padRandom(inp,block_size):
	padding = block_size - len(inp) % block_size
	pad = os.urandom(padding)
	inp+=pad
	return inp



def RandomOracle(plaintext):
	#generate random key
	count=random.randrange(5,11)
	pre=os.urandom(count)
	count=random.randrange(5,11)
	post=os.urandom(count)
	flip=random.randrange(0,2)
	Key=os.urandom(16) #16 bytes of key
	plaintext=pre+plaintext+post
	
	plaintext= padRandom(plaintext,16)
	#print("Plaintext:",plaintext)

	if flip:
		aes = AES.new(Key, AES.MODE_ECB)
		return (aes.encrypt(plaintext),flip)
	else:
		return (CBC_AES_ENCRYPT(plaintext,Key),flip)

def detectOracle():
	#Chosen plaintext adversary
	plaintext= b"\x00"*100
	#Validation is stored and verified with the answer
	ciphertext,validation = RandomOracle(plaintext)
	answer=0

	for blocks in [ciphertext[i:i+16] for i in range(len(ciphertext) - 16)]:
		if ciphertext.count(blocks) > 1:
			#print("BLOCKS:",blocks)
			answer=1
			break
	#print("Validation is",validation)
	if validation==1:
		print("Encryption was ECB")
	else:
		print("Encryption was CBC")

	#
	if answer==1:
		print("Predicted Encryption was ECB")
	else:
		print("Predicted Encryption was CBC")



def main():
	#flip 0 ECB, flip 1 CBC
	detectOracle()
	#Predict flip based on ciphertext analysis


if __name__ == '__main__':
	main()