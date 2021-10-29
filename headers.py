#!/usr/bin/python3
#Title: headers.py
#Author: ApexPredator
#License: MIT
#Github: https://github.com/ApexPredator-InfoSec/header_check
#Description: This script take a URL or list or URLs as arguments and tests for the headers: 'Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options', and 'Server'
import requests
import argparse
import socket
from urllib3.exceptions import InsecureRequestWarning

parser = argparse.ArgumentParser(prog='headers.py', usage='python3 -t <target> -f <file contianing target list> -d\npython3 headers.py -t https://securityheaders.com -d\npython3 headers.py -f urls.txt') #build argument list
parser.add_argument('-t', '--target', help='Target URL', required=False)
parser.add_argument('-f', '--file', help='File Containing Target URLs', required=False)
parser.add_argument('-d','--debug', help='Debug with proxy', required=False, action = 'store_const', const = True)
args = parser.parse_args()

s = requests.session()
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) #disable SSL verification warning to cleanup output

http_proxy = 'http://127.0.0.1:8080' #define proxy address to enable using BURP or ZAP
proxyDict = { #define proxy dictionary to enable using BURP or ZAP
            "http" : http_proxy,
            "https" : http_proxy
}

if args.debug:
    proxy = proxyDict #enable proxy if -d or --debug is present
else:
    proxy = False #disable proxy is -d or --debug is not present

def test_url(target):

    print("[+] Sending get request to target and checking header....")
    res = s.get(target, verify=False, proxies=proxy) #perform get request on url, disble SSL verification to prevent error for sites with invalid certs, proxy if proxy is enabled
    if 'https://' in target: #test for https url
        test_headers(target, res, 'Strict-Transport-Security') #test for Strict-Transport-Security header
        test_headers(target, res, 'Content-Security-Policy') #test for Content-Security-Policy
        test_headers(target, res, 'X-Frame-Options') #test for X-Frame-Options header
        test_headers(target, res, 'Server') #test for Server header
    elif 'http://' in target: #test for http url
        test_header(target, res, 'Content-Security-Policy') #test for Content-Security-Policy
        test_header(target, res, 'X-Frame-Options') #test for X-Frame-Options header
        test_header(target, res, 'Server') #test for Server header
    else:
        print("%s is an invalid URL" %target) #print invalid url if not https or http

def test_headers(target, res, header):
    print("[+]Testing headers for %s" %target + ' IP: ' + socket.gethostbyname(target[8:])) #print URL being tested and its IP
    if header in res.headers: #test if the header passed to test_headers is in the get response headers
        print("[+] %s is enabled" %header) #print header is enabled
        print("[+] Value of %s header is: %s" %(header,res.headers[header])) #print value of header

    else:
        print("[-] !!!! %s is not enabled on %s" %(header,target) + ' IP: ' + socket.gethostbyname(target[8:])) #print header is not enabled if it is not present, display URL and IP

def test_header(target, res, header):
    print("[+]Testing headers for %s" %target + ' IP: ' + socket.gethostbyname(target[7:])) #print URL being tested and its IP
    if header in res.headers: #test if header passed to test_header is in the get response headers
        print("[+] %s is enabled" %header) #print the header is enabled
        print("[+] Value of %s header is: %s" %(header,res.headers[header])) #print the vlaue of the header

    else:
        print("[-] !!!! %s is not enabled on %s" %(header,target) + ' IP: ' + socket.gethostbyname(target[7:])) #print header is not enabled if header is not found in get response header, display URL and IP

def main():

    if args.target: #test it -t or --target were passed and set target with value passed
        target = args.target
        test_url(target)

    elif args.file: #test if -f or --file were passed and set target with file named passed
        file = args.file
        with open(file, 'r') as target_list: #open file passed
            for line in target_list.readlines(): #read the lines in
                target = line.strip() #set target
                print("\n[+]Fetching URL from file.......\n")
                test_url(target) #test the url currently set in target
    else:
        print("[-]Either -t or -f arguments are required\nusage: python3 -t <target> -f <file contianing target list> -d\npython3 headers.py -t https://securityheaders.com -d\npython3 headers.py -f urls.txt") #print help message if neither -t or -f is passed

if __name__ == '__main__':

    main()
