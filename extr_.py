import json, os, subprocess, sys,re
from PyPDF2 import PdfFileReader, PdfFileWriter

"""
    USAGE 
    1. Ensure You have only the pdf file you want to extract in the folder
    2. 

"""


class CheckPackages:
    packages = [
        'PyPDF2'
    ]
    def __init__(self):

        try:
            import pip
        except ModuleNotFoundError:
            os.system('python mypip.py')

        for package in self.packages:
            try:
                import package
            except ModuleNotFoundError as e:
                self.intall_libry(package)

    def intall_libry(self, tool_name):
        subprocess.check_call([sys.executable, "-m", "pip", "install", tool_name])

    # make inport for the next class
    from PyPDF2 import PdfFileReader, PdfFileWriter


class PDFExtract:

    # packages = [
    #     'PyPDF2'
    # ]
    file_ext=''
    pdf_files = []
    readers = []
    

    def __init__(self, file_ext):

        packa = CheckPackages()
        #self.dump_ext = dump_ext
        self.file_ext = file_ext
        self.pdf_files = self.get_files_by_ext()
        self.citations = []

        #Page range below parsed as command line args
        self.start_page = int(sys.argv[2])
        self.end_page = int(sys.argv[3])
        self.result = open('result.{}'.format(sys.argv[4]), 'w')

        for pdf_file in self.pdf_files:
                self.readers.append(PdfFileReader(pdf_file, 'r'))

        # Check wether pip is installed else install mypip.py
        # try:
        #     import pip
        # except ModuleNotFoundError:
        #     os.system('python mypip.py')

        # iterate through the packages and install the ones not installed
        # reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        # installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

        # for package in self.packages:
        #     try:
        #         import package
        #     except ModuleNotFoundError as e:
        #         self.intall_libry(package)
                


    # Call the below method only once   
    # def intall_libry(self, tool_name):
    #     subprocess.check_call([sys.executable, "-m", "pip", "install", tool_name])

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

    def get_files_by_ext(self):
        extracted_files= []
        dir_files = os.listdir(os.path.dirname(os.path.realpath(__file__)))
        for file in dir_files:
            for y in range(1, 6):
                if file[-y:]==self.file_ext:
                    extracted_files.append(file)    
        return extracted_files

    def load_pages(self):
        
        if len(self.pdf_files)==1:
            for i in range(self.start_page-1, self.end_page):
                try:
                    pageText = self.readers[0].getPage(i).extractText().split()
                    
                    for text in pageText:
                        text = self.cire_non_ascii(text)
                        try:
                            if sys.argv[1]=='-t':
                                self.result.write('{}\n'.format(text))
                            elif sys.argv[1]=='-c':
                                if self.get_citations(text):
                                    cited = self.get_citations(text)
                                    
                                    for i in cited:
                                        if i not in self.citations:
                                            self.result.write('{}\n'.format(i))
                                            self.citations.append(i)
                                        
                            elif sys.argv[1]=='u':
                                pass
                            else:
                                pass

                                #print(self.get_citations(text))
                        except UnicodeEncodeError:
                            continue
                except IndexError:
                    continue
            #print(self.citations)
            self.citations =[]
        else:
            print('Provide One PDF file at a time')

pdf = PDFExtract('pdf')
pdf.load_pages()