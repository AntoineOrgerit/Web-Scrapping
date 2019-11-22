import justext
from utils.extractor import extract

def jt_treatement(input_file, output_file):
    paragraphs = justext.justext(input_file.read(), justext.get_stoplist('English'))
    
    for paragraph in paragraphs:
        output_file.write("<p>" + paragraph.text.replace("\n", " ") + "</p>\n")

def main():
    extract("../../../resources/html/", "../../../resources/JT/", jt_treatement)

if __name__ == '__main__':
    main()