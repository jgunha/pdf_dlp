#pdf DLP
import PyPDF2
import os

file = open("test1.pdf", 'rb')
fileReader = PyPDF2.PdfFileReader(file)
numberPages = fileReader.getNumPages()
print(fileReader.numPages)
pageObj = fileReader.getPage(0)
text = pageObj.extractText()
print(text)
#주민번호 정규표현식
#^(?:[0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1]))-[1-4][0-9]{6}$