import time
import json, re
FILE_INPUT = 'should-hate-speech-be-legally-protected-10134.txt'
FILE_OUTPUT = 'Kialo-Hate-Speech-nesting.json'

def clean_data(data):
    # make space for console printout
    for i in range(0, 20):
        print ""

    entry = {}
    result = []
    # read the text file line by line
    data = fi.readlines()
    # we remove the first two lines of the text
    # as we don't need the header
    for i in range(0, 3):
        data.pop(0)

    for i in data:
        tree =  re.findall(r"(^(\d{1,}.)+)", i)[0][0]
        entry["Tree"] = tree

        faction = re.findall(r"(?:(Con|Pro):)\s", i)[0]
        entry["Faction"] = faction

        content = re.findall(r"(Con|Pro{1,}:\s)(.+)", i)[0][1]
        entry["ToneInput"] = content

        parsed = re.findall(r"(\d{1,}(?=\.))+", tree)
        level = len(parsed)-1
        entry["Level"] = level

        result.append(entry)
        print result
        time.sleep(1.5)

    # make a json out of this data
    # data = json.dumps(result, sort_keys=False, indent=4, separators=(',', ': '))
    # print data

with open(FILE_INPUT, 'r') as fi:
    clean_data(FILE_INPUT)

# with open(FILE_OUTPUT, 'w') as fo:
#     fw.write(json.dumps(input_data, sort_keys=True, indent=4, separators=(',', ': ')))