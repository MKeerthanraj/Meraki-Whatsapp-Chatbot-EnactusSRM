# import libraries
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

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

# initializing the webdriver
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=C:\\Users\\keert\\AppData\\Local\\Google\\Chrome\\User Data') # User previous data for quick Log
options.add_argument('--profile-directory=Data\\Default')
driver = webdriver.Chrome(executable_path='../drivers/chromedriver92.exe',options=options)

# Files containing replies to each choice
optionAFile = open('../data/optionA.txt','r')
optionBFile = open('../data/optionB.txt','r')
optionCFile = open('../data/optionC.txt','r')
optionDFile = open('../data/optionD.txt','r')
optionEFile = open('../data/optionE.txt','r')

# Variables store the reply
optionAReply = optionAFile.read()
optionBReply = optionBFile.read()
optionCReply = optionCFile.read()
optionDReply = optionDFile.read()
optionEReply = optionEFile.read()

# Funtion returns reply text for each choice
def Choice(Msg):
    switcher = {
        'A' : optionAReply,
        'B' : optionBReply,
        'C' : optionCReply,
        'D' : optionDReply,
        'E' : optionEReply,
        'UNSUBSCRIBE' : 'You have been successfully Unsubscribed. We are sad to see you go...',
        '1010' : 'I am not so dumb Nerd, I can understand English!! Haha'
    }
    return switcher.get(Msg,'Please reply with the options *A*, *B*, *C*, *D*, *E*')

# Function to read the most recent msg
def readNewText():
    try:
        recentDiv = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div[last()]')
        recentObj=str(recentDiv.text)
    except NoSuchElementException:
        recentDiv = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[2]/div[last()]')
        recentObj = str(recentDiv.text)
    recentList=recentObj.split('\n')
    mostRecentMsg = recentList[0]
    return mostRecentMsg

# Function finds and selects rest chat if not in recents
def new_chat(user_name):
    searchButton = driver.find_element_by_xpath('//button[@class="_28-cz"]')
    searchButton.click()
    searchChat = driver.find_element_by_xpath('//div[@class="_13NKt copyable-text selectable-text"]')
    searchChat.send_keys(user_name)
    time.sleep(2)
    try:
        user1 = driver.find_element_by_xpath('//span[@title="{}"]'.format(user_name))
        user1.click()
        time.sleep(3)
        try:
            msgBox = driver.find_element_by_xpath('//div[@class="p3_M1"]')
            msgBox.send_keys('.')
            time.sleep(2)
            sendButton = driver.find_element_by_xpath('//button[@class="_4sWnG"]')
            sendButton.click()
        except NoSuchElementException:
            msgBox = driver.find_element_by_xpath('//div[@class="p3_M1 _1YbbN"]')
            msgBox.send_keys('.')
            time.sleep(2)
            sendButton = driver.find_element_by_xpath('//button[@class="_4sWnG"]')
            sendButton.click()

    except NoSuchElementException:
        print('User "{}" is not in the contact list'.format(user_name))

# Function to keep the bot resting in my contact until someone replies
def GoTosleep():
    #
    #--------------------------------------------------------------------------------------------------------------------
    # Bot rest in contact
    #
    username = 'Keerthan Raj Telangana'
    try:
        restuser = driver.find_element_by_xpath('//span[@title="{}"]'.format(username))
        restuser.click()
    except NoSuchElementException:
        new_chat(username)

    time.sleep(3)

# Function to Unsubscribe user:
def Unsubscribe():
    username = driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div[1]/div/span').text
    ind = usernameList.index(username)
    contactData.drop([ind],inplace=True)
    contactData.to_csv('../data/Contact_list.csv',index=False)
    return

# starting chrome
driver.get('https://web.whatsapp.com/')
driver.maximize_window()

#input anyting once ready
input('press enter once ready')

time.sleep(2)

# variable to control the infinite loop
infinite = 0

newMsgList=[]

# infinite loop to keep reading new msgs or wait for them
while infinite == 0:
    for key in range(1, 15):
        try:
            if driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div["{}"]/div/div/div[2]/div[2]/div[2]/span[1]/div/span'.format(key)).is_displayed():
                newMsgList.append(key)
        except:
            pass
        time.sleep(0.5)

    if len(newMsgList) == 0:
        GoTosleep()
        continue

    for k in newMsgList:
        try:
            user = driver.find_element_by_xpath(
                '//*[@id="pane-side"]/div[1]/div/div/div["{}"]/div/div/div[2]/div[2]/div[2]/span[1]/div/span'.format(
                    k))
            user.click()
            time.sleep(3)
            Msg = readNewText()
            if Msg == 'Unsubscribe':
                Unsubscribe()
            Msg = Msg.upper()
            Reply = Choice(Msg)
            time.sleep(1)
            try:
                msgBox = driver.find_element_by_xpath('//div[@class="p3_M1"]')
                msgBox.send_keys(Reply)
            except NoSuchElementException:
                msgBox = driver.find_element_by_xpath('//div[@class="p3_M1 _1YbbN"]')
                msgBox.send_keys(Reply)
            time.sleep(3)
            try:
                sendButton = driver.find_element_by_xpath('//button[@class="_4sWnG"]')
                sendButton.click()
            except Exception as e:
                print(e)
        except:
            pass

    GoTosleep()

    newMsgList=[]
