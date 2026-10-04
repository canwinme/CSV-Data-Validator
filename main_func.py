import csv
import json
from collections import Counter
import matplotlib.pyplot as plt

# Matplotlib 한글 및 음수 기호 깨짐 방지
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

def load_csv(filename):
    data = []
    try:
        with open(filename, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print("CSV 헤더가 없습니다.")
                return None

            for row in reader:
                data.append(row)
        
        if len(data) == 0:
            print("CSV 데이터가 비어 있습니다.")
            return None
        
    
    except FileNotFoundError:
        print("CSV 파일을 찾을 수 없습니다.")


def load_rules(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    
    except FileNotFoundError:
        print("규칙 파일을 찾을 수 없습니다.")
        return None
    
    except json.JSONDecodeError:
        print("JSON 형식이 올바르지 않습니다.")
        return None

def check_columns(data, rules):
    missing_columns = []

    if len(data) == 0:
        return missing_columns

    csv_columns = data[0].keys()

    for column in rules.keys():
        if column not in csv_columns:
            missing_columns.append(column)

    return missing_columns

def check_required(value):
    if value is None or value.strip() == "":
        return False

    return True

def check_type(value, expected_type):
    try:
        if expected_type == "int":
            int(value)

        elif expected_type == "float":
            float(value)

        elif expected_type == "str":
            str(value)

        return True

    except ValueError:
        return False

def check_range(value, min_value=None, max_value=None):
    value = float(value)

    if min_value is not None and value < min_value:
        return False

    if max_value is not None and value > max_value:
        return False

    return True

def validate_data(data, rules):
    errors = []
    # CSV 첫 번째 행은 헤더이므로 실제 데이터 행 번호는 2부터 시작
    for row_number, row in enumerate(data, start=2):

        for column, rule in rules.items():

            value = row.get(column, "")

            # 필수값이 없으면 이후 자료형/범위 검사는 생략
            if rule.get("required"):
                if not check_required(value):
                    errors.append({
                        "row": row_number,
                        "column": column,
                        "value": value,
                        "error": "필수값 누락"
                    })
                    continue

            # 선택 항목의 빈 값은 검증 대상에서 제외
            if value == "":
                continue

            expected_type = rule.get("type")

            if expected_type:
                if not check_type(value, expected_type):
                    errors.append({
                        "row": row_number,
                        "column": column,
                        "value": value,
                        "error": "자료형 오류"
                    })

                    continue

            if "min" in rule or "max" in rule:

                min_value = rule.get("min")
                max_value = rule.get("max")

                if not check_range(value, min_value, max_value):
                    errors.append({
                        "row": row_number,
                        "column": column,
                        "value": value,
                        "error": "범위 오류"
                    })

    return errors

def save_errors(errors, filename):

    with open(filename, "w", newline="", encoding="utf-8-sig") as file:

        fieldnames = [
            "row",
            "column",
            "value",
            "error"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(errors)
        
def check_duplicates(data, rules, errors):

    for column, rule in rules.items():

        if not rule.get("unique"):
            continue
        
        # 이미 나온 값을 저장해 중복 여부 확인
        seen = set()

        for row_number, row in enumerate(data, start=2):

            value = row.get(column, "")

            if value == "":
                continue

            if value in seen:
                errors.append({
                    "row": row_number,
                    "column": column,
                    "value": value,
                    "error": "중복 오류"
                })

            else:
                seen.add(value)

def draw_chart(errors):

    if len(errors) == 0:
        return
    
    error_count = Counter(
        error["error"]
        for error in errors
    )

    names = list(error_count.keys())
    counts = list(error_count.values())
    bars = plt.bar(names, counts)

    plt.title("CSV 검증 결과")
    plt.xlabel("오류 유형")
    plt.ylabel("오류 개수")
    
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            str(int(height)),
            ha="center",
            va="bottom"
            )
        
    plt.show()


def main():

    csv_file = "data/sample_normal.csv"
    rule_file = "rules/rules.json"

    data = load_csv(csv_file)
    rules = load_rules(rule_file)

    if data is None or rules is None:
        return

    missing_columns = check_columns(data, rules)

    if missing_columns:
        print("없는 컬럼 :", missing_columns)
        return

    errors = validate_data(data, rules)
    check_duplicates(
        data,
        rules,
        errors
    )

    print("\nCSV 검증 결과")
    print("전체 데이터 :", len(data), "건")
    print("총 오류 :", len(errors), "건")

    if len(errors) == 0:
        print("검증 결과 : 오류가 없습니다.")
    else:
        print("\n상세 오류")
        for error in errors:
            print(
                f"{error['row']}행 | "
                f"{error['column']} | "
                f"{error['value']} | "
                f"{error['error']}"
            )

    save_errors(
        errors,
        "output/result.csv"
    )

    draw_chart(errors)

if __name__ == "__main__":
    main()
