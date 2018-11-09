# dd09-scripting

A collection of useful scripts for data analysis.

## Kialo Parser

Kialo is a great platform. Unfortunately, it's really not so easy to analyze its data, since the only file that can be downloaded (scraping is not permitted) is in .txt format.

This python script takes two arguments:

```bash
kialo_parser.py path/to/input.txt path/to/output.json
```

and uses regular expressions to analyze the input Kialo's discussion data, storing different components in a json file, which has the following keys:

- "Tree": current comment's tree indicator, in the form of [n1].[n2]...[nr] where n is an integer, and r is the level subdivision of such tree.
- "Level": is the current comment's level, where 1 is the first sub-level, generally one "Pro" and one "Con" comment.
- "Stance": indicates if the comment is Pro or Con.
- "ToneInput": is the text content of the comment. The name is already set if the json is then used for [IBM's Tone Analyzer](https://www.ibm.com/watson/services/tone-analyzer/)
