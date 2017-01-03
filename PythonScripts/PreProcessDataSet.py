import os
import re

# Change or append file content in batch
# handle encoding exception: byte read -> decode('gbk','ignore') -> str handle
# -> encode('gbk','ignore') -> byte write
def ReplaceFileContent():
    path = "E:\Documents\OneDrive\Data"
    removeString = r'"operationName":""'
    replacePattern = r".*BPExternalId\?MRN=(.*),UserId=.*"
    for root,dirs,files in os.walk(path):
        for name in files:
            filename = root + "/" + name
            f = open(filename,"rb")
            content = ""
            skip = False
            for line in f.readlines():
                line = line.decode('gbk','ignore')
                match = re.match(replacePattern,line)
                if match:
                    mrn = match.group(1)
                    if ',' in mrn:
                        newmrn=mrn.replace(',',';')
                        line=line.replace(mrn,newmrn)
                if line.find(removeString) == -1:
                    content+=line
            content = content.encode('gbk','ignore')
            f.close()
            f = open(filename,"wb")
            f.write(content)
            f.close()
ReplaceFileContent()