
def flatten_dict(d): #input: 처칠 key 아래의 dict, output: 대/중/소제목 태깅된 string인데 string 안에 그 인물의 모든 내용들이 들어가있음
    addedResult = ''
    for key, value in d.items():
        if isinstance(value, dict):
            addedResult += "<" + key + ">" + flatten_dict(value) + "</" + key + ">"
        else:
            addedResult += " " + str(value)
    return addedResult

def real_flatten(dictData): #input: crawled dict, output: {person: content ...}
    tempDict = {}
    for key, value in dictData.items():
        tempString = flatten_dict(dictData[key])
        tempDict[key] = tempString
    return tempDict

# for key, value in tempDict.items(): #
#    print(f"Key: {key}, Value: {value}")

