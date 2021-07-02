# pip install bs4
# pip install selenium
# need Chrome Web Driver

from bs4 import BeautifulSoup
from selenium import webdriver
import os
import argparse
import requests

def parseArgument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required=True, help="html file(absolute path)")
    parser.add_argument('--timeout', required=False, help="Connection Timeout", default=5)
    
    return parser.parse_args()

def getSource(driver):
    html = driver.page_source # Get HTML Source
    bs = BeautifulSoup(html, 'html.parser') # Initialize BeautifulSoup Object

    return bs

def extractIP(ip):
    idx = ip.find('>')
    return ip[idx+1:-5]

def extractPort(port):
    idx = port.find('>')
    protocolIdx = port.find('(')
    return port[idx+1:protocolIdx -1]

def makeInfoDict(bsList):
    infoDict = {}
    ipTemp = ""

    for i in range(len(bsList)):
        if '"head">확인' in bsList[i]:
           ipTemp = extractIP(bsList[i+2])
           infoDict[ipTemp] = "DEFAULT"

        elif '포트:' in bsList[i]:
            port = []
            for j in range(i+1, 99999):
                if "TCP" not in bsList[j] and "UDP" not in bsList[j]:
                    break

                port.append(extractPort(bsList[j]))

            infoDict[ipTemp] = port

    return infoDict

if __name__ == '__main__':
    args = parseArgument()

    target = args.target
    timeout = int(args.timeout)
    print(timeout)
    
    cwd = os.getcwd().replace("\\", "/") + "/"
    
    url = "file:///" + cwd + target
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument('headless')

    driver = webdriver.Chrome('C:\\Users\\pijy0\\Documents\\chromedriver.exe', options=options) # Chrome Driver Path
    driver.get(url) # Reqeust to Target using GET Method

    bs = getSource(driver)
    bsList = str(bs).split("\n")
    
    infoDict = makeInfoDict(bsList)

    for ip in infoDict.keys():
        for port in infoDict.get(ip):
            url = "http://" + ip + ":" + port + "/"
            print(url) 
    
            try:
                if int(port) == 9100:
                    data = {"first":"AAAAAAAAAA", "second":"bbbbbbb"}
                    res = requests.post(url, data = data)
                    continue

                res = requests.get(url, timeout=timeout)
                print(res.text)
                print(res.status_code)

            except Exception as e:
                print(e)
                print("EXCEPTED >> " + ip + ":" + port)
    
    driver.close()