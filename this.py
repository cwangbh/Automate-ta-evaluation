import os
def pdf_to_csv(filename, separator, threshold):
    #from cStringIO import StringIO
    from pdfminer.converter import LTChar, TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage

    class CsvConverter(TextConverter):
        def __init__(self, *args, **kwargs):
            TextConverter.__init__(self, *args, **kwargs)
            self.separator = separator
            self.threshold = threshold

        def end_page(self, i):
            from collections import defaultdict
            lines = defaultdict(lambda: {})
            for child in self.cur_item._objs:  # <-- changed
                if isinstance(child, LTChar):
                    (_, _, x, y) = child.bbox
                    line = lines[int(-y)]
                    line[x] = child._text.encode(self.codec)  # <-- changed
            for y in sorted(lines.keys()):
                line = lines[y]
                self.line_creator(line)
                self.outfp.write(self.line_creator(line))
                self.outfp.write("\n")

        def line_creator(self, line):
            keys = sorted(line.keys())
            # calculate the average distange between each character on this row
            average_distance = sum([keys[i] - keys[i - 1] for i in range(1, len(keys))]) / len(keys)
            # append the first character to the result
            result = [line[keys[0]]]
            for i in range(1, len(keys)):
                # if the distance between this character and the last character is greater than the average*threshold
                if (keys[i] - keys[i - 1]) > average_distance * self.threshold:
                    # append the separator into that position
                    result.append(self.separator)
                # append the character
                result.append(line[keys[i]])
            printable_line = ''.join(result)
            return printable_line

    # ... the following part of the code is a remix of the
    # convert() function in the pdfminer/tools/pdf2text module
    rsrc = PDFResourceManager()

    ft = 'txt\\'+filename + '.txt'
    outfp = open(ft, 'w')

    #outfp = StringIO()
    device = CsvConverter(rsrc, outfp,codec="utf-8",  laparams=LAParams())
    # becuase my test documents are utf-8 (note: utf-8 is the default codec)

    fp = open(filename, 'rb')
    
    interpreter = PDFPageInterpreter(rsrc, device)
    for i, page in enumerate(PDFPage.get_pages(fp)):
        outfp.write("START PAGE %d\n" % i)
        if page is not None:
            interpreter.process_page(page)
        else:
            print 'none'
        outfp.write("END PAGE %d\n" % i)

    device.close()
    fp.close()
    outfp.close()
    #return outfp.getvalue()
    return 0


if __name__ == '__main__':
    path = 'summer\\'  # change to the folder containing the pdfs
    # the separator to use with the CSV
    separator = ';'
    # the distance multiplier after which a character is considered part of a new word/column/block. Usually 1.5 works quite well
    threshold = 1.7
    for file in os.listdir(path):
        current_file = os.path.join(path, file)
        print pdf_to_csv(current_file, separator, threshold)