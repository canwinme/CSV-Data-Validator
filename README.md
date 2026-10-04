# 규칙 기반 CSV 데이터 검증 프로그램

## 📌 프로젝트 소개

Python을 이용해 CSV 데이터에 포함된 **빈 값, 잘못된 자료형, 범위를 벗어난 값, 중복값**을 JSON 규칙에 따라 검사하는 프로그램입니다.

CSV 데이터와 검증 기준을 분리해 관리하고, 오류가 발생한 **행 번호·컬럼명·입력값·오류 유형**을 정리하여 CSV 파일로 저장합니다. 오류가 있는 경우에는 Matplotlib 막대그래프로 오류 유형별 개수를 확인할 수 있도록 구성했습니다.

동일한 기능을 함수형 코드(main_func.py)와 클래스형 코드(main_class.py)로 각각 구현하여 데이터 전달 방식과 관리 방식의 차이를 비교했습니다.

## 🛠 기술 스택

- **Language**: Python
- **Data Format**: CSV, JSON
- **Library**: Matplotlib
- **Built-in Modules**: csv, json, collections.Counter
- **Development Environment**: Windows, VS Code

## ✨ 주요 기능

- CSV 파일 읽기 및 헤더·데이터 유무 확인
- JSON 규칙 파일 읽기
- 규칙에 지정된 컬럼 존재 여부 확인
- 필수값 누락 검사
- int / float / str 자료형 검사
- min / max 범위 검사
- unique 설정 컬럼의 중복값 검사
- 오류 행 번호·컬럼명·입력값·오류 유형 기록
- 검증 결과를 output/result.csv로 저장
- 오류 유형별 개수를 Matplotlib 막대그래프로 시각화
- 오류가 없는 경우 그래프 출력 생략

## 🧩 검증 규칙

검증 기준은 rules/rules.json에서 관리합니다.

~~~json
{
  "id": {
    "type": "int",
    "required": true,
    "unique": true
  },
  "name": {
    "type": "str",
    "required": true
  },
  "age": {
    "type": "int",
    "required": true,
    "min": 0,
    "max": 120
  },
  "score": {
    "type": "float",
    "required": true,
    "min": 0,
    "max": 100
  }
}
~~~

| 규칙 | 설명 |
| --- | --- |
| required | 필수값 누락 또는 공백 검사 |
| type | int, float, str 자료형 검사 |
| min | 설정한 최솟값 이상인지 검사 |
| max | 설정한 최댓값 이하인지 검사 |
| unique | 동일 값의 중복 여부 검사 |

필수값 누락이 확인되면 해당 값의 자료형·범위 검사는 생략하고, 자료형 오류가 확인된 값도 범위 검사를 진행하지 않습니다.

## 🏗 프로젝트 구조

~~~text
CSV-Data-Validator/
├── README.md
├── main_class.py
├── main_func.py
├── requirements.txt
│
├── data/
│   ├── sample_normal.csv
│   └── sample_error.csv
│
├── rules/
│   └── rules.json
│
└── output/
    └── result.csv
~~~

### 파일 역할

- main_class.py: CSVValidator 클래스를 사용한 검증 프로그램
- main_func.py: 함수 중심으로 구성한 검증 프로그램
- data/sample_normal.csv: 검증 기준을 만족하는 정상 데이터
- data/sample_error.csv: 여러 종류의 오류가 포함된 500건의 테스트 데이터
- rules/rules.json: 컬럼별 검증 기준
- output/result.csv: 검증 후 생성되는 오류 목록

## 🔄 프로그램 동작 흐름

~~~text
CSV 데이터 ─────┐
                ├─> CSVValidator / 검증 함수
JSON 규칙 ──────┘
                        │
                        ▼
                  데이터 검증
                        │
              ┌─────────┼─────────┐
              ▼         ▼         ▼
          콘솔 출력  CSV 저장  그래프 표시
~~~

1. CSV 데이터와 JSON 규칙 파일을 읽습니다.
2. 규칙에 지정된 컬럼이 CSV에 존재하는지 확인합니다.
3. 필수값·자료형·범위 검사를 수행합니다.
4. unique 규칙이 적용된 컬럼의 중복값을 검사합니다.
5. 오류 정보를 콘솔에 출력하고 output/result.csv에 저장합니다.
6. 오류가 존재하면 오류 유형별 개수를 그래프로 표시합니다.

## ▶ 실행 방법

### 1. 저장소 복제

~~~bash
git clone https://github.com/canwinme/CSV-Data-Validator.git
cd CSV-Data-Validator
~~~

### 2. 필요한 라이브러리 설치

~~~bash
pip install -r requirements.txt
~~~

### 3. 클래스형 프로그램 실행

~~~bash
python main_class.py
~~~

기본 입력 파일은 data/sample_normal.csv로 설정되어 있습니다.

오류 데이터를 확인하려면 main_class.py의 입력 경로를 다음과 같이 변경합니다.

~~~python
validator = CSVValidator(
    "data/sample_error.csv",
    "rules/rules.json"
)
~~~

함수형 버전을 실행하려면 다음 명령을 사용합니다.

~~~bash
python main_func.py
~~~

