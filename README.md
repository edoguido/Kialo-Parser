# Kialo Parser

[Kialo](https://www.kialo.com/tour) is a great platform. Unfortunately, it's really not so easy to analyze its data, since the only file that can be downloaded (scraping is not permitted) is in .txt format.

This python script takes two arguments:

```bash
kialo_parser.py path/to/input.txt path/to/output.json
```
and uses regular expressions to analyze the input Kialo's discussion data, storing different components in a json file, which has the following keys:

- "Tree": current comment's tree indicator, in the form of [n1].[n2]...[nr] where n is an integer, and r is the level subdivision of such tree.
- "Level": is the current comment's level, where 1 is the first sub-level, generally one "Pro" and one "Con" comment.
- "Stance": indicates if the comment is Pro or Con.
- "ToneInput": is the text content of the comment. The name is already set if the json is then used for [IBM's Tone Analyzer](https://www.ibm.com/watson/services/tone-analyzer/)

Upon execution, the program will ask whether the user wants to use [IBM's Tone Analyzer](https://www.ibm.com/watson/services/tone-analyzer/) after extracting Kialo's data from the provided .txt file.

The required data in order to use IBM's services are:
- The API key or User/Pass combination.
- The URL where the IBM's server is located (and which has been selected during the resource creation process, in the personal IBM page).