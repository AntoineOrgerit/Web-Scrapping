from bs4 import BeautifulSoup

from utils.extractor import extract

def bs_treatement(input_file, output_file):
    soup = BeautifulSoup(input_file, "html.parser")
    
    for text in soup.stripped_strings:
        if text:
            output_file.write("<p>" + text.replace("\n", " ") + "</p>\n")

def main():
    extract("../../../resources/html/", "../../../resources/BS/", bs_treatement)

if __name__ == '__main__':
    main()
