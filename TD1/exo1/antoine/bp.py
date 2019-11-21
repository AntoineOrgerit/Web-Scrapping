from boilerpipe.extract import Extractor

from utils.extractor import extract

def bp_treatement(input_file, output_file):
    if input_file.read():
        input_file.seek(0)
        extractor = Extractor(extractor="ArticleExtractor", html=input_file.read())
        output_file.write(extractor.getHTML())
    else:
        output_file.write(" ")


def main():
    extract("../../../../resources/html/", "../../../../resources/BP/", bp_treatement)

if __name__ == '__main__':
    main()
