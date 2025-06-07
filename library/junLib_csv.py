import os
import sys
from __init__ import *
sys.path.append(source_code_path)
from _workplace.library.junLib import *
from _workplace.library.junLib_importlib import auto_import
auto_import('pandas', 'pandas')
import csv
import pandas as pd

def convert_text_to_csv(text_file, csv_file=''):
    with open(text_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if not csv_file:
        csv_file = change_extension(text_file, 'csv')

    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
        csv_writer = csv.writer(file)
        for line in lines:
            line = line.replace('\n','').replace('\n','')
            cells = line.strip().split('\t')
            if cells[0]:
                csv_writer.writerow(cells)
    return csv_file

def convert_csv_to_txt(csv_file):
    txt_file = change_extension(csv_file, 'txt')
    # CSV 파일 읽기
    df = pd.read_csv(csv_file)

    # 탭으로 구분된 텍스트 파일로 변환하여 출력
    df.to_csv(txt_file, sep='\t', index=False)

def read_csv_and_get_rows(csv_file):
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
    return rows

def add_columns_and_vaules_for_label_file(label_file=None, lines=None, col_names=[]):
    lines = read_lines(label_file)

    new_lines = []

    if not col_names:
        new_lines.append('start\tend\ttext\tfilename')
    else:
        new_lines.append('\t'.join(col_names))
    for line in lines:
        new_lines.append(line)
    write_to_file(label_file, new_lines)
    return label_file

def add_file_name_for_label_file(label_file, folder_path, ext='mp4'):
    lines = read_lines(label_file)
    files = get_files_in_folder_via_ext(folder_path, extension=ext)
    new_lines = []
    for i, line in enumerate(lines, 0):
        # file_num = os.path.splitext(os.path.basename(str(files[i])))[0].split('_')[-1]
        # print(f"file_num: {file_num}")
        line = line.rstrip('\n') + '\t' + files[i] + '\n'
        new_lines.append(line)
    return write_to_file(label_file, new_lines)

def add_files_name_for_csv(label_file, files_path_list: list, ext='mp4'):
    lines = read_lines(label_file)
    new_lines = []
    for i, line in enumerate(lines):
        # file_num = os.path.splitext(os.path.basename(str(files[i])))[0].split('_')[-1]
        # print(f"file_num: {file_num}")
        line = line.rstrip('\n') + '\t' + os.path.basename(files_path_list[i]) + '\n'
        new_lines.append(line)
    return write_to_file(label_file, new_lines)

def add_column_names(csv_file, name_row=[]):
    rows = read_csv_and_get_rows(csv_file)
    add_values = []
    for name in name_row:
        add_values += [name]
    rows[0] = add_values + rows[0]
    return write_rows(csv_file, rows)

def add_row_numbers(csv_file):
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
        rows = list(csv.reader(file))
    rows[0] = ['num'] + rows[0]

    for i in range(1,len(rows)-1):
        rows[i] = [i] + rows[i]  # 행 번호를 첫 번째 열에 추가
    
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    return csv_file

def add_column(csv_file, column_name, index=0, values=[]):
    rows = read_csv_and_get_rows(csv_file)
    
    # 새로운 열의 이름을 index 번째 행에 추가
    rows[0].insert(index, column_name)
    add_value(csv_file, column_name, values)
    write_rows(csv_file, rows)

def add_value(csv_file, column_name, values):
    rows = read_csv_and_get_rows(csv_file)
    # 모든 행에 해당 열에 해당하는 값을 추가
    for i, row in enumerate(rows[1:], 1):
        column_index = find_column_index(csv_file, column_name)
        if column_index is not -1:
            row.insert(column_index, values[i-1])
    write_rows(csv_file, rows)

def write_rows(csv_file, rows, encoding="utf-8-sig"):
    print(rows)
    if encoding:
        with open(csv_file, 'w', newline='', encoding=encoding) as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(rows)
    else:
        with open(csv_file, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(rows)
    return csv_file

def write_rows_no_encoding(csv_file, rows):
    print(rows)
    with open(csv_file, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
    return csv_file

def find_column_index(csv_file, column_name):
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        first_row = next(reader)  # 첫 번째 행 읽기
        
        for i, column in enumerate(first_row):
            if column == column_name:
                return i + 1  # 컬럼 인덱스는 1부터 시작하므로 1을 더해 반환
    return -1  # 컬럼을 찾지 못한 경우 -1 반환


def search_value_in_csv(csv_file, search_column, search_value, target_column, type:str='str', encoding:str='utf-8-sig'):
    with open(csv_file, 'r', encoding=encoding) as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            print(f"search_col: {str(row[search_column])}\tsearch_value: {str(search_value)}")
            if not str(row[search_column]):
                continue
            if str(row[search_column]).strip():
                if type=='float':
                    if(float(row[search_column]) == float(search_value)):
                        print('find target column')
                        return row[target_column]
                elif type == 'int':
                    if(int(row[search_column]) == int(search_value)):
                        print('find target column')
                        return row[target_column]

                elif (str(row[search_column]) == str(search_value)):
                    print('find target column')
                    return row[target_column]
    return None

def remove_empty_rows(csv_file=''):
    csv_file = strip_quotes(input('Enter csv File: ')) if not csv_file else csv_file
    # CSV 파일 읽기
    rows = []
    rows = read_csv_and_get_rows(csv_file)

    # 비어있는 행 제거
    non_empty_rows = [row for row in rows if any(field.strip() for field in row)]

    # 원래 파일에 덮어쓰기
    return write_rows(csv_file, non_empty_rows)

def dict_to_csv(output_csv, data_dict, key_header, value_header, input_csv=None):
    """
    주어진 dict 값을 CSV 파일에 입력하거나 대체합니다.
    input_csv가 제공된 경우, 해당 파일을 기반으로 데이터를 업데이트합니다.

    :param output_csv: 출력할 CSV 파일의 경로
    :param data_dict: 입력할 데이터 (dict 형태)
    :param key_header: dict의 키에 해당하는 CSV header
    :param value_header: dict의 값에 해당하는 CSV header
    :param input_csv: (선택사항) 기존 CSV 파일의 경로
    """
    
    rows = []
    
    # input_csv가 제공된 경우, 해당 파일을 읽어옵니다.
    if input_csv:
        with open(input_csv, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # key_header와 value_header를 기반으로 데이터를 업데이트합니다.
                if row[key_header] in data_dict:
                    row[value_header] = data_dict[row[key_header]]
                rows.append(row)
    else:
        for key, value in data_dict.items():
            rows.append({key_header: key, value_header: value})
    
    # 결과를 CSV 파일에 입력합니다.
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=[key_header, value_header])
        csv_writer.writeheader()
        for row in rows:
            csv_writer.writerow(row)

def csv_to_list(csv_file):
    result_json_data = []
    
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            result_json_data.append(row)
    return result_json_data

def csv_to_dict(csv_file, key_column, value_column):
    """
    주어진 CSV 파일에서 두 개의 열 이름을 기반으로 dict 형태로 반환합니다.
    키 값이 중복될 경우, 가장 처음 나온 value 값만 dict에 추가합니다.

    :param csv_file: CSV 파일의 경로
    :param key_column: dict의 키로 사용될 열의 이름
    :param value_column: dict의 값으로 사용될 열의 이름
    :return: dict 형태의 결과
    """
    
    result_dict = {}
    
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            key = row[key_column]
            value = row[value_column]
            
            # 키 값이 result_dict에 이미 존재하지 않는 경우에만 추가
            if key not in result_dict:
                result_dict[key] = value
            
    return result_dict

def search_and_replace_content(csv_file, search_column, search_value, replace_value):
    """
    CSV 파일에서 주어진 열(search_column)의 값을 검색(search_value)하여 
    해당 값을 다른 값(replace_value)으로 대체합니다.

    :param csv_file: 대체 작업을 수행할 CSV 파일의 경로
    :param search_column: 값을 검색할 열의 이름
    :param search_value: 대체할 값을 검색하기 위한 기준 값
    :param replace_value: 대체할 새로운 값
    """
    
    # CSV 파일을 읽기 모드로 열기
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        # DictReader를 사용하여 CSV 파일을 읽기
        csv_reader = csv.DictReader(file)
        
        # 결과를 저장할 빈 리스트 초기화
        rows = []
        
        # CSV의 각 행을 순회
        for row in csv_reader:
            # 디버깅을 위한 출력
            print(f"search_col: {row[search_column]}\tsearch_value: {search_value}")
            
            # 현재 행의 search_column 열의 값이 search_value와 일치하는지 확인
            if (row[search_column]) == (search_value):
                # 디버깅을 위한 출력
                print((row[search_column]) == (search_value))
                
                # 일치하는 경우, 해당 값을 replace_value로 대체
                row[search_column] = replace_value
            
            # 수정된 행을 rows 리스트에 추가
            rows.append(row)
        
        # 수정된 행들을 CSV 파일에 다시 쓰기
        return write_rows(csv_file, rows)

def run():
    # 텍스트 파일과 CSV 파일 경로 설정
    text_file = strip_quotes(input('Drag and Drop text file: '))
    csv_file = strip_quotes(input('Drag and Drop csv file: '))

    # 메서드 호출하여 변환 수행
    convert_text_to_csv(text_file, csv_file)

if __name__ =="__main__":
    # run()
    remove_empty_rows()