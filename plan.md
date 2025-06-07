# junLib 리팩토링 계획

## 1. 현재 구조 분석

### 1.1 중복/유사 기능 그룹
- XML 관련: `junLib_xml.py`, `junLib_xml_class.py`, `junLib_xml_class_json.py`, `junLib_xsd.py`, `junLib_xsd_json.py`
- CSV 관련: `junLib_csv.py`, `junLib_csv_class.py`
- 비디오 관련: `junLib_video.py`, `junLib_video_player.py`
- 파일 시스템: `junLib.py`의 파일 관련 함수들
- 유틸리티: `junLib_datetime.py`, `junLib_pickle.py`

### 1.2 현재 문제점
- 기능 중복
- 일관성 없는 구조 (일부는 클래스, 일부는 함수)
- 파일 간 의존성 복잡
- 유지보수 어려움
- 테스트 작성 어려움

## 2. 리팩토링 옵션

### 2.1 옵션 1: 단일 패키지 구조
```
junLib/
├── library/
│   ├── __init__.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── xml_handler.py      # XML, XSD 관련 모든 기능
│   │   ├── csv_handler.py      # CSV 관련 모든 기능
│   │   ├── video_handler.py    # 비디오 관련 모든 기능
│   │   └── file_handler.py     # 파일 시스템 관련 기능
│   └── utils/
│       ├── __init__.py
│       ├── datetime_utils.py   # 날짜/시간 관련 유틸리티
│       └── common_utils.py     # 공통 유틸리티 함수들
```

장점:
- 기능별 명확한 구분
- 확장성이 좋음
- 모듈화가 잘 됨
- 패키지 관리가 용이

단점:
- 임포트 경로가 길어짐
- 패키지 구조가 복잡해질 수 있음

### 2.2 옵션 2: 서브패키지 구조
```
junLib/
├── library/
│   ├── __init__.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── xml/
│   │   │   ├── __init__.py
│   │   │   ├── handler.py
│   │   │   └── validator.py
│   │   ├── csv/
│   │   │   ├── __init__.py
│   │   │   └── handler.py
│   │   ├── video/
│   │   │   ├── __init__.py
│   │   │   ├── handler.py
│   │   │   └── player.py
│   │   └── file/
│   │       ├── __init__.py
│   │       └── handler.py
│   └── utils/
│       ├── __init__.py
│       ├── datetime/
│       │   ├── __init__.py
│       │   └── utils.py
│       └── common/
│           ├── __init__.py
│           └── utils.py
```

장점:
- 더 세분화된 기능 구분
- 각 기능별 독립적인 확장 가능
- 테스트 작성이 용이

단점:
- 구조가 매우 복잡해짐
- 임포트 경로가 매우 길어짐
- 초기 설정이 복잡

### 2.3 옵션 3: 기능별 폴더 구조 + 네임스페이스 패키지
```
junLib/
├── __init__.py              # 모든 핵심 클래스/함수를 여기서 임포트
├── xml/
│   ├── __init__.py
│   ├── XMLHandler.py       # XML 핸들러 클래스
│   ├── XMLValidator.py     # XML 검증 클래스
│   └── utils.py            # XML 관련 유틸리티
├── csv/
│   ├── __init__.py
│   ├── CSVHandler.py       # CSV 핸들러 클래스
│   └── utils.py            # CSV 관련 유틸리티
├── video/
│   ├── __init__.py
│   ├── VideoHandler.py     # 비디오 핸들러 클래스
│   ├── AudioHandler.py     # 오디오 핸들러 클래스
│   └── utils.py            # 비디오 관련 유틸리티
├── file/
│   ├── __init__.py
│   ├── FileHandler.py      # 파일 핸들러 클래스
│   └── utils.py            # 파일 관련 유틸리티
└── utils/
    ├── __init__.py
    ├── datetime.py         # 날짜/시간 관련 유틸리티
    └── common.py           # 공통 유틸리티 함수들
```

장점:
- 기능별로 명확한 구분
- 각 기능의 관련 코드가 한 폴더에 모여있어 관리가 용이
- 간단한 임포트 구조 (`from junLib import XMLHandler`)
- 확장성이 좋음 (각 기능 폴더 내에서 자유롭게 파일 추가 가능)
- 불필요한 중첩 폴더 제거로 구조가 더 단순해짐

단점:
- 파일 구조가 약간 복잡해짐
- 각 기능 폴더의 `__init__.py` 관리 필요

## 3. 권장 방향

### 3.1 단기 계획
1. 옵션 3(기능별 폴더 구조)로 전환
   - 가장 사용자 친화적인 구조
   - 간단한 임포트 방식
   - 빠른 개발 가능

### 3.2 장기 계획
1. 각 모듈에 대한 테스트 코드 작성
2. 문서화 개선
3. 타입 힌트 추가
4. 필요에 따라 옵션 1이나 2로 전환 검토

## 4. 구체적인 마이그레이션 단계

### 4.1 1단계: 기본 구조 설정
1. 새로운 파일 구조 생성
2. `__init__.py`에 모든 핵심 클래스/함수 임포트 추가
3. 각 모듈 파일 생성

### 4.2 2단계: 코드 이전
1. XML 관련 코드 통합
2. CSV 관련 코드 통합
3. 비디오 관련 코드 통합
4. 파일 시스템 관련 코드 통합
5. 유틸리티 함수 이전

### 4.3 3단계: 테스트 및 검증
1. 각 모듈에 대한 단위 테스트 작성
2. 기존 기능과의 호환성 검증
3. 성능 테스트

