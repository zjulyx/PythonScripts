"""
Parse rmca log
Handle encoding exception:
    byte read -> decode('gbk','ignore') -> str -> encode('gbk','ignore') -> byte write
"""
import os

LOGLEVEL = {"Info": 0, "Warn": 1, "Error": 2}


def getsubstring(originstring, index, beginchar, endchar):
    '''get sub string of assigned index, beginchar and endchar'''
    begin = originstring.find(beginchar, index)
    end = originstring.find(endchar, index)
    return originstring[begin + 1:end]


def findandparse(originstring, guid, keyword, currentdict, beginchar, endchar):
    '''find the keyword and parse it into dict'''
    index = originstring.find(keyword)
    if index == -1:
        return
    value = getsubstring(originstring, index, beginchar, endchar)
    if keyword == "Timestamp":
        value = value[value.find('-') + 1:value.find('T') + 6]
    if keyword == "Msg":
        value = value.replace(',', ';')
        if keyword not in currentdict[guid]:
            currentdict[guid][keyword] = value
        else:
            currentdict[guid][keyword] += " AND " + value
        index = originstring.find("Detail")
        if index != -1:
            value = getsubstring(originstring, index, beginchar,
                                 endchar).replace(',', ';')
            currentdict[guid][keyword] += " AND " + value
    elif keyword not in currentdict[guid]:
        currentdict[guid][keyword] = value
    elif keyword == "Level":
        if LOGLEVEL[value] > LOGLEVEL[currentdict[guid][keyword]]:
            currentdict[guid][keyword] = value


def parsermcalog():
    """Parse rmca log by removing invalid entries and replacing some token"""
    path = r"E:\Documents\Rmca"
    outputfilename = r'RMCA_Log.csv'
    currentdict = {}
    keywords = {
        "Msg": ['[', ']'],
        "EffectiveEnv": ['[', ']'],
        "BpExtId": ['[', ']'],
        "CaExtId": ['[', ']'],
        "EndPoint": ['[', ']'],
        "Timestamp": ['=', '{'],
        "Level": ['=', '{'],
        "Category": ['=', '{']
    }
    for root, dirs, files in os.walk(path):
        dirs[:] = []
        content = "TrackingGuid"
        for keyword in keywords:
            content += ',' + keyword
        content += '\n'
        for name in files:
            if not name.endswith(".csv"):
                filename = root + "/" + name
                currentfile = open(filename, "rb")
                for line in currentfile.readlines():
                    line = line.decode('gbk', 'ignore')
                    index = line.find('TrackingGuid')
                    if index != -1:
                        guid = getsubstring(line, index, '[', ']')
                        if guid != "":
                            if guid not in currentdict:
                                currentdict[guid] = {}
                            for keyword in keywords:
                                findandparse(line, guid, keyword, currentdict,
                                             keywords[keyword][0],
                                             keywords[keyword][1])
                currentfile.close()
        for guid in currentdict:
            content += guid
            for keyword in keywords:
                if keyword in currentdict[guid]:
                    content += "," + currentdict[guid][keyword]
                else:
                    content += ","
            content += "\n"
        content = content.encode('gbk', 'ignore')
        currentfile = open(root + "/" + outputfilename, "wb")
        currentfile.write(content)
        currentfile.close()


parsermcalog()
