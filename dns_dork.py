#!/usr/bin/env python
import argparse
import json
import sys
import urllib
from time import sleep

try:    # Python3 renamed urllib2 to urllib.request
    import urllib2
except ImportError:
    import urllib.request as urllib2
    import urllib.parse as urllib

def get_args():
    global args
    
    parser = argparse.ArgumentParser('dns_dork.py', formatter_class=lambda prog:argparse.HelpFormatter(prog,max_help_position=40))
    parser.add_argument('-t', '--target', help='Target domain', dest='target', required=True)
    parser.add_argument('-v', '--verbose', action="store_true", default=False, help='Verbose mode', dest='verbose', required=False)
    args = parser.parse_args()

def find_subdomains(searchstrings):
    global args
    url = 'http://ajax.googleapis.com/ajax/services/search/web?'
    params = { 'q': "site:"+args.target+' -site:www.'+args.target+searchstrings}
    data = urllib.urlencode(params)
    url = url + data + '&v=1.0'
    print(str(url))

    request = urllib2.Request( url,None, {'Referer': 'http://www.duckduckgo.com' })
    response = urllib2.urlopen(request)
    results = json.loads(response.read().decode("utf-8"))
    
    startlen = len(subdomainlist)

    for reply in results['responseData']['results']:
        if reply['unescapedUrl'] != None:
            print('\n=[Link]= ')
            string = reply['unescapedUrl']
            string = string.replace("http://", "")
            string = string.replace("https://", "")
            subdomain = string.split("/")
            print(subdomain[0] + " " + str(len(subdomainlist)))
            subdomainlist.append(str(subdomain[0])) # subdomain[0] is unicode, cast it to str

    if startlen == len(subdomainlist):
        print("no more domains")
        print(subdomainlist)
        sys.exit()
            
def update_string(xlist):
    searchstrings = ""
    for item in xlist:
        searchstrings = searchstrings + ' -site:'+item
    return searchstrings


if __name__ == "__main__":
    global args
    get_args()
    subdomainlist = []
            
    for x in range(20):
        subdomainlist = list(set(subdomainlist)) # removing any duplicate entires
        searchstrings = update_string(subdomainlist)  # create search string from subdomain list
        find_subdomains(searchstrings)  # find those strings 

    subdomainlist = list(set(subdomainlist)) # removing any duplicate entires
    subdomainlist.sort()
    print(subdomainlist)
