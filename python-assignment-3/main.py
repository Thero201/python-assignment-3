import csv
import json
import os


class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True

        print(f"Error: {self.filename} not found. Please download the file from LMS.")
        return False

    def create_output_folder(self, folder="output"):
        print("Checking output folder...")
        if os.path.exists(folder):
            print(f"Output folder already exists: {folder}/")
            return folder

        try:
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
            return folder
        except OSError as error:
            print(f"Error: could not create folder '{folder}': {error}")
            return None


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, "r", encoding="utf-8", newline="") as file:
                self.students = list(csv.DictReader(file))
            print(f"Data loaded successfully: {len(self.students)} students")
            return self.students
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found. Please check the filename.")
        except Exception as error:
            print(f"Error: could not load data: {error}")

        self.students = []
        return self.students

    def preview(self, n=5):
        if not self.students:
            print("No data available for preview.")
            return

        print(f"First {n} rows:")
        print("-" * 30)
        for student in self.students[:n]:
            print(
                f"{student.get('student_id', 'N/A')} | "
                f"{student.get('age', 'N/A')} | "
                f"{student.get('gender', 'N/A')} | "
                f"{student.get('country', 'N/A')} | "
                f"GPA: {student.get('GPA', 'N/A')}"
            )
        print("-" * 30)


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def _to_float(self, value, student_id, field_name):
        try:
            return float(value)
        except (TypeError, ValueError):
            print(
                f"Warning: could not convert {field_name} for student "
                f"{student_id} — skipping row."
            )
            return None

    def analyse(self):
        low_sleep_gpas = []
        high_sleep_gpas = []
        ready_students = []

        for student in self.students:
            student_id = student.get("student_id", "Unknown")

            sleep = self._to_float(student.get("sleep_hours"), student_id, "sleep_hours")
            gpa = self._to_float(student.get("GPA"), student_id, "GPA")

            if sleep is None or gpa is None:
                continue

            if sleep < 6:
                low_sleep_gpas.append(gpa)
            else:
                high_sleep_gpas.append(gpa)

            ready_students.append({"student_id": student_id, "GPA": gpa, "sleep_hours": sleep})

        if not ready_students:
            self.result = {
                "analysis": "Sleep vs GPA",
                "total_students": len(self.students),
                "low_sleep": {"students": 0, "avg_gpa": 0},
                "high_sleep": {"students": 0, "avg_gpa": 0},
                "gpa_difference": 0,
                "lambda_filter_summary": {
                    "students_sleep_under_6": 0,
                    "gpa_values_first_5": [],
                    "students_stress_above_7": 0,
                },
            }
            return self.result

        avg_low = round(sum(low_sleep_gpas) / len(low_sleep_gpas), 2) if low_sleep_gpas else 0
        avg_high = round(sum(high_sleep_gpas) / len(high_sleep_gpas), 2) if high_sleep_gpas else 0
        difference = round(abs(avg_high - avg_low), 2)

        # Lambda / Map / Filter
        low_sleep_students = list(
            filter(lambda s: s["sleep_hours"] < 6, ready_students)
        )
        gpa_values = list(
            map(lambda s: s["GPA"], ready_students)
        )
        stressed_students = list(
            filter(lambda s: float(s.get("mental_stress_level", 0)) > 7, self.students)
        )

        self.result = {
            "analysis": "Sleep vs GPA",
            "total_students": len(self.students),
            "low_sleep": {"students": len(low_sleep_gpas), "avg_gpa": avg_low},
            "high_sleep": {"students": len(high_sleep_gpas), "avg_gpa": avg_high},
            "gpa_difference": difference,
            "lambda_filter_summary": {
                "students_sleep_under_6": len(low_sleep_students),
                "gpa_values_first_5": gpa_values[:5],
                "students_stress_above_7": len(stressed_students),
            },
        }
        return self.result

    def print_results(self):
        if not self.result:
            print("No analysis results to print.")
            return

        lf = self.result.get("lambda_filter_summary", {})

        print("-" * 30)
        print("Sleep vs GPA Analysis")
        print("-" * 30)
        print(f"Students sleeping < 6 hours  : {self.result['low_sleep']['students']} "
              f"avg GPA: {self.result['low_sleep']['avg_gpa']}")
        print(f"Students sleeping >= 6 hours : {self.result['high_sleep']['students']} "
              f"avg GPA: {self.result['high_sleep']['avg_gpa']}")
        print(f"GPA difference               : {self.result['gpa_difference']}")
        print("-" * 30)

        print("-" * 30)
        print("Lambda / Map / Filter")
        print("-" * 30)
        print(f"sleep_hours < 6          : {lf.get('students_sleep_under_6', 0)}")
        print(f"GPA values (first 5)     : {lf.get('gpa_values_first_5', [])}")
        print(f"mental_stress_level > 7  : {lf.get('students_stress_above_7', 0)}")
        print("-" * 30)

        print("=" * 30)
        print("ANALYSIS RESULT")
        print("=" * 30)
        print(f"Analysis         : {self.result['analysis']}")
        print(f"Total students   : {self.result['total_students']}")
        print("-" * 30)
        print("Sleep < 6 hours:")
        print(f"  Students       : {self.result['low_sleep']['students']}")
        print(f"  Average GPA    : {self.result['low_sleep']['avg_gpa']}")
        print("Sleep >= 6 hours:")
        print(f"  Students       : {self.result['high_sleep']['students']}")
        print(f"  Average GPA    : {self.result['high_sleep']['avg_gpa']}")
        print("-" * 30)
        print(f"GPA difference   : {self.result['gpa_difference']}")
        print("=" * 30)


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, "w", encoding="utf-8") as file:
                json.dump(self.result, file, indent=4)
            print(f"Result saved to {self.output_path}")
        except OSError as error:
            print(f"Error: could not save result to '{self.output_path}': {error}")


def main():
    file_manager = FileManager("students.csv")
    if not file_manager.check_file():
        print("Stopping program.")
        return

    output_folder = file_manager.create_output_folder()
    if output_folder is None:
        print("Stopping program.")
        return

    data_loader = DataLoader("students.csv")
    students = data_loader.load()
    if not students:
        return

    data_loader.preview()

    analyser = DataAnalyser(students)
    analyser.analyse()
    analyser.print_results()

    saver = ResultSaver(analyser.result, os.path.join(output_folder, "result.json"))
    saver.save_json()


if __name__ == "__main__":
    main()