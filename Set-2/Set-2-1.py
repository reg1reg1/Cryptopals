import binascii




#Globals

def padPKCS7(inp,block_size=16):
	#print("Received input is ",type(inp))
	#print(type(inp.encode("utf-8")))
	str1 = bytes(inp.encode('utf-8'))
	#print("Byte array ",type(str1))
	padding = block_size - len(str1) % block_size
	pkcs7 = b"\x04"
	for i in range(padding):
		str1+=pkcs7
	return str1.decode("utf-8")
def main():
	print(padPKCS7("YELLOW SUBMARINE",20))
if __name__=="__main__":
	main()