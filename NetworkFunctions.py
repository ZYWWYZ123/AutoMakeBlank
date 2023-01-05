try:
    from selenium import webdriver
    import sys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from bs4 import BeautifulSoup
    import TextFunctions
except:
    print("Can't load selenium / lxml / bs4.The program needs these to work properly.")
def transGrabberForTED(linkIn):
    #load browser
    browseOption = webdriver.EdgeOptions()
    browseOption.add_experimental_option('excludeSwitches',['enable-logging'])
    browseOption.page_load_strategy = 'eager'
    driverWebPage = webdriver.Edge(options=browseOption, service=Service('msedgedriver.exe'))
    if linkIn[-11:] != '/transcript':
        linkIn += '/transcript'
    driverWebPage.get(linkIn)

    a = input("Make sure the page is properly loaded, then press enter. Wait/Refresh until you see transcript text.")
    windows = driverWebPage.window_handles
    driverWebPage.switch_to.window(windows[-1])
    webSource = driverWebPage.page_source
    goodSoup = BeautifulSoup(webSource,'lxml')
    try:
        transClassTreeList = goodSoup.find_all(class_='mb-6 w-full')
    except:
        print("You may open wrong page!")
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
    returnlist = []
    returnlist.append(transTitle)
    returnlist.append(transcriptText)
    with open(transTitle + ".txt",'w',encoding='utf-8') as fileObject:
        fileObject.write(transcriptText)
        fileObject.close()
    return returnlist
