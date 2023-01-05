#DESIGNED BY Yiwen Zhang@XJTU
import sys
import NetworkFunctions
import TextFunctions
try:
    with open('article.txt', 'r', encoding='utf-8') as imp_file:
        test_t = imp_file.readlines()
    with open('wordBlkList.txt', 'r', encoding='utf-8') as word_bl:
        test_t = word_bl.readlines()
except:
    a = input('An error occured! Check your article and black list.')
    sys.exit()

def impBlkList():
    word_all_bl = ''
    with open('wordBlkList.txt', 'r', encoding='utf-8') as word_bl:
        for line in word_bl.readlines():
            word_all_bl += line
        blkWord = TextFunctions.div_words(word_all_bl, 'n')
        return blkWord

with open('article.txt', 'r', encoding='utf-8') as impFile:
    words_all = ''
    articleSource = ''
    articleTitle = ''
    art_parag = []
    impFileLine = impFile.readlines()
    if TextFunctions.linkSearch(impFileLine[0]) == 'TED':
        articleSource = 'ted'
        NetSource = NetworkFunctions.transGrabberForTED(impFileLine[0])
        articleTitle = NetSource[0]
        impFileLine = NetSource[1].split('\n')
        for num in range(0,len(impFileLine)):
            impFileLine[num] = impFileLine[num] + '\n'
    else:
        articleSource = input("Choose method based on it's source: [ted];[cnn10]\n")
    for line in impFileLine:
        if line[-1] != '\n':
            line += '\n'
        line = TextFunctions.timeApplauseLineDel(line, articleSource)
        words_all += line
    words_div = TextFunctions.div_words(words_all, 'y')
    words_div_copy = words_div[:]
    words_count = len(TextFunctions.div_words(words_all, 'n'))
    if words_count < 20:
        a = input('This article needs more words!')
        sys.exit()
    blank_minimum = int(words_count*TextFunctions.ProgSetting['blankMinRate'])
    blank_maximum = int(words_count*TextFunctions.ProgSetting['blankMaxRate'])

wordsBlkList = impBlkList()
blankNumber = 0
deletedWord = []
forbiddenList = []
for item in wordsBlkList:
    forbiddenList.append(item)
for item in TextFunctions.blankSignBlkList:
    forbiddenList.append(item)
while blankNumber <= blank_minimum:
    blankNumber = 0
    returnString = TextFunctions.blankMaker(words_div, forbiddenList, blank_maximum, deletedWord)
    outPutList = returnString[0]
    deletedWord = returnString[1]
    for item in outPutList:
        if TextFunctions.blankCheck(item):
            blankNumber += 1
    words_div = outPutList
    print(F'Status: {str(blankNumber)} blankets has been set yet.')

#print article
outPutWord = TextFunctions.textCompose(outPutList, words_div_copy)

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

print(F'NOTICE: This article has {str(words_count)} words.')
print(F'Max blanket num: {str(blank_maximum)}. Min blanket num: {str(blank_minimum)}')
print(F'Now the test has {str(blankNumber)} blankets.')
a = input("Press enter to quit...")