import os
import openpyxl

class XlsxToTxtConverter:
    def __init__(self):
        self.xlsx_file_path = None
        self.data = None
        self.txt_file_path = None

    def convert_to_txt_file(self, xlsx_file_path):
        print(f"Converting {xlsx_file_path} to txt...")
        self.xlsx_file_path = xlsx_file_path
        self.txt_file_path = os.path.splitext(xlsx_file_path)[0] + '.txt'
        workbook = openpyxl.load_workbook(self.xlsx_file_path, data_only=True)
        sheet = workbook.active
        self.data = [str(cell.value) for row in sheet.iter_rows() for cell in row]
        with open(self.txt_file_path, 'w', encoding='utf-8') as f:
            f.writelines([sentence + '\n' for sentence in self.data])
        print(f'Successfully converted {self.xlsx_file_path} to {self.txt_file_path}')
        return self.txt_file_path


def main():
    xlsx_converter = XlsxToTxtConverter()

    # Convert xlsx to txt
    xlsx_file_path = '../resource/线上学习-关系2_1678766818257.xlsx'
    txt_file_path = xlsx_converter.convert_to_txt_file(xlsx_file_path)
    print(f"XLSX to TXT: {txt_file_path}")


if __name__ == '__main__':
    main()
