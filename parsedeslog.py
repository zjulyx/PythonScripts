"""
Pre-process data set
Handle encoding exception:
    byte read -> decode('gbk','ignore') -> str -> encode('gbk','ignore') -> byte write
"""
import os


def getsubstring(originstring, index, beginchar, endchar):
    '''get sub string of assigned index, beginchar and endchar'''
    begin = originstring.find(beginchar, index)
    end = originstring.find(endchar, index)
    return originstring[begin + 1:end]


def findandparse(originstring, keyword, beginchar, endchar):
    '''find the keyword and parse it into dict'''
    index = originstring.find(keyword)
    if index == -1:
        return
    value = getsubstring(originstring, index, beginchar, endchar)
    if keyword == "Timestamp=":
        value = value[value.find('-') + 1:value.find('T') + 6]
    return value


def appendline(line, keywords, shouldfind):
    '''append line to content'''
    first = True
    content = ""
    for keyword in keywords:
        if not first:
            content += ','
        if shouldfind:
            content += findandparse(line, keyword, keywords[keyword][0],
                                    keywords[keyword][1])
        else:
            if keyword.endswith('='):
                content += keyword[0:len(keyword) - 1]
            else:
                content += keyword
        first = False
    content += '\n'
    return content


def parsedeslog():
    """parsedeslog by removing invalid entries and replacing some token"""
    path = r"E:\Documents\DES"
    removestrings = [r'"operationName":""', r'"baseData":{}']
    outputfilename = r'DES_Test_Log.csv'
    keywords = {
        "UserId=": ['=', ','],
        "ClientIp=": ['=', ','],
        "Machine=": ['=', '{'],
        "Api=": ['=', ','],
        "Latency=": ['=', '\"'],
        "Timestamp=": ['=', '{'],
        "succeeded": [':', ','],
    }
    for root, dirs, files in os.walk(path):
        dirs[:] = []
        content = appendline(None, keywords, False)
        for name in files:
            if not name.endswith(".csv"):
                filename = root + "/" + name
                currentfile = open(filename, "rb")
                for line in currentfile.readlines():
                    line = line.decode('gbk', 'ignore')
                    shouldskip = False
                    for removestring in removestrings:
                        if line.find(removestring) != -1:
                            shouldskip = True
                            break
                    if not shouldskip:
                        content += appendline(line, keywords, True)
            content = content.encode('gbk', 'ignore')
            currentfile.close()
            currentfile = open(root + "/" + outputfilename, "ab")
            currentfile.write(content)
            currentfile.close()
            content = ""


parsedeslog()
