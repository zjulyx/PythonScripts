"""
copy file content from test.cs to program.cs in batch
Handle encoding exception:
    byte read -> decode('gbk','ignore') -> str -> encode('gbk','ignore') -> byte write
"""
import os


def copycontent():
    """replace file content by replacing oldstring with newstring"""
    programpath = r"E:\Documents\Code\Program"
    testpath = r"E:\Documents\Code\Test"
    teststring = r"[TestMethod]"
    programstring = r"public static void Main()"
    for root, dirs, files in os.walk(testpath):
        dirs[:] = []
        for name in files:
            testfilename = root + "/" + name
            testfile = open(testfilename, "rb")
            testcontent = ""
            start = False
            cnt = 0
            for line in testfile.readlines():
                line = line.decode('gbk', 'ignore')
                if line.find("_TestHelper"):
                    line = line.replace("_TestHelper", "Helper")
                if line.find("StringToCharArray"):
                    line = line.replace("StringToCharArray",
                                        "Helper.StringToCharArray")
                if start:
                    if cnt == 1:
                        testcontent += line
                    else:
                        cnt += 1
                if line.find(teststring) != -1:
                    start = True
                elif line.find("        }") != -1:
                    start = False
            testfile.close()
            for root1, dirs1, files1 in os.walk(programpath):
                dirs1[:] = []
                for name1 in files1:
                    if name == name1:
                        programfilename = root1 + "/" + name1
                        programfile = open(programfilename, "rb")
                        programcontent = ""
                        skip = False
                        for line1 in programfile.readlines():
                            line1 = line1.decode('gbk', 'ignore')
                            if line1.find(programstring) != -1:
                                skip = True
                                programcontent += line1
                                programcontent += testcontent
                            if not skip:
                                programcontent += line1
                            if line1.find("        }") != -1:
                                skip = False
                        programcontent = programcontent.encode('gbk', 'ignore')
                        programfile.close()
                        programfile = open(programfilename, "wb")
                        programfile.write(programcontent)
                        programfile.close()


copycontent()
