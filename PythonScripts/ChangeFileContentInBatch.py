import os

# Change or append file content in batch
# handle encoding exception: byte read -> decode('gbk','ignore') -> str handle
# -> encode('gbk','ignore') -> byte write
def ReplaceFileContent():
	path = "E:\Documents\OneDrive\Code"
	oldString = "using System.Linq;"
	newString = "using System.Collections.Generic;"
	for root,dirs,files in os.walk(path):
		for name in files:
			if(name.endswith(".cs")):
				filename = root + "/" + name
				f = open(filename,"rb")				
				content = ""
				skip = False
				for line in f.readlines():
					line = line.decode('gbk','ignore')
					if line.find(newString) != -1:
						skip = True
					index = line.find(oldString)
					if  (not skip) and (index != -1):
						content+=(newString + "\r\n").rjust(index)
					content+=line
				content = content.encode('gbk','ignore')
				f.close()
				f = open(filename,"wb")				
				f.write(content)
				f.close()					
ReplaceFileContent()
									