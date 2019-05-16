inp1="1c0111001f010100061a024b53535009181c"
inp2="686974207468652062756c6c277320657965"

check="746865206b696420646f6e277420706c6179"



def xorInput(inp1,inp2):
	hxlen=len(inp1)
	dec=int(inp1,16)^int(inp2,16)
	return hex(dec).split('x')[-1]


def main():
	#validating output
	print("Solution is ",xorInput(inp1,inp2)==check)
if __name__=="__main__":
	main()