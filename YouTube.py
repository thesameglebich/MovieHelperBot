import urllib
from urllib import request
from urllib.parse import quote
import re, os, sys
from copy import copy

searchURL = "https://www.youtube.com/results?search_query="
watchURL = "https://www.youtube.com/watch?v="
def findlink(name):
    name += " обзор"
    newlink = searchURL+quote(name)
    doc = urllib.request.urlopen(newlink).read().decode('cp1251', errors='ignore')
    match = re.findall("\?v\=(.+?)\"", doc)
    finallink = copy(watchURL) + match[0]
    return finallink

findlink("майор гром")