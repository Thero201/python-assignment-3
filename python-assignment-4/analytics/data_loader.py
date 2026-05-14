import csv


class DataLoader:

    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):

        with open(self.filename, "r", encoding="utf-8") as file:
            self.students = list(csv.DictReader(file))

        print(f"Total students: {len(self.students)}")

        return self.students

    def preview(self, n=5):

        print("First 5 rows:")
        print("-" * 30)

        for student in self.students[:n]:

            print(
                f"{student['student_id']} | "
                f"{student['age']} | "
                f"{student['gender']} | "
                f"{student['country']} | "
                f"GPA: {student['GPA']}"
            )

        print("-" * 30)