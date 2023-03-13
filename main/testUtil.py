from util.xlsx2text import XlsxToTxtConverter

def testxlsx2text(xlsx_path):
    conv = XlsxToTxtConverter()
    conv.convert_to_txt_file(xlsx_path)
    
    
if __name__ == '__main__':
    xlsx_path = 'resource/aaa.xlsx'
    testxlsx2text(xlsx_path)