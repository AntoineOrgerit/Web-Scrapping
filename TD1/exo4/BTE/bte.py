from utils.bte import html2text
from utils.extractor import extract

def bte_treatement(input_file, output_file):
    text = html2text(input_file.read())
    
    output_file.write("<p>" + text.replace("\n", " ") + "</p>\n")


def main():
    extract("../../../resources/html/", "../../../resources/BTE/", bte_treatement)

if __name__ == '__main__':
    main()
