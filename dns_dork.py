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


class output:
    def status(self, message):
        print(col.blue + "[*] " + col.end + message)

    def good(self, message):
        print(col.green + "[+] " + col.end + message)

    def verbose(self, message):
        if args.verbose:
            print(col.brown + "[v] " + col.end + message)

    def warn(self, message):
        print(col.red + "[-] " + col.end + message)

    def fatal(self, message):
        print("\n" + col.red + "FATAL: " + message + col.end)


class col:
    if sys.stdout.isatty():
        green = '\033[32m'
        blue = '\033[94m'
        red = '\033[31m'
        brown = '\033[33m'
        end = '\033[0m'
    else:   # Colours mess up redirected output, disable them
        green = ""
        blue = ""
        red = ""
        brown = ""
        end = ""


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
    out.verbose(str(url).encode('utf-8'))

    request = urllib2.Request( url,None, {'Referer': 'http://www.duckduckgo.com' })
    response = urllib2.urlopen(request)
    results = json.loads(response.read().decode("utf-8"))
    
    startlen = len(subdomainlist)

    for reply in results['responseData']['results']:
        if reply['unescapedUrl'] != None:
            string = reply['unescapedUrl']
            string = string.replace("http://", "")
            string = string.replace("https://", "")
            subdomain = string.split("/")
            out.good("Found subdomain - " + subdomain[0] + " [" + str(len(subdomainlist)) + "]")
            subdomainlist.append(str(subdomain[0])) # subdomain[0] is unicode, cast it to str

    if startlen == len(subdomainlist):
        print(subdomainlist)
        sys.exit()
            
def update_string(xlist):
    searchstrings = ""
    for item in xlist:
        searchstrings = searchstrings + ' -site:'+item
    return searchstrings


if __name__ == "__main__":
    global args
    out = output()
    get_args()
    subdomainlist = []
            
    for x in range(20):
        subdomainlist = list(set(subdomainlist)) # removing any duplicate entires
        searchstrings = update_string(subdomainlist)  # create search string from subdomain list
        find_subdomains(searchstrings)  # find those strings 

    subdomainlist = list(set(subdomainlist)) # removing any duplicate entires
    subdomainlist.sort()
    print(subdomainlist)
