#This Python Script will retrieve the "data/token.json" file and extend it with tokenDescription field
#Selenium is used to do the Google Search ; BeautifulSoup for parsing the Google Search; revChatGPT.ChatGPT for ChatGPT query

import json
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from revChatGPT.ChatGPT import Chatbot

#Your CHATGPT session token, see
chatGPTSessionToken = "YOUR_SESSION_TOKEN"

#Interval to send the next request to ChatGPT in minutes
reqInterval = 3

#Location of the jsonFile
jsonFile = 'data/tokens.json'

#Requested number of Google Results
numOfResults = 3

#Maximum length of query, which is send to ChatGPT
maxLengthOfQuery = 2000

#Read JSON File
def readJson():
    with open(jsonFile,'r') as f:
        data = json.load(f)
    return data

#Write to JSON file
def writeJson(data):
    print("Updating Data in JSON")
    with open(jsonFile,'w') as f:
        json.dump(data, f)


data = readJson()


# create a new Chrome browser instance
def openNewChrome():
    print("Opening new Chrome instance")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

#Do a Google search and return the result
def doGoogleSearch(tokenName):
    print("Starting Google Search")
    driver = openNewChrome()
    # visit the Google search page
    driver.get("https://www.google.com")
    #Accept privacy pop-up
    acceptButton = driver.find_element("id","L2AGLb")
    acceptButton.click()
    # find the search box element and enter your query
    search_box = driver.find_element("name","q")
    search_box.send_keys(tokenName + " crypto description")

    # submit the form to initiate the search
    search_box.submit()

    #this can be activated if the result takes too long
    #time.sleep(5)

    # Get the page source
    html = driver.page_source
    return html

#To parse html repsonse from page
def parseHtml(htmlResponse):
    # Parse the HTML
    soup = BeautifulSoup(htmlResponse, 'html.parser')
    return soup

#Extract Google Search Results
def extractGoogleResults(tokenName):
    print("Extracting Google Results")
    search_results = parseHtml(doGoogleSearch(tokenName)).find_all('div', class_='g')
    url = []
    for i in range(numOfResults):
        title = search_results[i].find('a')
        url.append(title.get('href'))
        #print(url)
    return url

#Get Website content from the Extracted Google Results
def accessURL(url):
    driver = openNewChrome()
    driver.get(url)
    html = driver.page_source
    return html

def getURLContent(tokenName):
    print("Getting the Website Content: ")
    chatGPTText = ""
    for url in extractGoogleResults(tokenName):
        print (url)
        html = accessURL(url)
        response = parseHtml(html).find_all(["p","h1","h2","h3","h4","h5","h6"])
        for element in response:
             chatGPTText += " ".join(element.stripped_strings)
    #print(chatGPTText)
    return chatGPTText
def runChatGPT(prompt):
    print("###Running ChatGPT###")
    while True:
        try:
            chatbot = Chatbot({
            "session_token": chatGPTSessionToken
            }, conversation_id=None, parent_id=None) # You can start a custom conversation

            response = chatbot.ask(prompt, conversation_id=None, parent_id=None) # You can specify custom conversation and parent ids. Otherwise it uses the saved conversation (yes. conversations are automatically saved)
            #Read out message from Response
            print("Read out message from Response")
            message = response['message']
            print("This is the generated message from ChatGPT: ")
            print(message)
            break
        except Exception as e:
            print("An error occurred:", e)
            wait = 15 * 60
            print("We will try in %d seconds" % wait)
            time.sleep(wait)
    return message

    # {
    #   "message": message,
    #   "conversation_id": self.conversation_id,
    #   "parent_id": self.parent_id,
    # }

def reduceQueryLenth(query):
    print("Reducing the query")
    words = query.split()
    #Set length to limit
    limitedQuery = words[:maxLengthOfQuery]
    limitedString = " ".join(limitedQuery)
    #print(limitedString)
    return limitedString

#This is the run function which will iterate through the Json Objects and trigger 1. Google search , 2. ChatGPT Query , 3. write message back to tokens.json
def run():
    print("###Iteration Through JSON starts###")
    for field in data:
        print("###Creating Query String###")
        print ("Executing Script for tokenName: " +field.get("tokenName") + " and token: " + field.get("token"))
        print ("Progress --> Field:  %d" % data.index(field))
        print ("From Total Elements: %d" % len(data))
        if "tokenDescription" in field:
            print("tokenDesciption already exitst. Skip to next one")
        else:
            print("tokenDescription does not exist. Running Query")
            chatGPTQuery = "write a 200 word article on " + field.get("tokenName") + "and the " + field.get("token") + " token, based on the below information, mentioning nothing about price or dates: \n" + getURLContent(field.get("tokenName"))
            print("Adding into dictionary")
            field["tokenDescription"]= runChatGPT(reduceQueryLenth(chatGPTQuery))
            print("Wait %d minutes until next request" % (reqInterval))
            time.sleep(3*60)
        writeJson(data)



#Call the run() function
print("###Starting Script###")
run()
