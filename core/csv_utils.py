"""
CSV 파일 처리를 위한 유틸리티 함수들
"""
import os
import sys
import pandas as pd
import csv
from typing import List, Dict, Optional, Union
from junLib import path_exist

def get_csv_file_path(csv_file: str) -> str:
    """
    CSV 파일의 경로를 반환합니다.
    """
    if not path_exist(csv_file):
        csv_file = os.path.join(os.path.dirname(__file__), csv_file)
    return csv_file

def read_csv_and_get_rows(csv_file: str, encoding: str = 'utf-8-sig') -> List[List[str]]:
    """
    CSV 파일을 읽어서 행들의 리스트를 반환합니다.
    
    Args:
        csv_file (str): 읽을 CSV 파일의 경로
        encoding (str): 파일 인코딩
        
    Returns:
        List[List[str]]: CSV 파일의 행들의 리스트
    """
    with open(csv_file, 'r', newline='', encoding=encoding) as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
    return rows

def write_rows(csv_file: str, rows: List[List[str]], encoding: str = 'utf-8-sig') -> str:
    """
    행들의 리스트를 CSV 파일로 저장합니다.
    
    Args:
        csv_file (str): 저장할 CSV 파일의 경로
        rows (List[List[str]]): 저장할 행들의 리스트
        encoding (str): 파일 인코딩
        
    Returns:
        str: 저장된 파일의 경로
    """
    with open(csv_file, 'w', newline='', encoding=encoding) as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
    return csv_file

def find_column_index(csv_file: str, column_name: str) -> int:
    """
    CSV 파일에서 특정 열의 인덱스를 찾습니다.
    
    Args:
        csv_file (str): CSV 파일의 경로
        column_name (str): 찾을 열의 이름
        
    Returns:
        int: 열의 인덱스 (1부터 시작), 찾지 못한 경우 -1
    """
    with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        first_row = next(reader)
        
        for i, column in enumerate(first_row):
            if column == column_name:
                return i + 1
    return -1

def add_column_names(csv_file: str, name_row: List[str]) -> str:
    """
    CSV 파일에 열 이름을 추가합니다.
    
    Args:
        csv_file (str): CSV 파일의 경로
        name_row (List[str]): 추가할 열 이름들의 리스트
        
    Returns:
        str: 수정된 파일의 경로
    """
    rows = read_csv_and_get_rows(csv_file)
    rows[0] = name_row + rows[0]
    return write_rows(csv_file, rows)

def add_row_numbers(csv_file: str) -> str:
    """
    CSV 파일의 각 행에 번호를 추가합니다.
    
    Args:
        csv_file (str): CSV 파일의 경로
        
    Returns:
        str: 수정된 파일의 경로
    """
    rows = read_csv_and_get_rows(csv_file)
    rows[0] = ['num'] + rows[0]
    
    for i in range(1, len(rows)):
        rows[i] = [i] + rows[i]
    
    return write_rows(csv_file, rows)

