import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *
from _workplace.library.junLib_importlib import auto_import
auto_import('pandas', 'pandas')
import pandas as pd
import csv

class CSVHelper:
    def __init__(self, worker_code=None, csv_file_path=None):
        if csv_file_path: self.set_csv_file_path(csv_file_path)
        if worker_code: self.set_worker_code(worker_code)

    def set_csv_file_path(self, csv_file_path):
        self.csv_file_path = csv_file_path
        return self

    def set_worker_code(self, worker_code:str):
        self.worker_code = worker_code
        return self

    def convert_text_to_csv(self, text_file, csv_file=None):
        csv_file = csv_file or self.change_extension(text_file, 'csv')
        with open(text_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
            csv_writer = csv.writer(file)
            for line in lines:
                line = line.replace('\n','').replace('\n','')
                cells = line.strip().split('\t')
                if cells[0]:
                    csv_writer.writerow(cells)
        return csv_file

    def convert_csv_to_txt(self, csv_file=None):
        csv_file = self.csv_file_path or csv_file
        if not csv_file:
            print("convert_csv_to_txt엔 csv_file 인자가 필요합니다.")
            return
        elif not path_exist(csv_file):
            print("csv_file 경로에 파일이 없습니다.")
            return

        txt_file = self.change_extension(csv_file, 'txt')
        # CSV 파일 읽기
        df = pd.read_csv(csv_file)

        # 탭으로 구분된 텍스트 파일로 변환하여 출력
        df.to_csv(txt_file, sep='\t', index=False)

    def read_csv_and_get_rows(self, csv_file):
        with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
        return rows

    def add_columns_and_values_for_csv(self, label_file=None, lines=None, col_names=[]):
        lines = self.read_lines(label_file)

        new_lines = []

        if not col_names:
            new_lines.append('start\tend\ttext\tfilename')
        else:
            new_lines.append('\t'.join(col_names))
        for line in lines:
            new_lines.append(line)
        self.write_to_file(label_file, new_lines)
        return label_file

    def write_to_file(self, file_path, lines:list):
        with open(file_path, 'w', encoding='utf-8-sig') as file:
            for line in lines:
                file.write(line + '\n')

    def change_extension(self, file_path, new_extension):
        base_name, _ = os.path.splitext(file_path)
        return base_name + '.' + new_extension

    def add_values_to_column(self, csv_file, column_name, values):
        """
        지정된 CSV 파일의 특정 컬럼(column_name)에 값을 추가합니다.
        
        :param csv_file: 값을 추가할 CSV 파일의 경로
        :param column_name: 값을 추가할 컬럼의 이름
        :param values: 추가할 값들의 리스트
        """
        rows = self.read_csv_and_get_rows(csv_file)
        
        # 컬럼 인덱스를 찾기 위해 컬럼 이름을 사용합니다.
        column_index = self.find_column_index(csv_file, column_name)
        
        if column_index != -1:
            # 컬럼 인덱스가 유효한 경우에만 값을 추가합니다.
            for i, value in enumerate(values):
                if i < len(rows):
                    rows[i][column_index] = value
                else:
                    rows.append([])
                    for j in range(1, column_index):
                        if j < column_index:
                            rows[i].insert(j, '')
                        else:
                            rows[i].insert(column_index, value)
                            break
        
        self.write_rows(csv_file, rows)

    def count_non_empty_cells(self, search_column, search_value, csv_file=None) -> int:
        """
        특정 열(search_column)의 특정 값(search_value)을 검색하여 해당 값의 행에서 값이 있는 셀의 개수를 반환합니다.
        검색한 열에 대한 개수는 제외합니다.

        :param csv_file: CSV 파일의 경로
        :param search_column: 검색할 열의 이름
        :param search_value: 검색할 값
        :return: 값이 있는 셀의 개수 (검색한 열 제외)
        """
        csv_file = csv_file or self.csv_file_path
        rows = self.read_csv_and_get_rows(csv_file)

        # search_column의 인덱스를 찾습니다.
        col_index_search = self.find_column_index(csv_file, search_column)
        print("col_index:\t",col_index_search)
        if col_index_search == -1:
            # 만약 해당 열이 존재하지 않는다면 None을 반환합니다.
            print(col_index_search)
            return 0

        for row in rows:
            print("/",row[col_index_search], "/\t/", search_value, "/")
            if row[col_index_search] == search_value:
                # search_value 값이 있는 행을 찾았습니다.
                # 해당 행에서 값이 있는 셀의 개수를 계산하고, search_column에 대한 개수를 제외합니다.
                non_empty_cells_count = sum(1 for cell in row if cell) - 1
                print("count ",non_empty_cells_count)
                return non_empty_cells_count
            else:
                continue
        # 해당 값을 찾지 못한 경우 None을 반환합니다.
        print("count:", 0)
        return 0

    def get_or_set_value(self, search_column, search_value, target_column, replacement_value=None, csv_file=None):
        """
        특정 열(search_column)의 특정 값(search_value)을 검색하여 해당 값의 행 중 특정 열(target_column)의 값을 반환합니다.
        만약 해당 값이 없다면 False, 있다면 그 값 반환
        만약 replacement_value 값이 있다면 그 값을 해당 위치에 대입 후 이전 값 존재 여부 반환

        :param search_column: 검색할 열의 이름
        :param search_value: 검색할 값
        :param target_column: 값을 반환할 열의 이름
        :param replacement_value: 대입할 값 (optional)
        :param csv_file: CSV 파일의 경로 (optional)
            - 인자가 있다면 인자를, 인자가 없다면 self.csv_file_path 값으로 대신함.
        :return: target_column 열의 값 또는 False 또는 None
        """
        csv_file = csv_file or self.csv_file_path
        if not csv_file:
            print("csv_file_path is None")
            return None
        rows = self.read_csv_and_get_rows(csv_file)

        # search_column과 target_column의 인덱스를 찾습니다.
        col_index_search = self.find_column_index(csv_file, search_column)
        # print("col_index search\t", col_index_search)
        col_index_target = self.find_column_index(csv_file, target_column)
        # print("col_index target\t", col_index_target)

        if col_index_search == -1 or col_index_target == -1:
            # 만약 해당 열이 존재하지 않는다면 None을 반환합니다.
            print("Not exist.")
            return None

        for row in rows:
            if str(row[col_index_search]).strip() == str(search_value).strip():
                # search_value 값이 있는 행을 찾았습니다.
                if not row[col_index_target]:
                    # target_column 열의 값이 없고, replacement_value 값이 주어진 경우 replacement_value 값을 대입합니다.
                    if replacement_value:
                        row[col_index_target] = replacement_value
                        self.write_rows(csv_file, rows)
                    return False
                else:
                    if replacement_value:
                        row[col_index_target] = replacement_value
                        self.write_rows(csv_file, rows)
                    return row[col_index_target]

        # 해당 값을 찾지 못한 경우 None을 반환합니다.
        print("Can't find.")
        return None


    def find_column_index(self, csv_file, column_name):
        with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            first_row = next(reader)  # 첫 번째 행 읽기
            
            for i, column in enumerate(first_row):# 컬럼 인덱스는 1부터 시작?
                if column == column_name:
                    return i
        return -1  # 컬럼을 찾지 못한 경우 -1 반환    

    def write_rows(self, csv_file, rows):
        """
        주어진 행들(rows)을 지정된 CSV 파일에 씁니다.

        :param csv_file: CSV 파일의 경로
        :param rows: 쓸 행들의 리스트
        """
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(rows)

if __name__ == "__main__":
    csv_helper = CSVHelper()
    # 클래스 인스턴스를 생성

    # 사용 예시:
    text_file = 'input.txt'
    csv_file = 'output.csv'

    csv_helper.convert_text_to_csv(text_file, csv_file)
    csv_helper.convert_csv_to_txt(csv_file)
    # 필요한 메서드 호출
