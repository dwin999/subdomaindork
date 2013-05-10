#!/usr/bin/env python
import argparse
import json
import platform
import sys
import urllib
from time import sleep
#Please input your bing API key below, you can get one from https://datamarket.azure.com/account/keys 
key = 'put api key here'
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
    if sys.stdout.isatty() and platform.system() != "Windows"
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
    parser.add_argument('-g', '--google', action="store_true", default=True, help='Use google search', dest='g', required=False)
    parser.add_argument('-b', '--bing', action="store_true", default=False, help='Use bing API', dest='b', required=False)
    parser.add_argument('-v', '--verbose', action="store_true", default=False, help='Verbose mode', dest='verbose', required=False)
    args = parser.parse_args()
    
def bing_subdomains(searchstrings):
    global args
    user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
    creds = (':%s' % key).encode('base64')[:-1]
    auth = 'Basic %s' % creds
    url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query=%27'
    data = "site%3A"+args.target+'%20-www.'+args.target+searchstrings
    url = url + data + "%27&$top=50&$format=json"
    out.verbose(url.encode('utf-8'))
    if(len(str(url)) > 2048):
        end(subdomainlist)
        exit()
    request = urllib2.Request(url)
    request.add_header('Authorization', auth)
    request.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(request)
    results = json.load(response)
    startlen = len(subdomainlist)
    for reply in results['d']['results']:
        if reply['Url'] != None:
            string = reply['Url']
            string = string.replace("http://", "")
            string = string.replace("https://", "")
            subdomain = string.split("/")
            out.good("Found subdomain - " + subdomain[0] + " [" + str(len(subdomainlist)) + "]")
            subdomainlist.append(subdomain[0].encode('utf-8')) # subdomain[0] is unicode, cast it to str
    if startlen == len(subdomainlist):
        print "no more domains"
        print end(subdomainlist)
        sys.exit()
def bing_update_string(xlist):
    searchstrings = ""
    for item in xlist:     
        searchstrings = searchstrings + '%20-domain%3A'+item
    #error in that the first string cannot have %20 
    searchstrings = searchstrings[3:]
    return searchstrings
        
def google_subdomains(searchstrings):
    global args
    url = 'http://ajax.googleapis.com/ajax/services/search/web?'
    params = { 'q': "site:"+args.target+' -site:www.'+args.target+searchstrings}
    data = urllib.urlencode(params)
    url = url + data + '&v=1.0'
    out.verbose(url.encode('utf-8'))
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
            subdomainlist.append(subdomain[0].encode('utf-8')) # subdomain[0] is unicode, cast it to str

    if startlen == len(subdomainlist):
        print(subdomainlist)
        sys.exit()
            
def update_string(xlist):
    searchstrings = ""
    for item in xlist:
        searchstrings = searchstrings + ' -site:'+item
    return searchstrings

def end(subdomainlist):
    subdomainlist = list(set(subdomainlist)) # removing any duplicate entires
    subdomainlist.sort()
    for item in subdomainlist:
        print item
    print "Total subs: " + str(len(subdomainlist))

if __name__ == "__main__":
    global args
    out = output()
    get_args()
    subdomainlist = []
            
    for x in range(20):
        subdomainlist = list(set(subdomainlist)) # removing any duplicate entires      
        if(args.g):
            searchstrings = update_string(subdomainlist)  # create search string from subdomain list
            google_subdomains(searchstrings)  # find those strings 
        if(args.b):
            searchstrings = bing_update_string(subdomainlist)  # create search string from subdomain list
            bing_subdomains(searchstrings)  # find those strings
            
    end(subdomainlist)