### 4.4 4단계: 문서화 및 배포
1. README 업데이트
2. API 문서 작성
3. 예제 코드 작성
4. PyPI 배포 준비

## 5. 주의사항
- 기존 코드의 기능을 유지하면서 점진적으로 이전
- 각 단계마다 테스트 수행
- 사용자에게 변경사항 알림
- 하위 호환성 유지

## 6. 임포트 예시

### 옵션 3의 임포트 방식:
```python
# 핸들러 임포트
from junLib import XMLHandler, CSVHandler, VideoHandler, FileHandler

# 유틸리티 임포트
from junLib import format_time, format_time_with_ms

# 사용 예시
xml_handler = XMLHandler("example.xml")
csv_handler = CSVHandler("data.csv")
video_handler = VideoHandler("video.mp4")
file_handler = FileHandler("some_file.txt")

formatted_time = format_time(3600)  # "01:00:00"
```

이 방식은 다음과 같은 장점이 있습니다:
1. 사용자는 패키지의 내부 구조를 알 필요 없이 바로 필요한 클래스나 함수를 임포트할 수 있습니다.
2. 각 기능별로 관련 코드가 한 폴더에 모여있어 관리가 용이합니다.
3. 각 기능 폴더 내에서 자유롭게 파일을 추가하고 구조를 변경할 수 있습니다.
4. `__init__.py`를 통해 깔끔한 API를 제공합니다.
5. 불필요한 중첩 폴더가 없어 구조가 더 단순합니다.

예를 들어, `xml/__init__.py`는 다음과 같이 구성될 수 있습니다:
```python
from .XMLHandler import XMLHandler
from .XMLValidator import XMLValidator
from .utils import some_xml_utility

__all__ = ['XMLHandler', 'XMLValidator', 'some_xml_utility']
```

그리고 최상위 `__init__.py`에서는:
```python
from .xml import XMLHandler
from .csv import CSVHandler
from .video import VideoHandler
from .file import FileHandler
from .utils.datetime import format_time, format_time_with_ms

__all__ = [
    'XMLHandler',
    'CSVHandler',
    'VideoHandler',
    'FileHandler',
    'format_time',
    'format_time_with_ms'
]
```

## 7. 작업 순서

### 7.1 CSV 모듈 리팩토링
1. `csv/CSVHandler.py` 파일 수정
   - 클래스 이름을 `CSVHandler`로 변경
   - 불필요한 임포트 제거
   - 상대 경로 임포트로 변경
   - 문서화 추가

2. `csv/utils.py` 파일 수정
   - 유틸리티 함수 정리
   - 문서화 추가
   - 타입 힌트 추가

3. `csv/__init__.py` 파일 수정
   - 필요한 클래스와 함수 노출
   - 문서화 추가

### 7.2 XML 모듈 리팩토링
1. `xml/XMLHandler.py` 파일 수정
2. `xml/XMLValidator.py` 파일 수정
3. `xml/utils.py` 파일 수정
4. `xml/__init__.py` 파일 수정

### 7.3 비디오 모듈 리팩토링
1. [x] `video/VideoHandler.py` 파일 수정
2. [x] `video/AudioHandler.py` 파일 수정
3. [x] `video/utils.py` 파일 수정
4. [x] `video/__init__.py` 파일 수정

### 7.4 파일 시스템 모듈 리팩토링
1. [x] `file/FileHandler.py` 파일 수정
2. [x] `file/__init__.py` 파일 수정

### 7.5 유틸리티 모듈 정리
1. [x] `util/__init__.py` 파일 수정
2. `util/datetime.py` 파일 수정
3. `util/common.py` 파일 수정

### 7.6 테스트 및 문서화
1. 각 모듈별 테스트 코드 작성
2. API 문서 작성
3. 예제 코드 작성
4. README 업데이트

## 8. 임포트 경로 관리

### 8.1 상대 경로 임포트 규칙
- 최상위 모듈(`junLib`)은 `..`를 사용하여 임포트
  ```python
  from .. import junLib  # 올바른 예
  from . import junLib   # 잘못된 예
  ```
- 같은 패키지 내의 다른 모듈은 `.`를 사용하여 임포트
  ```python
  from . import some_module  # 올바른 예
  from .. import some_module # 잘못된 예
  ```

### 8.2 임포트 경로 수정 대상
1. CSV 모듈
   - [x] `csv/utils.py`: `from . import junLib` → `from .. import junLib`

2. XML 모듈
   - [x] `xml/XMLHandler.py`: `from . import junLib` → `from .. import junLib`
   - [x] `xml/XMLValidator.py`: `from . import junLib` → `from .. import junLib`
   - [x] `xml/utils.py`: `from . import junLib` → `from .. import junLib`

3. 비디오 모듈
   - [x] `video/VideoHandler.py`
   - [x] `video/AudioHandler.py`
   - [x] `video/utils.py`

4. 파일 시스템 모듈
   - [x] `file/FileHandler.py`
   - [x] `file/__init__.py`

### 8.3 주의사항
1. 순환 참조 방지
   - 모듈 간 순환 참조가 발생하지 않도록 주의
   - 필요한 경우 타입 힌트에 문자열로 타입 지정

2. 상대 경로 사용
   - 가능한 한 절대 경로 대신 상대 경로 사용
   - 패키지 구조 변경 시 임포트 경로도 함께 수정

3. 임포트 순서
   - 표준 라이브러리
   - 서드파티 라이브러리
   - 로컬 모듈

4. 임포트 검증
   - 각 모듈 리팩토링 시 임포트 경로 검증 필수
   - 테스트 코드로 임포트 동작 확인
