# file_utils.py 리팩토링 계획

## 1. 모듈 분리 계획

현재의 `file_utils.py`를 다음과 같은 구조로 분리하여 각 모듈의 책임을 명확히 합니다.

```
core/
├── utils/
│   ├── __init__.py
│   ├── file_utils.py      # 파일 기본 작업
│   ├── folder_utils.py    # 폴더 관련 작업
│   ├── path_utils.py      # 경로 관련 작업
│   ├── io_utils.py        # 파일 입출력 작업
│   ├── search_utils.py    # 검색 관련 작업
│   └── text_utils.py      # 텍스트 처리 작업
```

## 2. 각 모듈별 주요 함수 분배

### file_utils.py (파일 기본 작업)
- move_file()
- copy_file()
- delete_file()
- rename_file()
- rename_and_move_file()
- move_with_backup()
- copy_and_rename_file()

### folder_utils.py (폴더 관련 작업)
- create_folder()
- remove_empty_folders()
- move_folder_structure()
- is_empty_folder()
- move_folder()
- delete_folders_by_name()
- create_folders()
- lift_folders()
- move_files_up()
- move_files_to_parent_folder()

### path_utils.py (경로 관련 작업)
- join_folder_path()
- basename()
- parent_path()
- split_filename()
- path_exist()
- change_extension()
- add_suffix()
- get_suffix()
- except_ext_filename()
- bro_folder_path()

### io_utils.py (파일 입출력 작업)
- read_lines()
- write_to_file()
- write_to_xmlfile()
- get_size_in_kb()
- get_size_in_mb()
- get_files_info()

### search_utils.py (검색 관련 작업)
- get_files_path_in_folder_via_ext()
- get_files_path_in_folder_via_ext_yield()
- get_files_path_in_folder_via_startwith()
- get_files_path_in_folder_via_endswith()
- get_files_path_in_folder_via_contain()
- get_files_path_at_all()
- find_files_with_extension()
- get_specific_sub_folder_path()
- get_specific_sub_folder_paths()
- get_matching_sub_folder_paths()
- get_startwith_sub_folder_path()

### text_utils.py (텍스트 처리 작업)
- convert_to_korean_numbers()
- change_encoding()
- format_time()
- strip_quotes()
- seconds_to_hms()
- seconds_to_ms()

## 3. 리팩토링 단계

1. **준비 단계**
   - utils 폴더 생성
   - 각 모듈 파일 생성
   - `__init__.py` 작성

2. **코드 이전**
   - 각 함수를 해당하는 모듈로 이동
   - 의존성 관계 정리
   - import 문 수정

3. **의존성 관리**
   - 순환 참조 방지
   - 필요한 함수만 import
   - `__init__.py`에서 주요 함수 export

4. **문서화**
   - 각 모듈의 docstring 작성
   - 함수별 상세 문서화
   - 예제 코드 추가

5. **테스트**
   - 각 모듈별 단위 테스트 작성
   - 통합 테스트 수행
   - 기존 코드와의 호환성 검증

## 4. 코드 예시

```python
# path_utils.py
def join_folder_path(*args):
    """경로들을 결합합니다."""
    return str(os.path.join(*args))

# file_utils.py
from .path_utils import join_folder_path, basename

def move_file(source, target, show_msg=False):
    """파일을 이동합니다."""
    if os.path.isdir(target):
        target = join_folder_path(target, basename(source))
    # ... 구현

# folder_utils.py
from .path_utils import path_exist, join_folder_path

def create_folder(folder_path, show_msg=True):
    """폴더를 생성합니다."""
    if not path_exist(folder_path):
        os.makedirs(folder_path)
        if show_msg:
            print(f"폴더를 생성했습니다: {folder_path}")
```

## 5. 기대 효과

1. **코드 구조 개선**
   - 각 모듈의 책임이 명확해짐
   - 코드 가독성 향상
   - 유지보수 용이성 증가

2. **확장성**
   - 새로운 기능 추가가 용이
   - 모듈별 독립적인 버전 관리 가능

3. **재사용성**
   - 필요한 기능만 선택적으로 import 가능
   - 다른 프로젝트에서도 재사용 용이

4. **테스트 용이성**
   - 모듈별 단위 테스트 작성 가능
   - 테스트 커버리지 향상

## 6. 주의사항

1. **하위 호환성 유지**
   - 기존 코드에서 사용중인 함수들의 인터페이스 유지
   - 필요한 경우 deprecation 경고 추가

2. **문서화**
   - 모든 변경사항 문서화
   - 사용 예제 추가
   - 마이그레이션 가이드 작성

3. **점진적 적용**
   - 한 번에 모든 변경을 적용하지 않고 단계적으로 진행
   - 각 단계별로 테스트 수행 