import sys, json, re

with open(sys.argv[1], 'r') as fi:
    lines = []
    for line in fi:
        lines.append(line)

    # list containing each parsed comment
    result = []

    # # TO-DO: use discussion title as first entry
    # title = re.search(r"(Discussion Title: )(.*)", lines[0])
    # result.append({
    #     "Title": title.group(2)
    # })

    # we remove the first two lines of the text
    # as we don't need the header
    for i in range(0, 3):
        lines.pop(0)

    # iterate every row in the text file
    for line in lines:
        # find the tree position the comment is in
        tree =  re.search(r"(^(\d{1,}.)+)", line)

        # find if the comment is Pro or Con
        stance = re.search(r"(Con|Pro(?::))", line)

        # find the text of the comment 
        content = re.search(r"((Con|Pro):\s)(.*)", line)

        # define the hierarchy of the current comment 
        # which is based on the tree structure
        parsed = re.findall(r"(\d{1,}(?=\.))+", tree.group())
        level = len(parsed)-1

        # make a dictionary with the single entry
        # and put it at the end of the list
        result.append({
            "Tree": tree.group(),
            "Level": level,
            "Stance": stance.group(),
            "ToneInput": content.group(3)
            })

    # make a json out of the data
    data = json.dumps(result, sort_keys=False, indent=4, separators=(',', ': '))

with open(sys.argv[2], 'w') as fo:
    print data
    fo.write(data)