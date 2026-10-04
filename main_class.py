import csv
import json
from collections import Counter
import matplotlib.pyplot as plt

# Matplotlib 한글 및 음수 기호 깨짐 방지
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

class CSVValidator:
    def __init__(self, csv_file, rule_file):
        self.csv_file = csv_file
        self.rule_file = rule_file
        self.data = []
        self.rules = {}
        self.errors = []

    def load_csv(self):
        try:
            with open(self.csv_file, "r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)

                if reader.fieldnames is None:
                    print("CSV 헤더가 없습니다.")
                    return False

                for row in reader:
                    self.data.append(row)

            if len(self.data) == 0:
                print("CSV 데이터가 비어 있습니다.")
                return False
            
            return True

        except FileNotFoundError:
            print("CSV 파일을 찾을 수 없습니다.")
            return False

    def load_rules(self):
        try:
            with open(self.rule_file, "r", encoding="utf-8") as file:
                self.rules = json.load(file)

            return True

        except FileNotFoundError:
            print("규칙 파일을 찾을 수 없습니다.")
            return False

        except json.JSONDecodeError:
            print("JSON 형식이 올바르지 않습니다.")
            return False
    
    def check_columns(self):
        missing = []
        csv_columns = self.data[0].keys()

        for column in self.rules.keys():
            if column not in csv_columns:
                missing.append(column)

        return missing    

    def check_required(self, value):
        return value is not None and value.strip() != ""

    def check_type(self, value, expected_type):
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
        
    def check_range(self, value, min_value=None, max_value=None):
        value = float(value)

        if min_value is not None and value < min_value:
            return False

        if max_value is not None and value > max_value:
            return False

        return True  
    
    def validate_data(self):
        self.errors = []

        # CSV 1행이 헤더이므로 실제 데이터 행 번호는 2부터 시작
        for row_number, row in enumerate(self.data, start=2):
            for column, rule in self.rules.items():

                value = row.get(column, "")

                # 필수값이 없으면 이후 자료형/범위 검사는 생략
                if rule.get("required") and not self.check_required(value):
                    self.errors.append({
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

                if expected_type and not self.check_type(value, expected_type):
                    self.errors.append({
                        "row": row_number,
                        "column": column,
                        "value": value,
                        "error": "자료형 오류"
                    })
                    continue

                if "min" in rule or "max" in rule:
                    min_value = rule.get("min")
                    max_value = rule.get("max")

                    if not self.check_range(value, min_value, max_value):
                        self.errors.append({
                            "row": row_number,
                            "column": column,
                            "value": value,
                            "error": "범위 오류"
                        })

        return self.errors  
    
    def check_duplicates(self):
        for column, rule in self.rules.items():
            if not rule.get("unique"):
                continue
            
            # 이미 등장한 값을 저장하여 중복 여부 확인
            seen = set()

            for row_number, row in enumerate(self.data, start=2):
                value = row.get(column, "")

                if value == "":
                    continue

                if value in seen:
                    self.errors.append({
                        "row": row_number,
                        "column": column,
                        "value": value,
                        "error": "중복 오류"
                    })
                else:
                    seen.add(value)
    
    def save_errors(self, filename):
        with open(filename, "w", newline="", encoding="utf-8-sig") as file:
            fieldnames = ["row", "column", "value", "error"]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.errors)
    
    def draw_chart(self):
        if len(self.errors) == 0:
            return

        error_count = Counter(
            error["error"]
            for error in self.errors
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
        plt.figtext(
            0.98,
            0.95,
            f"총 오류: {len(self.errors)}",
            ha="right",
            va="top"
        )

        plt.show()
        
def main():
    validator = CSVValidator(
        "data/sample_normal.csv",
        "rules/rules.json"
    )

    if not validator.load_csv():
        return

    if not validator.load_rules():
        return

    missing = validator.check_columns()

    if missing:
        print("없는 컬럼 :", missing)
        return

    validator.validate_data()
    validator.check_duplicates()

    print("\nCSV 검증 결과")
    print("전체 데이터 :", len(validator.data), "건")
    print("총 오류 :", len(validator.errors), "건")
    print()
    for error in validator.errors:
        print(error)

    validator.save_errors("output/result.csv")
    validator.draw_chart()


if __name__ == "__main__":
    main()
