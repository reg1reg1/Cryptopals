from Crypto.Cipher import AES
from base64 import b64decode

#GLOBAL
FILE_NAME="7.txt"
BLOCKSIZE=128
KEY="YELLOW SUBMARINE"

def extractCipher():
	with open(FILE_NAME) as input_file:
		cipherFile = b64decode(input_file.read())
	return cipherFile





def AESDECRYPT(enc,key):
    aes = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    return aes.decrypt(enc)




def main():
	with open("output-aes-7.txt","w") as write_file:
		write_file.write(AESDECRYPT(extractCipher(),KEY).decode("utf-8"))
if __name__=="__main__":
	main()