from PIL import Image
import sys, getopt

def main(argv):

	screenTFileF = True #optional parameter, so if it's missing then display the text on the screen.
	outputFile = ""
	subtract = 1

	try: #no dashes = arguments
		opts, args = getopt.getopt(argv,"ho", ["help"])
	except getopt.GetoptError as err: #nandle errors
		print(str(err))
		sys.exit(2)
	for opt, arg in opts:
		if opt == '--help': #print usage and exit
			print("Usage: python3 stega.py -o <output file> <input file>\n-o <output file> is optional, prints the output in the file specified instead of the command line.\n<input file> is required, specifies the file that contains the picture.")
			sys.exit(0)
		elif opt == "-o":
			outputFile = args[0]
			subtract = 0
			file = open(outputFile, "w+") #create new file
			screenTFileF = False
	inputFile = args[len(args)-1-subtract] #input file will be in a different index depending on whether the user wants to print to an output file

	try:
		image = Image.open(inputFile)
	except IOError:
		print("Unable to load image")
		sys.exit(1)
	

	rgb_im = image.convert('RGB')
	byte = 0
	lenByte = 0
	arrBytes = []
	last3Bytes = [] #contains the last 3 bytes entered to check if I should stop
	breakThis = False #break does not break out of all loops
	for y in range(image.size[1]): #go through image pixels
		for x in range(image.size[0]):
			arrPixel = rgb_im.getpixel((x, y)) #[r,g,b,a]
			for i in range(3): #[r,g,b]
				if lenByte == 8: #if it is a byte.
					last3Bytes.append(byte)
					if len(last3Bytes) > 3: #add new one to end and remove first index
						last3Bytes.pop(0) #remove the first one - makes this list act like a queue
					if len(last3Bytes) == 3 and last3Bytes[0] == 127 and last3Bytes[1] == 10 and last3Bytes[2] == 13:
						breakThis = True #^stop reading input
						break
					arrBytes.append(byte) #add finished byte to array of all bytes
					byte = 0
					lenByte = 0 #reset
				if breakThis:
					break
				add = (arrPixel[i] & 3) #get only last 2 bits
				add = add << lenByte #shift bits left by an increasing amount
				byte = byte | add #make the last 2 bits equal to the last 2 bits of each r, g, or b
				lenByte+=2
			if breakThis:
				break
		if breakThis: break

	finStr = ""
	for i in range(len(arrBytes)):
		if i != 0: #don't add the first byte
			finStr+=chr(arrBytes[i]) #convert to ascii and add to final string
	if screenTFileF: #print to command line
		print(finStr)
	else: #print to file
		finStr = finStr[0:len(finStr)-3] #skip the first and last couple bytes (they are this: ) 
		#the 3 ending bytes are the stop codon, so don't include them
		file.write(finStr)
		file.close()


if __name__ == "__main__":
	main(sys.argv[1:])