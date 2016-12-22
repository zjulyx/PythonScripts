import os

# Change or append file content in batch
# handle encoding exception: byte read -> decode('gbk','ignore') -> str handle -> encode('gbk','ignore') -> byte write

def ReplaceFileContent():
	path = "E:\Documents\OneDrive\Code"
	for root,dirs,files in os.walk(path):
		for name in files:
			if(name.endswith(".cs")):
				filename = root + "/" + name
				f = open(filename,"rb")				
				content=""
				for line in f.readlines():
					line=line.decode('gbk','ignore')
					index = line.find("public class Solution")
					newstring = "[Difficulty(Difficulty.Hard)]\n"
					if index != -1:
						content+=newstring.rjust(len(newstring) + index)
					content+=line
				content=content.encode('gbk','ignore')
				f.close()
				f = open(filename,"wb")				
				f.write(content)
				f.close()					
ReplaceFileContent()
									