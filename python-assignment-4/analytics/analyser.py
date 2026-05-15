class DataAnalyser:

    def __init__(self, students):

        self.students = students
        self.result = {}

    def analyse(self):

        print("Not implemented — use a child class")

    def print_results(self):

        for key, value in self.result.items():
            print(f"{key}: {value}")

    def __str__(self):

        return f"DataAnalyser: base class, {len(self.students)} students"


class SleepAnalyser(DataAnalyser):

    def __init__(self, students):

        super().__init__(students)

    def analyse(self):

        low_sleep_gpas = []
        high_sleep_gpas = []

        for student in self.students:

            try:

                sleep = float(student["sleep_hours"])
                gpa = float(student["GPA"])

                if sleep < 6:
                    low_sleep_gpas.append(gpa)

                else:
                    high_sleep_gpas.append(gpa)

            except:
                continue

        avg_low = round(
            sum(low_sleep_gpas) / len(low_sleep_gpas), 2
        ) if low_sleep_gpas else 0

        avg_high = round(
            sum(high_sleep_gpas) / len(high_sleep_gpas), 2
        ) if high_sleep_gpas else 0

        difference = round(abs(avg_high - avg_low), 2)

        self.result = {
            "total_students": len(self.students),

            "low_sleep": {
                 "students": len(low_sleep_gpas),
                "avg_gpa": avg_low
            },

            "high_sleep": {
                "students": len(high_sleep_gpas),
               "avg_gpa": avg_high
            },

        "gpa_difference": difference
}
    def print_results(self):

        print("=" * 30)
        print("SLEEP ANALYSIS REPORT")
        print("=" * 30)

        super().print_results()

        print("=" * 30)

    def __str__(self):

        return (
            f"SleepAnalyser: Sleep vs GPA Analysis, "
            f"{len(self.students)} students"
        )


class CountryAnalyser(DataAnalyser):

    def __init__(self, students):

        super().__init__(students)

    def analyse(self):

        countries = {}

        for student in self.students:

            country = student.get("country", "Unknown")

            countries[country] = countries.get(country, 0) + 1

        self.result = {

            "total_students": len(self.students),
            "total_countries": len(countries)
        }

    def print_results(self):

        print("=" * 30)
        print("COUNTRY ANALYSIS REPORT")
        print("=" * 30)

        super().print_results()

        print("=" * 30)

    def __str__(self):

        return (
            f"CountryAnalyser: Country Analysis, "
            f"{len(self.students)} students"
        )