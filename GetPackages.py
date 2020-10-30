import os, subprocess, sys

class GetPackages:

    def __init__(self, package):
        try:
            import pip
        except ModuleNotFoundError:
            #fix this to download from pip website
            os.system('python mypip.py')
        try:
            import package
        except ModuleNotFoundError as e:
            self.intall(package)

    def intall(self, tool_name):
        subprocess.check_call([sys.executable, "-m", "pip", "install", tool_name, "--user"])

#usage sample
#check_packages = GetPackages('folium')

#pdf.load_pages()