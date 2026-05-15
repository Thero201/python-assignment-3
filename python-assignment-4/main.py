from analytics import FileManager, DataLoader, ResultSaver, Report
from analytics.analyser import SleepAnalyser, CountryAnalyser


import os

 
def main():

    fm = FileManager("students.csv")

    if not fm.check_file():
        return

    output_folder = fm.create_output_folder()

    dl = DataLoader("students.csv")

    students = dl.load()

    dl.preview()



    analysers = [

        SleepAnalyser(students),

        CountryAnalyser(students[:10])
    ]

    print("-" * 30)
    print("Running all analysers:")
    print("-" * 30)

    for analyser in analysers:

        print(analyser)

        analyser.analyse()

        analyser.print_results()



    saver = ResultSaver(
        {},
        os.path.join(output_folder, "result.json")
    )

    report = Report(
        analysers[0],
        saver
    )

    report.generate()


if __name__ == "__main__":
    main()