"""
Change or append file content in batch
Handle encoding exception:
    byte read -> decode('gbk','ignore') -> str -> encode('gbk','ignore') -> byte write
"""
import os


def replacefilecontent():
    """replace file content by replacing oldstring with newstring"""
    path = r"E:\Documents\OneDrive\Code"
    oldstring = "using System.Linq;"
    newstring = "using System.Collections.Generic;"
    for root, dirs, files in os.walk(path):
        print(dirs)
        for name in files:
            if name.endswith(".cs"):
                filename = root + "/" + name
                currentfile = open(filename, "rb")
                content = ""
                skip = False
                for line in currentfile.readlines():
                    line = line.decode('gbk', 'ignore')
                    if line.find(newstring) != -1:
                        skip = True
                    index = line.find(oldstring)
                    if (not skip) and (index != -1):
                        content += (newstring + "\r\n").rjust(index)
                    content += line
                content = content.encode('gbk', 'ignore')
                currentfile.close()
                currentfile = open(filename, "wb")
                currentfile.write(content)
                currentfile.close()


replacefilecontent()
