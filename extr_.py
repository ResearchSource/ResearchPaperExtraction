import json, os, subprocess, sys,re
import GetPackages as get_libs
import FileManip as fileManip

#getPackages
get_libs.GetPackages('PyPDF2')
#import the packages
from PyPDF2 import PdfFileReader,PdfFileWriter

class PDFExtract:

    file_ext='pdf'
    pdf_files = []
    readers = []

    #file manipulating class declared
    fman = fileManip.FileManip()
    
    def __init__(self):

        self.citations = []
        self.pdf_files = self.fman.get_files_by_ext(self.file_ext)
        

        #Page range below parsed as command line args
        
        
        # self.result = open('result.{}'.format(sys.argv[4]), 'w')

        for pdf_file in self.pdf_files:
                self.readers.append(PdfFileReader(pdf_file, 'r'))

        self.get_contents()

        
    def get_citations(self, text):

        author = "(?:[A-Z][A-Za-z'`-]+)"
        etal = "(?:et al.?)"
        additional = "(?:,? (?:(?:and |& )?" + author + "|" + etal + "))"
        year_num = "(?:19|20)[0-9][0-9]"
        page_num = "(?:, p.? [0-9]+)?"  # Always optional
        year = "(?:, *"+year_num+page_num+"| *\("+year_num+page_num+"\))"
        regex = "(" + author + additional+"*" + year + ")"
        matches = re.findall(regex, text)
        return matches

    def cire_non_ascii(self, string):
        ''' Returns the string without non ASCII characters'''
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)

    def load_pages(self):

        self.start_page = int(sys.argv[2])
        self.end_page = int(sys.argv[3])
        
        if len(self.pdf_files)==1:
            #fileName to be saved with
            self.result = open('{}.{}'.format(self.pdf_files[0], sys.argv[4]), 'w')
            for i in range(self.start_page-1, self.end_page):
                try:
                    return self.readers[0].getPage(i).extractText().split()
                except IndexError:
                    continue
        else:
            print('Provide One PDF file at a time')


    def get_contents(self):
        
        for text in self.load_pages():
            text = self.cire_non_ascii(text)
            try:
                if sys.argv[1]=='-t':
                    self.result.write('{} '.format(text))
                elif sys.argv[1]=='-c':
                    if self.get_citations(text):
                        cited = self.get_citations(text)
                        for i in self.get_citations(text):
                            if i not in self.citations:
                                self.result.write('{} '.format(i))
                                self.citations.append(i)                  
                elif sys.argv[1]=='u':
                    pass
                else:
                    pass
            except UnicodeEncodeError:
                continue

PDFExtract()
