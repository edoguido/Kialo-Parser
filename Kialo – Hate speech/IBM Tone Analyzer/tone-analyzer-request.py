# --------------------------------------------
# upgrade tools in a new terminal window first
# pip install --upgrade pip
# pip install --upgrade watson-developer-cloud
# --------------------------------------------
# use following module in case of API errors
# from watson_developer_cloud import WatsonApiException
#
# python version required to run this script is 2.7
# because version 3.7 doesn't seem to recognize
# module watson_developer_cloud for import
#
# head over to http://www.json-xls.com/json2xls
# to convert the restuling json file to excel
#
# !!! IMPORTANTE !!!
# 22:58 giorno 7.11.18 Primo Live Share

import time, json
from watson_developer_cloud import ToneAnalyzerV3

FILE_INPUT = '../Kialo-Hate-Speech-nesting.json'
FILE_OUTPUT = 'Kialo-Hate-Speech-analyzed.json'

# we imported time because ToneAnalyzer versions have YYYY-MM-DD format
currentVersion = time.strftime("%Y-%m-%d")
print("Using Tone Analyzer\'s version:" + currentVersion)

tone_analyzer = ToneAnalyzerV3(
    version=currentVersion,
    username='ebe9c8f8-5cfb-4a59-b761-74991e7dae81',
    password='DAwTow5XZGzB',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

with open(FILE_INPUT, 'r') as fi:
    # Loads json as list
    input_data = json.load(fi)

# Take 'ToneInput' key values in input file
for i in range(0, len(input_data)):
    input_texts = input_data[i]['ToneInput']

    # sends data and requests the analysis
    tone_analysis = tone_analyzer.tone( {'text': input_texts}, 'application/json' ).get_result()

    print i+1, "of", len(input_data), "processed"
    # put analyzed content in a brand new key
    input_data[i]['tone_analysis'] = tone_analysis
    to_write = json.dumps(input_data, sort_keys=True, indent=4, separators=(',', ': '))

# file is open in 'append' mode, 
# meaning that new content will be added 
# at the end of the file
with open(FILE_OUTPUT, 'a') as fo:
    # write data to file by appending new data to the end of the file
    # print(to_write)
    fo.write(to_write)