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
# because version 3.7 doesn't seem to recognize the 'watson_developer_cloud' module for import
#
# once converted, you can head over to
# http://www.json-xls.com/json2xls
# to convert the resulting json file to excel format, if needed.

import sys, time, json, re

if len(sys.argv) < 3:
    print "Not enough arguments. Aborting..."
    sys.exit()

elif len(sys.argv) > 3:
    print "Too many arguments. Aborting..."
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]

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

    choose_analysis = raw_input("\nDo you wish to use IBM's Tone Analyzer after parsing the input file? [y/n]: ")

    if choose_analysis == "y" or choose_analysis == "yes" or choose_analysis == "Y" or choose_analysis == "YES":
        """
        ////////////////////////////
        IBM TONE ANALYZER OPERATIONS
        ////////////////////////////
        """

        from watson_developer_cloud import ToneAnalyzerV3

        # we imported time because ToneAnalyzer versions have YYYY-MM-DD format
        current_version = time.strftime("%Y-%m-%d")
        print "\n"
        print "///////////////////////////////////"
        print "-----------------------------------"
        print("Using Tone Analyzer\'s v" + current_version)
        print "-----------------------------------"
        print "///////////////////////////////////"
        print "\n"

        api_option = raw_input("Are you using an API key? [y/n]: ")

        if api_option == "y":
            log1 = raw_input("Please insert your API key\n")
        elif api_option == "n":
            log1 = raw_input("Please insert your Username\n")
            log2 = raw_input("Please insert your Password\n")
        else:
            print("aborting")

        url = raw_input("Now provide the server url for the Tone Analyzer\n")
        print "All set. Initiating analysis process..."

        if api_option == "y":
            tone_analyzer = ToneAnalyzerV3(
                version=current_version,
                iam_apikey=log1,
                url=url
            )
        elif api_option == "n":
            tone_analyzer = ToneAnalyzerV3(
                version=current_version,
                username=log1,
                password=log2,
                url=url
            )


        # default url='https://gateway.watsonplatform.net/tone-analyzer/api'

        for entry in range(0, len(result)):
            # takes 'ToneInput' key values in input file
            input_texts = result[entry]['ToneInput']

            # sends data and requests the analysis
            tone_analysis = tone_analyzer.tone( {'text': input_texts}, 'application/json' ).get_result()

            print entry+1, "of", len(result), "processed", "\033[1A\r"
            # put analyzed content in a brand new key
            result[entry]['tone_analysis'] = tone_analysis
            to_write = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

        """
        ////////////////////////////
        IBM TONE ANALYZER OPERATIONS
        ////////////////////////////
        """

    elif choose_analysis != "y" or choose_analysis != "yes" or choose_analysis != "Y" or choose_analysis != "YES":
        to_write = json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

with open(output_file, 'w') as fo:
    # print to_write
    fo.write(to_write)
    print "/////////////////////"
    print "---------------------"
    print "Operation completed."
    print "---------------------"
    print "/////////////////////"