def dict_to_csv(output_csv: str, data_dict: Dict, key_header: str, value_header: str, 
                input_csv: Optional[str] = None) -> None:
    """
    딕셔너리 데이터를 CSV 파일로 저장합니다.
    
    Args:
        output_csv (str): 출력할 CSV 파일의 경로
        data_dict (Dict): 저장할 데이터 딕셔너리
        key_header (str): 키에 해당하는 열 이름
        value_header (str): 값에 해당하는 열 이름
        input_csv (str, optional): 기존 CSV 파일의 경로
    """
    rows = []
    
    if input_csv:
        with open(input_csv, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row[key_header] in data_dict:
                    row[value_header] = data_dict[row[key_header]]
                rows.append(row)
    else:
        for key, value in data_dict.items():
            rows.append({key_header: key, value_header: value})
    
    with open(output_csv, 'w', encoding='utf-8-sig', newline='') as file:
        csv_writer = csv.DictWriter(file, fieldnames=[key_header, value_header])
        csv_writer.writeheader()
        for row in rows:
            csv_writer.writerow(row)

def search_and_replace_content(csv_file: str, search_column: str, search_value: str, 
                             replace_value: str) -> None:
    """
    CSV 파일에서 특정 값을 검색하여 다른 값으로 대체합니다.
    
    Args:
        csv_file (str): CSV 파일의 경로
        search_column (str): 검색할 열의 이름
        search_value (str): 검색할 값
        replace_value (str): 대체할 값
    """
    rows = read_csv_and_get_rows(csv_file)
    header = rows[0]
    search_index = header.index(search_column)
    
    for row in rows[1:]:
        if row[search_index] == search_value:
            row[search_index] = replace_value
    
    write_rows(csv_file, rows)

def convert_text_to_csv(text_file: str, csv_file: Optional[str] = None) -> str:
    """
    텍스트 파일을 CSV 파일로 변환합니다.
    
    Args:
        text_file (str): 변환할 텍스트 파일의 경로
        csv_file (str, optional): 저장할 CSV 파일의 경로
        
    Returns:
        str: 저장된 CSV 파일의 경로
    """
    if not csv_file:
        csv_file = os.path.splitext(text_file)[0] + '.csv'

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

def convert_csv_to_text(csv_file: str) -> str:
    """
    CSV 파일을 텍스트 파일로 변환합니다.
    
    Args:
        csv_file (str): 변환할 CSV 파일의 경로
        
    Returns:
        str: 저장된 텍스트 파일의 경로
    """
    txt_file = os.path.splitext(csv_file)[0] + '.txt'
    df = pd.read_csv(csv_file)
    df.to_csv(txt_file, sep='\t', index=False)
    return txt_file

def remove_empty_rows(csv_file: str) -> str:
    """
    CSV 파일에서 비어있는 행을 제거합니다.
    
    Args:
        csv_file (str): CSV 파일의 경로
        
    Returns:
        str: 수정된 파일의 경로
    """
    rows = read_csv_and_get_rows(csv_file)
    non_empty_rows = [row for row in rows if any(field.strip() for field in row)]
    return write_rows(csv_file, non_empty_rows)

def csv_to_list(csv_file: str) -> List[Dict]:
    """
    CSV 파일을 리스트로 변환합니다.
    
    Args:
        csv_file (str): CSV 파일의 경로
        
    Returns:
        List[Dict]: 변환된 리스트
    """
    result_json_data = []
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            result_json_data.append(row)
    return result_json_data

def csv_to_dict(csv_file: str, key_column: str, value_column: str) -> Dict:
    """
    CSV 파일을 딕셔너리로 변환합니다.
    
    Args:
        csv_file (str): CSV 파일의 경로
        key_column (str): 키로 사용할 열의 이름
        value_column (str): 값으로 사용할 열의 이름
        
    Returns:
        Dict: 변환된 딕셔너리
    """
    result_dict = {}
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            key = row[key_column]
            value = row[value_column]
            if key not in result_dict:
                result_dict[key] = value
    return result_dict

if __name__ == "__main__":
    # 테스트용 CSV 파일 생성
    test_data = [
        ['name', 'age', 'city'],
        ['John', '30', 'New York'],
        ['Alice', '25', 'London'],
        ['Bob', '35', 'Paris']
    ]
    
    # 테스트 파일 경로
    test_csv = 'test.csv'
    
    # CSV 파일 생성
    write_rows(test_csv, test_data)
    print(f"테스트 CSV 파일이 생성되었습니다: {test_csv}")
    
    # 각 함수 테스트
    print("\n1. 열 인덱스 찾기 테스트:")
    name_index = find_column_index(test_csv, 'name')
    print(f"'name' 열의 인덱스: {name_index}")
    
    print("\n2. 행 번호 추가 테스트:")
    add_row_numbers(test_csv)
    print("행 번호가 추가되었습니다.")
    
    print("\n3. CSV를 딕셔너리로 변환 테스트:")
    result_dict = csv_to_dict(test_csv, 'name', 'city')
    print(f"변환된 딕셔너리: {result_dict}")
    
    print("\n4. CSV를 리스트로 변환 테스트:")
    result_list = csv_to_list(test_csv)
    print(f"변환된 리스트: {result_list}")
    
    print("\n5. 내용 검색 및 대체 테스트:")
    search_and_replace_content(test_csv, 'city', 'London', 'Berlin')
    print("'London'이 'Berlin'으로 변경되었습니다.")
    
    # 테스트 파일 삭제
    os.remove(test_csv)
    print(f"\n테스트 CSV 파일이 삭제되었습니다: {test_csv}")
