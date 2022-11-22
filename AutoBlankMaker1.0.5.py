#DESIGNED BY Yiwen Zhang@XJTU
import re
import sys
import NetworkFunctions
import TextFunctions
try:
    with open('article.txt', 'r', encoding='utf-8') as imp_file:
        test_t = imp_file.readlines()
    with open('wordBlkList.txt', 'r', encoding='utf-8') as word_bl:
        test_t = word_bl.readlines()
except UnicodeDecodeError:
    print('You used wrong encoding way to send the file. Use utf-8 instead of others.')
    sys.exit()
except:
    print('An error occured! Check your article and black list.')
    sys.exit()

print('Choose: cnn10,ted,chinadaily...')
articleSource = input('Where did this article come from? ')

def impBlkList():
    word_all_bl = ''
    with open('wordBlkList.txt', 'r', encoding='utf-8') as word_bl:
        for line in word_bl.readlines():
            word_all_bl += line
        blkWord = TextFunctions.div_words(word_all_bl, 'n')
        return blkWord

with open('article.txt', 'r', encoding='utf-8') as imp_file:
    words_all = ''
    art_parag = []
    for line in imp_file.readlines():
        if line[-1] != '\n':
            line += '\n'
        line = TextFunctions.timeApplauseLineDel(line, articleSource)
        words_all += line
    words_div = TextFunctions.div_words(words_all, 'y')
    words_div_copy = words_div[:]
    words_count = len(TextFunctions.div_words(words_all, 'n'))
    if words_count < 15:
        print('This article needs more words!')
        sys.exit()
    blank_minimum = int(words_count*0.095)
    blank_maximum = int(words_count*0.125)

wordsBlkList = impBlkList()
blankNumber = 0
deletedWord = []
while blankNumber <= blank_minimum:
    blankNumber = 0
    returnString = TextFunctions.blankMaker(words_div, wordsBlkList, blank_maximum, deletedWord)
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