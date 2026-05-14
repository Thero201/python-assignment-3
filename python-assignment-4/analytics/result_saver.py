import json


class ResultSaver:

    def __init__(self, result, output_path):

        self.result = result
        self.output_path = output_path

    def save_json(self):

        with open(self.output_path, "w", encoding="utf-8") as file:

            json.dump(self.result, file, indent=4)

        print(f"Result saved to {self.output_path}")