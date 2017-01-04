"""
Pre-process data set
Handle encoding exception:
    byte read -> decode('gbk','ignore') -> str -> encode('gbk','ignore') -> byte write
"""
import os
import re


def preprocessdataset():
    """preprocessdataset by removing invalid entries and replacing some token"""
    path = r"E:\Documents\OneDrive\Data"
    removestrings = [r'"operationName":""', r'"baseData":{}']
    replacepattern = r".*BPExternalId\?MRN=(.*),UserId=.*"
    outputfilename = r'DES_Test_Log.csv'
    for root, dirs, files in os.walk(path):
        print(dirs)
        for name in files:
            if not name.endswith(".csv"):
                filename = root + "/" + name
                currentfile = open(filename, "rb")
                content = ""
                for line in currentfile.readlines():
                    line = line.decode('gbk', 'ignore')
                    match = re.match(replacepattern, line)
                    if match:
                        mrn = match.group(1)
                        if ',' in mrn:
                            newmrn = mrn.replace(',', ';')
                            line = line.replace(mrn, newmrn)
                    shouldskip = False
                    for removestring in removestrings:
                        if line.find(removestring) != -1:
                            shouldskip = True
                            break
                    if not shouldskip:
                        content += line
                content = content.encode('gbk', 'ignore')
                currentfile.close()
                currentfile = open(root + "/" + outputfilename, "ab")
                currentfile.write(content)
                currentfile.close()


preprocessdataset()
