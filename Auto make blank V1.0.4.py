#DESIGNED BY Matt Zhang@XJTU
import re
import random
import sys
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

signBlkList = ['',' ']
blankSignBlkList = [',','.','"','\n','!','?','(',')',':',';']

def div_words(word_file, keep_sign):
    if keep_sign == 'n':
        #don't keep sign
        words_splited = re.split('[,|!|.|\s|\n|"|?|(|)|:|;]', word_file)
    else:
        #keep sign except space and blank
        words_splited = re.split(r'([,|!|.|\s|\n|"|?|(|)|:|;])', word_file)
    nCounter = 0
    while nCounter < len(words_splited):
        if words_splited[nCounter] in signBlkList:
            words_splited.pop(nCounter)
        else:
            nCounter += 1
    return words_splited

def impBlkList():
    word_all_bl = ''
    with open('wordBlkList.txt', 'r', encoding='utf-8') as word_bl:
        for line in word_bl.readlines():
            word_all_bl += line
        blkWord = div_words(word_all_bl, 'n')
        return blkWord

def blankMaker(org_txt):
    blank_rate = 0.04
    forbiddenLst = []
    blankedList = []
    for item in blankSignBlkList:
        forbiddenLst.append(item)
    for item in wordsBlkList:
        forbiddenLst.append(item)
    blankNumber2 = 0
    for item in org_txt:
        if blankCheck(item):
            blankNumber2 += 1
    for txt_vocab in org_txt:
        if blankNumber2 >= blank_maximum:
            blankedList.append(txt_vocab)
            continue
        if txt_vocab.lower() in deletedWord:
            blankedList.append(txt_vocab)
            continue
        if txt_vocab.lower() in forbiddenLst:
            blankedList.append(txt_vocab)
        else:
            rdNum = random.randint(1,10000)
            if rdNum <= blank_rate*10000:
                deletedWord.append(txt_vocab.lower())
                letter_num = len(txt_vocab)
                if letter_num <= 4:
                    txt_vocab = '________'
                else:
                    txt_vocab = '________'
                    add_line = int((letter_num - 4) * 1.28)
                    counter = 0
                    while counter < add_line:
                        txt_vocab += '_'
                        counter += 1
                blankedList.append(txt_vocab)
                blankNumber2 += 1
            else:
                blankedList.append(txt_vocab)
    return blankedList

def blankCheck(stringIn):
    checkStatus = re.match(r'_+', stringIn)
    return checkStatus

with open('article.txt', 'r', encoding='utf-8') as imp_file:
    words_all = ''
    art_parag = []
    for line in imp_file.readlines():
        words_all += line
    words_div = div_words(words_all, 'y')
    words_div_copy = words_div[:]
    words_count = len(div_words(words_all, 'n'))
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
    outPutList = blankMaker(words_div)
    for item in outPutList:
        if blankCheck(item):
            blankNumber += 1
    words_div = outPutList
    print(F'Status: {str(blankNumber)} blankets has been set yet.')

#print article
outPutWord = ''
quotationMark = 1
questionNum = 1
wordNum = 0
for item in outPutList:
    if item == '(':
        outPutWord += item
    elif item == '"':
        if quotationMark == 1:
            outPutWord += item
            quotationMark = 2
        elif quotationMark == 2:
            outPutWord += F'{item} '
            quotationMark = 1
    elif item == '\n':
        if outPutList[wordNum-1] == '\n':
            wordNum += 1
            continue
        else:
            outPutWord += item
    elif blankCheck(item):
        outPutWord += F'{str(questionNum)}.{item} '
        questionNum += 1
    elif wordNum+1 < len(words_div_copy):
        if outPutList[wordNum+1] == '.':
            outPutWord += item
        elif outPutList[wordNum+1] == ',':
            outPutWord += item
        else:
            outPutWord += F'{item} '
    else:
        outPutWord += F'{item} '
    wordNum += 1

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
