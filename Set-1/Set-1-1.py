
#A-Z=0-25,a-z=26-51,0-9=52-61,+,/
#implement your own base64 library

b64Matrix= ["+","/"]
givenHexString="49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
#expected ouput
exp="SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
def hextoAscii(hexStr):
	ans=""
	i=0
	while i<len(hexStr):
		gg=int(hexStr[i:i+2],16)
		ans=ans+chr(gg)
		i=i+2
	return ans

def hextTobase64(str1):
	#Convert the entire ascii string to binary
	asciistr=hextoAscii(givenHexString)
	y=''.join(format(ord(x), '08b') for x in asciistr)
	#divide the binary string into sextets
	#print(y)
	i=0
	fetch=0
	gp=len(y)%6
	ans=""
	for i in range(gp):
		y=y+"0"
	while i< len(y):
		g=y[i:i+6]
		#print(g)
		asci=int(g,2)
		#fetch value from the matrix
		if asci <=25:
			fetch=chr(asci+65)
		elif asci <=51:
			fetch=chr(97+asci-26)
		elif asci <=61:
			fetch = chr(48+asci-52)
		elif asci<=63:
			fetch = b64Matrix[asci-62]
		else:
			print("MISCALCULATION")
		ans=ans+fetch
		i=i+6
	#final 6 bits and padding
	if gp==2:
		ans=ans+"=="
	elif gp==4:
		ans=ans+"="
	return ans


def main():
	#validating output
	print("Solution is ",hextTobase64(givenHexString)==exp)
if __name__=="__main__":
	main()