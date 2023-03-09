import re
import random

signBlkList = ['',' ']
blankSignBlkList = [',','.','"','\n','!','?','(',')',':',';','*','/','--']
noSpaceList = ['.',',',')','?','!','\n',':']
noSpaceList2 = ['\n','(']
fNameErrList = ['!','?','*','/','\\','|','>','<']

ProgSetting = {
    'blankMinRate': 0.100,
    'blankMaxRate': 0.125,
    'blankRate': 0.04,
    'ignoreCapital': False,
    'docxOutput': True,
    'addTitle': True,
    #do not edit items below!!!
    'NetFunc': True,
    'BlkList': True,
    'WhtList': True,
    'docxPlugin': True,
    'subtitle': False
}

try:
    import docx
except:
    ProgSetting['docxOutput'] = False

def blankCheck(stringIn):
    checkStatus = re.search(r'___+', stringIn)
    return checkStatus

def commentLDet(text):
    if re.search(r'￥<￥', text):
        return True
    else:
        return False

def commentRDet(text):
    if re.search(r'￥>￥', text):
        return True
    else:
        return False

def textClean(text):
    for item in fNameErrList:
        text = text.replace(item,'')
    return text

def cnnNameSearch(item):
    if re.match(r'[A-Z]{2}.*:', item):
        item = item.split(':')[0]
    else:
        return False
    item = re.sub(r'\(.*?\)','', item)
    if re.search(r'[a-z]', item):
        return False
    return True

def blankMaker(org_txt, forbiddenLst, blank_maximum, deletedWord, whtLst):
    commentSign = False
    blankRate = ProgSetting['blankRate']
    blankedList = []; blankNumber2 = 0
    for item in org_txt:
        if blankCheck(item):
            blankNumber2 += 1
    for word in org_txt:
        if blankNumber2 >= blank_maximum or blankCheck(word):
            pass
        elif ProgSetting['ignoreCapital'] and word.lower() != word:
            pass
        elif commentLDet(word):
            if commentRDet(word) is False:
                commentSign = True
        elif commentRDet(word):
            commentSign = False
        elif commentSign:
            pass
        elif word.lower() in forbiddenLst or word.lower() in deletedWord:
            pass
        else:
            rdNum = random.randint(1,10000)
            if word in whtLst:
                rdNum = 1
            if rdNum <= blankRate*10000:
                deletedWord.append(word.lower())
                letter_num = len(word)
                word = '________'
                add_line = int((letter_num - 4) * 1.25)
                counter = 0
                while counter < add_line:
                    word += '_'
                    counter += 1
                blankNumber2 += 1
        blankedList.append(word)
    return blankedList, deletedWord

def textCompose(outPutList, words_div_copy, articleTitle):
    outPutWord = ''; quotationMark = 1; questionNum = 1; wordNum = -1
    if articleTitle and ProgSetting['addTitle']:
        outPutWord += articleTitle + '\n'
    for item in outPutList:
        wordNum += 1
        item = item.replace('￥>￥',''); item = item.replace('￥<￥','')
        if blankCheck(item):
            outPutWord += F'{str(questionNum)}.{item}'
            questionNum += 1
        elif item == '\n' and wordNum != 0 and outPutList[wordNum-1] == '\n' or item == '':
            continue
        else:
            outPutWord += item
        if item in noSpaceList2:
            pass
        elif item == '"':
            if quotationMark == 1:
                quotationMark = 2
            else:
                quotationMark = 1; outPutWord += ' '
        elif wordNum+1 < len(words_div_copy) and outPutList[wordNum+1] in noSpaceList:
            pass
        else:
            outPutWord += ' '
    return outPutWord

def TransClean(word, articleSource):
    if articleSource.lower() == 'ted':
        if re.match(r'\d+:\d+\n', word) and len(word) == 6:
            return ''
        elif word[0] == '(' and word[-2] == ')':
            if '(' not in word[1:-2] and ')' not in word[1:-2]:
                return F'￥<￥{word[:-1]}￥>￥\n'
            else:
                return word
        else:
            return word
    elif articleSource.lower() == 'cnn':
        if word[0] == '(' and word[-2] == ')':
            if '(' not in word[1:-2] and ')' not in word[1:-2]:
                return F'￥<￥{word[:-1]}￥>￥\n'
            else:
                return word
        elif cnnNameSearch(word):
            if re.match(r'SUBTITLE:',word):
                ProgSetting['subtitle'] = True
                return '￥<￥【SUBTITLE】￥>￥\n'
            divWord = re.split(r'(:)', word)
            outWord = ''; ProgSetting['subtitle'] = False
            for numCount in range(0,len(divWord)):
                if numCount == 0:
                    outWord += F'￥<￥【{divWord[0]}】￥>￥'
                else:
                    outWord += divWord[numCount]
            return outWord
        elif ProgSetting['subtitle']:
            return '\n'
        elif word == 'END\n':
            return F'￥<￥{word}￥>￥\n'
        else:
            return word
    else:
        return word

def div_words(word_file, keep_sign):
    if keep_sign == 'n':
        #don't keep sign
        words_splited = re.split('[,|!|.|\s|\n|"|?|(|)|:|;]', word_file)
    else:
        #keep sign except space and blank
        words_splited = re.split('([,|!|.|\s|\n|"|?|(|)|:|;])', word_file)
    nCounter = 0
    while nCounter < len(words_splited):
        if words_splited[nCounter] in signBlkList:
            words_splited.pop(nCounter)
        else:
            nCounter += 1
    return words_splited

def linkSearch(textIn):
    if re.match(r'https://www\.ted\.com/talks/',textIn):
        return 'TED'
    elif re.match(r'http://www\.listeningexpress\.com/cnn10/',textIn):
        return 'CNNE'
    else:
        return 'None'
