import os


class FileManager:

    def __init__(self, filename):
        self.filename = filename

    def check_file(self):

        print("Checking file...")

        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True

        print(f"Error: {self.filename} not found.")
        return False

    def create_output_folder(self, folder="output"):

        print("Checking output folder...")

        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")

        return folder