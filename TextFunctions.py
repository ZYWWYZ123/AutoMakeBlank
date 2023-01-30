import re
import random

signBlkList = ['',' ']
blankSignBlkList = [',','.','"','\n','!','?','(',')',':',';','*','/','--']
noSpaceList = ['.',',',')','?','!','\n']
fNameErrList = ['!','?','*','/','\\','|','>','<']

ProgSetting = {
    'blankMinRate': 0.100,
    'blankMaxRate': 0.125,
    'blankRate': 0.04,
    'ignoreCapital': False,
    'docxOutput': True,
    #do not edit items below!!!
    'NetFunc': True,
    'BlkList': True,
    'WhtList': True,
    'docxPlugin': True,
}

try:
    import docx
except:
    ProgSetting['docxOutput'] = False

def blankCheck(stringIn):
    checkStatus = re.search(r'___+', stringIn)
    return checkStatus

def blankMaker(org_txt, forbiddenLst, blank_maximum, deletedWord, whtLst):
    commentSign = False
    blankRate = ProgSetting['blankRate']
    blankedList = []
    blankNumber2 = 0
    for item in org_txt:
        if blankCheck(item):
            blankNumber2 += 1
    for txt_vocab in org_txt:
        if blankNumber2 >= blank_maximum:
            blankedList.append(txt_vocab)
        elif txt_vocab.lower() != txt_vocab and ProgSetting['ignoreCapital']:
            blankedList.append(txt_vocab)
        elif commentLDet(txt_vocab):
            if commentRDet(txt_vocab):
                blankedList.append(txt_vocab)
            else:
                commentSign = True
                blankedList.append(txt_vocab)
        elif commentRDet(txt_vocab):
            commentSign = False
            blankedList.append(txt_vocab)
        elif commentSign:
            blankedList.append(txt_vocab)
        elif txt_vocab.lower() in forbiddenLst or txt_vocab.lower() in deletedWord:
            blankedList.append(txt_vocab)
        else:
            rdNum = random.randint(1,10000)
            if txt_vocab in whtLst:
                rdNum = 1
            if rdNum <= blankRate*10000:
                deletedWord.append(txt_vocab.lower())
                letter_num = len(txt_vocab)
                txt_vocab = '________'
                add_line = int((letter_num - 4) * 1.25)
                counter = 0
                while counter < add_line:
                    txt_vocab += '_'
                    counter += 1
                blankNumber2 += 1
            blankedList.append(txt_vocab)
    return blankedList, deletedWord

def textCompose(outPutList, words_div_copy):
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
                pass
            else:
                outPutWord += item
        elif blankCheck(item):
            outPutWord += F'{str(questionNum)}.{item} '
            questionNum += 1
        elif commentLDet(item):
            if commentRDet(item):
                outPutWord += item[3:re.search(r'￥>￥', item).span()[0]]
                outPutWord += item[re.search(r'￥>￥', item).span()[1]:]
            else:
                outPutWord += item[3:]
        elif commentRDet(item):
            outPutWord += item[:re.search(r'￥>￥', item).span()[0]]
            outPutWord += item[re.search(r'￥>￥', item).span()[1]:]
        elif wordNum+1 < len(words_div_copy) and outPutList[wordNum+1] in noSpaceList:
            outPutWord += item
        else:
            outPutWord += F'{item} '
        wordNum += 1
    return outPutWord

def TransClean(ckWord, articleSource):
    if articleSource.lower() == 'ted':
        if re.match(r'\d+:\d+\n', ckWord) and len(ckWord) == 6:
            return ''
        elif ckWord[0] == '(' and ckWord[-2] == ')':
            if '(' not in ckWord[1:-2] and ')' not in ckWord[1:-2]:
                return F'￥<￥{ckWord[:-1]}￥>￥\n'
            else:
                return ckWord
        else:
            return ckWord
    elif articleSource.lower() == 'cnn':
        subti = False
        if ckWord[0] == '(' and ckWord[-2] == ')':
            if '(' not in ckWord[1:-2] and ')' not in ckWord[1:-2]:
                return F'￥<￥{ckWord[:-1]}￥>￥\n'
            else:
                return ckWord
        elif re.match(r'[A-Z]{3}.*:', ckWord):
            if re.match(r'SUBTITLE:',ckWord):
                subti == True
                return ''
            divWord = re.split(r'(:)', ckWord)
            outWord = ''; subti = False
            for numCount in range(0,len(divWord)):
                if numCount == 0:
                    outWord += F'￥<￥【{divWord[0]}】￥>￥'
                else:
                    outWord += divWord[numCount]
            return outWord
        elif subti:
            return ''
        elif ckWord == 'END\n':
            return F'￥<￥{ckWord}￥>￥\n'
        else:
            return ckWord
    else:
        return ckWord

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

def languageDetect():
    return 0

def linkSearch(textIn):
    if re.match(r'https://www\.ted\.com/talks/',textIn):
        print('Found a TED link! The page will be opened in a browser. Follow instructions in the program window.')
        return 'TED'
    elif re.match(r'http://www\.listeningexpress\.com/cnn10/',textIn):
        print('Found a CNN (listeningexpress.com) link. Text will be processed automatically.')
        return 'CNNE'
    else:
        return 'None'

def textClean(text):
    returnText = ''
    for letter in text:
        if letter in fNameErrList:
            pass
        else:
            returnText += letter
    return returnText
