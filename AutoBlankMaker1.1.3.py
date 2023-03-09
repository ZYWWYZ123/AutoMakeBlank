#DESIGNED BY Yiwen Zhang@XJTU
#import base part
import sys; import re
import TextFunctions
try:
    with open('article.txt', 'r', encoding='utf-8') as imp_file:
        pass
except:
    a = input("An error occured while loading necessary file 'article.txt', please check the file and restart program. Press enter to exit.")
    sys.exit()
#import extra functions
try:
    import NetworkFunctions
except:
    print("NOTICE: Download module is not available.")
    TextFunctions.ProgSetting['NetFunc'] = False
try:
    with open('wordBlkList.txt', 'r', encoding='utf-8') as word_bl:
        pass
except:
    print("NOTICE: Black list module is not available.")
    TextFunctions.ProgSetting['BlkList'] = False
try:
    with open('wordWitList.txt', 'r', encoding='utf-8') as word_wt:
        pass
except:
    print("NOTICE: White list module is not available")
    TextFunctions.ProgSetting['WhtList'] = False

#Functions
def impBlkList():
    if TextFunctions.ProgSetting['BlkList'] == False:
        return []
    word_all_bl = ''
    with open('wordBlkList.txt', 'r', encoding='utf-8') as word_bl:
        for line in word_bl.readlines():
            word_all_bl += line
        blkWord = TextFunctions.div_words(word_all_bl, 'n')
        return blkWord

def impWhtList():
    if TextFunctions.ProgSetting['WhtList'] == False:
        return []
    word_all_wh = ''
    with open('wordWitList.txt', 'r', encoding='utf-8') as word_wh:
        for line in word_wh.readlines():
            word_all_wh += line
        whtWord = TextFunctions.div_words(word_all_wh, 'n')
        return whtWord

def netFuncErr():
    a = input("Cannot process link for download module is missing. Please check files and restart program. Press enter to quit program.")
    sys.exit()

with open('article.txt', 'r', encoding='utf-8') as impFile:
    words_all = ''; articleSource = ''; articleTitle = ''
    art_parag = []
    impFileLine = impFile.readlines()
    if TextFunctions.linkSearch(impFileLine[0]) == 'TED':
        if TextFunctions.ProgSetting['NetFunc'] == False:
            netFuncErr()
        print('Found a TED link! The page will be opened in a browser. Follow instructions in the program window.')
        articleSource = 'ted'
        NetSource = NetworkFunctions.transGrabberForTED(impFileLine[0])
        articleTitle = NetSource[0]
        impFileLine = NetSource[1].split('\n')
        for num in range(0,len(impFileLine)):
            impFileLine[num] += '\n'
    elif TextFunctions.linkSearch(impFileLine[0]) == 'CNNE':
        if TextFunctions.ProgSetting['NetFunc'] == False:
            netFuncErr()
        print('Found a CNN (listeningexpress.com) link. Text will be processed automatically.')
        articleSource = 'cnn'
        NetSource = NetworkFunctions.transGrabberForCNNExp(impFileLine[0])
        articleTime = NetSource[0]
        articleTitle = NetSource[1]
        impFileLine = NetSource[2].split('\n')
        for num in range(0,len(impFileLine)):
            impFileLine[num] += '\n'
    else:
        articleSource = input("Enter the source of the article to use preset,which can help avoid setting blank in some confusing part in text, or just press enter to ignore this and use basic functions. Choose from: [ted];[cnn]\n")
    for line in impFileLine:
        if line[-1] != '\n':
            line += '\n'
        line = TextFunctions.TransClean(line, articleSource)
        words_all += line
    words_div = TextFunctions.div_words(words_all, 'y')
    while words_div[0] == '\n':
        words_div.pop(0)
    words_div_copy = words_div[:]
    words_count = len(TextFunctions.div_words(words_all, 'n'))
    if words_count < 20:
        a = input("Program stopped for finding the text don't have enough words.Press Enter to quit program.")
        sys.exit()
    blank_minimum = int(words_count*TextFunctions.ProgSetting['blankMinRate'])
    blank_maximum = int(words_count*TextFunctions.ProgSetting['blankMaxRate'])

wordsBlkList = impBlkList(); WhtLst = impWhtList()
blankNumber = 0; roundNum = 0
deletedWord = []; forbiddenList = []
for item in wordsBlkList:
    forbiddenList.append(item)
for item in TextFunctions.blankSignBlkList:
    forbiddenList.append(item)
while blankNumber <= blank_minimum:
    blankNumber = 0; roundNum += 1
    returnString = TextFunctions.blankMaker(words_div, forbiddenList, blank_maximum, deletedWord, WhtLst)
    outPutList = returnString[0]
    deletedWord = returnString[1]
    for item in outPutList:
        if TextFunctions.blankCheck(item):
            blankNumber += 1
    words_div = outPutList
    print(F'Circulate {str(roundNum)}, processed {str(blankNumber)} blanks yet.', end='\r')

#print article
outPutWord = TextFunctions.textCompose(outPutList, words_div_copy, articleTitle)

with open('@Test paper.txt', 'w', encoding='utf-8') as file:
    file.write(outPutWord)
    file.close()

wdMax = len(words_div_copy)
ansNum = 1
ansFile = ''
for c_num in range(0,wdMax):
    if outPutList[c_num] != words_div_copy[c_num]:
        ansFile += F'{str(ansNum)}. {words_div_copy[c_num]}\n'
        ansNum += 1

with open('@Answer sheet.txt', 'w', encoding='utf-8') as file:
    file.write(ansFile)
    file.close()

print(F'\nNOTICE: Program stopped successfully, this article has {str(words_count)} words.')
print(F'NOTICE: Max blanket num: {str(blank_maximum)}. Min blanket num: {str(blank_minimum)}')
print(F'NOTICE: Output file has {str(blankNumber)} blankets.')
a = input("Press enter to quit...")