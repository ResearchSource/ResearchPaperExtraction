import os
class FileManip:

    def get_files_by_ext(self, ext):
        extracted_files= []
        dir_files = os.listdir(os.path.dirname(os.path.realpath(__file__)))
        for file in dir_files:
            for y in range(1, 6):
                if file[-y:]==ext:
                    extracted_files.append(file)    
        return extracted_files