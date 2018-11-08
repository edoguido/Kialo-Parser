import json, re
FILE_INPUT = 'Kialo-Hate-Speech.json'
FILE_OUTPUT = 'Kialo-Hate-Speech-nesting.json'

with open(FILE_INPUT, 'r') as fi:
    # Loads json as a list
    input_data = json.load(fi)

def add_entry(data, entry):
    # Loop over each element in the collection
    # and set its nesting level based on RegEx
    for i in range(0, len(data)):
        # This comment's tree value
        parsing = data[i]['Tree']
        parsed = re.findall('(\d{1,}(?=\.))+', parsing)
        data[i][entry] = len(parsed)-1

    print(data)

add_entry(input_data, 'Level')

with open(FILE_OUTPUT, 'w') as fo:
    fw.write(json.dumps(input_data, sort_keys=True, indent=4, separators=(',', ': ')))