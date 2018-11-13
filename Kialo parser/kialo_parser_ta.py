# script by Edoardo Guido
# -----------------------------------------------------
# upgrade tools in a new terminal window first
# pip install --upgrade pip
# pip install --upgrade watson-developer-cloud
# -----------------------------------------------------
# use following module in case of API errors
# from watson_developer_cloud import WatsonApiException
#
# python version required to run this script is 2.7
# because version 3.7 doesn't seem to recognize
# the 'watson_developer_cloud' module for import
#
# once converted, you can
# head over to http://www.json-xls.com/json2xls
# to convert the resulting json file to excel format.

import sys, time, json, re
input_file = sys.argv[1]
output_file = sys.argv[2]
ta_bol = sys.argv[3]

with open(input_file, 'r') as fi:
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
    for line in range(0, 3):
        lines.pop(0)

    # iterate every row in the text file
    for line in lines:
        # find the tree position the comment is in
        tree =  re.search(r"^(\d{1,}.)+", line)

        # find if the comment is Pro or Con
        stance = re.search(r"(Con|Pro)(?::)", line)

        # find the text of the comment
        content = re.search(r"((Con|Pro)(?::\s))(.*)", line)

        # define the hierarchy of the current comment
        # which is based on the tree structure
        parsed = re.findall(r"(\d{1,}(?=\.))+", tree.group())
        level = len(parsed)-1

        # make a dictionary with the single entry
        # and put it at the end of the list
        result.append({
            "Tree": tree.group(),
            "Level": level,
            "Stance": stance.group(1),
            "ToneInput": content.group(3)
            })

    if ta_bol == "True":
        """
        ////////////////////////////
        IBM TONE ANALYZER OPERATIONS
        ////////////////////////////
        """

        from watson_developer_cloud import ToneAnalyzerV3

        # we imported time because ToneAnalyzer versions have YYYY-MM-DD format
        currentVersion = time.strftime("%Y-%m-%d")
        print("Using Tone Analyzer\'s version:" + currentVersion)

        username = sys.argv[4]
        passkey = sys.argv[5]
        tone_analyzer = ToneAnalyzerV3(
            version=currentVersion,
            username=username,
            password=passkey,
            url='https://gateway.watsonplatform.net/tone-analyzer/api'
        )

        for entry in range(0, len(result)):
            # takes 'ToneInput' key values in input file
            input_texts = result[entry]['ToneInput']

            # sends data and requests the analysis
            tone_analysis = tone_analyzer.tone( {'text': input_texts}, 'application/json' ).get_result()

            print entry+1, "of", len(result), "processed", "\r"
            # put analyzed content in a brand new key
            result[entry]['tone_analysis'] = tone_analysis
            to_write = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

        """
        ////////////////////////////
        IBM TONE ANALYZER OPERATIONS
        ////////////////////////////
        """

    elif ta_bol == "False":
        to_write = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

with open(output_file, 'w') as fo:
    print to_write
    fo.write(to_write)