from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import os
import re
import sys

#주민등록번호 정규표현식 설정
p = re.compile('(?:[0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1]))-[1-4][0-9]{6}')
#pdf 파일의 내용 추출
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

#연도,월별 날짜 수 확인
def check_month_day(year, month, day):
    check = 0
    if year <= 20:
        if (year+2000)%4 == 0 & (year+2000) % 100 != 0 | (year+2000 %400 ==0):
            check = 1
    else:
        if (year+1900)%4 == 0 & (year+1900) % 100 != 0 | (year+1900 %400 ==0):
            check = 1
    if month == 1 | month == 3 | month == 5 | month == 7 | month == 8 | month == 10 | month == 12:
        if day > 31:
            return 0
    elif month == 2 & check == 1:
        if day > 29:
            return 0
    elif month == 2 & check != 1:
        if day > 28:
            return 0
    else:
        if day > 30:
            return 0
    return 1

#오류검증코드 확인
def checksum(str):
    year1 = int(str[0])
    year2 = int(str[1])
    month1 = int(str[2])
    month2 = int(str[3])
    day1 = int(str[4])
    day2 = int(str[5])
    sex = int(str[7])
    reg1 = int(str[8])
    reg2 = int(str[9])
    reg3 = int(str[10])
    reg4 = int(str[11])
    num = int(str[12])
    check = int(str[13])
    result = 11 - ((year1*2+year2*3+month1*4+month2*5+day1*6+day2*7+sex*8+reg1*9+reg2*2+reg3*3+reg4*4+num*5)%11)
    if check != result:
        return 0
    return 1

#주민번호 유효성 확인
def is_correct(str):
    year = int(str[0] + str[1])
    month = int(str[2] + str[3])
    day = int(str[4] + str[5])
    sex = int(str[7])
    reg1 = int(str[8] + str[9])
    reg2 = int(str[10] + str[11])
    num = int(str[12])
    check = int(str[13])
    if check_month_day(year, month, day) == 0:
        return 0
    if sex != 1 & sex != 2 & sex != 3 & sex != 4:
        return 0
    if year <= 20 & sex == 1 or sex == 2:
        return 0
    elif year > 20 & sex == 3 or sex == 4:
        return 0
    if reg1 > 96:
        return 0
    if num == 0:
        return 0
    if checksum(str) == 0:
        return 0
    return 1
try:
    #pdf 파일을 인자로 받아 내용 추출
    text = convert_pdf_to_txt(os.getcwd() +'\\'+ sys.argv[1])
    #내용을 ' '로 나누어 각각을 정규표현식과 매칭
    texts = text.split()
    for text in texts:
        m = p.search(text)
        if m is not None:
            str = m.group()
            if is_correct(str) == 1:
                print(m.group())
except:
    #실행 방법
    print('wrong usage....\nUSAGE -> "python3 main.py [pdf_file]"')
