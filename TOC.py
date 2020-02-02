from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

# Open a PDF document.
fp = open('fw9.pdf', 'rb')
password = '1111'
parser = PDFParser(fp)
document = PDFDocument(parser,password)

# Get the outlines of the document.
outlines = document.get_outlines()
for (level,title,dest,a,se) in outlines:
    print (level, title)