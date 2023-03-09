try:
    from selenium import webdriver
    import sys; import re; import time
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from bs4 import BeautifulSoup
    import TextFunctions
    import requests
except:
    print("Can't load selenium / lxml / bs4 / requests. This extension needs these to work properly.")

def loadBrowser():
    browseOption = webdriver.EdgeOptions()
    browseOption.add_experimental_option('excludeSwitches',['enable-logging'])
    browseOption.page_load_strategy = 'eager'
    Driver = webdriver.Edge(options=browseOption, service=Service('msedgedriver.exe'))
    return Driver

def transGrabberForTED(linkIn):
    driverWebPage = loadBrowser()
    if linkIn[-11:] != '/transcript':
        linkIn += '/transcript'
    while True:
        try:
            driverWebPage.get(linkIn)
            break
        except:
            print('An error occured! Retry in 5s!')
            time.sleep(5)
    a = input("Make sure the page is properly loaded, then press enter. Wait/Refresh until you see transcript text.")
    windows = driverWebPage.window_handles
    driverWebPage.switch_to.window(windows[-1])
    webSource = driverWebPage.page_source
    goodSoup = BeautifulSoup(webSource,'lxml')
    try:
        transClassTreeList = goodSoup.find_all(class_='mb-6 w-full')
    except:
        print("An error ouuured while grabbing text!")
        sys.exit()
    transClassLength = len(transClassTreeList)
    transcriptText = ""
    for num in range(0,transClassLength):
        textPar = transClassTreeList[num].span.text[:-1]
        for letter in textPar:
            if letter == "\n":
                transcriptText += ' '
            else:
                transcriptText += letter
        transcriptText += "\n"
    transTitle = TextFunctions.textClean(goodSoup.find_all(class_='mb-2 flex w-full flex-col')[0].h1.text)
    with open(transTitle + ".txt",'w',encoding='utf-8') as fileObject:
        fileObject.write(transcriptText)
        fileObject.close()
    return transTitle, transcriptText

def transGrabberForCNNExp(linkIn):
    linkIn = linkIn.replace('%20',' '); linkIn = linkIn.replace('.html', '.txt')
    replacePo = re.search(r'\d{4}-\d{2}-\d{2}',linkIn).span()
    linkIn = linkIn.replace(linkIn[replacePo[0]:replacePo[1]],'cnn10 ' + linkIn[replacePo[0]:replacePo[1]])
    while True:
        try:
            webPage = requests.get(linkIn)
            break
        except:
            print('An error occured! Retry in 5s!')
            time.sleep(5)
    textDownDiv = webPage.text.replace('\r\n','\n').split('\n')
    with open(textDownDiv[0] + '.txt', 'w', encoding='utf-8') as fileObject:
        fileObject.write(webPage.text.replace('\r\n','\n'))
        fileObject.close()
    Time = ''; Title = ''; Text = ''; Switch = 0
    for item in textDownDiv:
        if Switch == 0:
            if re.match(r'CNN10 \d{4}-\d{2}-\d{2}',item):
                Time = item
                Switch = 1
        elif Switch == 1:
            if re.search(r'Aired .*a ET',item):
                Title = item.split(' Aired')[0]
                Switch = 2
        elif Switch == 2:
            if re.match(r'THIS IS A RUSH TRANSCRIPT',item):
                Switch = 3
        elif Switch == 3:
            Text += item; Text += '\n'
    return Time, Title, Text