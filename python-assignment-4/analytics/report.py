class Report:

    def __init__(self, analyser, saver):

        self.analyser = analyser
        self.saver = saver

    def generate(self):

        print("Generating report...")

        self.analyser.analyse()

        self.analyser.print_results()

        self.saver.result = self.analyser.result

        self.saver.save_json()

        print("Report complete.")