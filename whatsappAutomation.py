# import Libraries
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# Function finds and selects new chat
def new_chat(user_name):
    searchButton = driver.find_element_by_xpath('//button[@class="_28-cz"]')
    searchButton.click()
    searchChat = driver.find_element_by_xpath('//div[@class="_13NKt copyable-text selectable-text"]')
    searchChat.send_keys(user_name)
    time.sleep(2)
    try:
        user1 = driver.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
        user1.click()
        time.sleep(1)
    except NoSuchElementException:
        print('User "{}" is not in the contact list'.format(user_name))

# Function sends message in chat box
def sendMsg(message):
    try:
        msgBox = driver.find_element_by_xpath('//div[@class="p3_M1"]')#_2A8P4 p3_M1
        msgBox.send_keys(message)
        time.sleep(1)
        sendButton = driver.find_element_by_xpath('//button[@class="_4sWnG"]')
        sendButton.click()
    except NoSuchElementException:
        print("exception")
        msgBox = driver.find_element_by_xpath('//div[@class="p3_M1 _1YbbN"]')  # _2A8P4
        msgBox.send_keys(message)
        time.sleep(1)
        sendButton = driver.find_element_by_xpath('//button[@class="_4sWnG"]')
        sendButton.click()

# Function sends file from the MediaPath
def sendFile(path):
    driver.find_element_by_css_selector("span[data-icon='clip']").click();
    driver.find_element_by_xpath('//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]').send_keys(path);
    time.sleep(2)
    sendFileButton = driver.find_element_by_xpath('//div[@class="_165_h _2HL9j"]') #SncVf _3doiV
    sendFileButton.click()
    return True

def returnNewMsgList():
    newMsgList = []
    for key in range(1, 15):
        try:
            if driver.find_element_by_xpath(
                    '//*[@id="pane-side"]/div[1]/div/div/div["{}"]/div/div/div[2]/div[2]/div[2]/span[1]/div/span'.format(
                            key)).is_displayed():
                newMsgList.append(key)
        except:
            pass
        #time.sleep(0.5)
    if len(newMsgList) == 0 :
        return False
    else:
        return True

# Initializing web driver
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=C:\\Users\\keert\\AppData\\Local\\Google\\Chrome\\User Data') # User previous data for quick Log
options.add_argument('--profile-directory=Data\\Default')
driver = webdriver.Chrome(executable_path='../drivers/chromedriver92.exe',options=options)

# Starts driver
driver.get('https://web.whatsapp.com/')
driver.maximize_window()

# Reading contact list
contactData = pd.read_csv('../data/Contact_list.csv')

# taking only the first name
firstNameList = list(contactData.iloc[:,0].values)
index = 0
for name in firstNameList:
    name=name.strip()
    firstNameList[index]=name + ' '
    index+=1

# taking only the last name
lastNameList = list(contactData.iloc[:,1].values)
# concatenating the two first and last names
usernameList = [i + j for i, j in zip(firstNameList, lastNameList)]

# reading msg file
MsgFile = open('../data/textMsg.txt','r')

WholeMsg = []
for line in MsgFile:
    WholeMsg.append(line.strip())

message = ''

# ------------------------------------------------------------------------------------------------------------------- MediaPath for Media
MediaPath = 'C:\\Users\\INDIA\\Desktop\\Untitled.png'

# variable stored number of lines before sending the media file
linesBeforeMedia = int(input('lines before media file '))
linesBeforeMedia += 1

# waits for user input until whatsapp beb is ready
input('press enter once ready')
time.sleep(2)

# used as a counter
i = 0
status = False

# keeps a count of number of contacts already broadcasted
countSent = 0
# start reading each name and sen msg each
for username in usernameList:
    try:
        user = driver.find_element_by_xpath('//span[@title="{}"]'.format(username))
        user.click()
    except NoSuchElementException:  # in case contact is not in recent chats
        new_chat(username)

    time.sleep(2 )

    # reads line wise the whole text
    for sentence in WholeMsg:
        i += 1
        if i == linesBeforeMedia:
            time.sleep(1)
            status = sendFile(MediaPath)
            if status == True:
                time.sleep(1)
                sendMsg(sentence)
        else:
            time.sleep(2)
            sendMsg(sentence)
        time.sleep(1)

    # checks if the file was sent... if not it resends
    #if status == False and linesBeforeMedia != -1:
    #    status = sendFile(MediaPath)
    #    if status == True:
    #        status = False
    #else:
    #    status = False

    i = 0
    countSent+=1
    if countSent % 5 == 0:
        if returnNewMsgList():
            stopBroadCast = input('stop Broadcast Y/N : ')
            if stopBroadCast == 'Y' or stopBroadCast == 'y':
                print('deleting {} number of contacts'.format(countSent))
                data = pd.read_csv('../data/Contact_list.csv')
                temp_data = data.loc[countSent:]
                temp_data.to_csv('../data/Contact_list.csv', index=False)
                break
            else :
                time.sleep(2)
                continue
    time.sleep(1)