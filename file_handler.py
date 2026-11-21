
import os


class FileHandler:

    def __init__(self):
        self.data_folder = "data"

        os.makedirs(self.data_folder, exist_ok=True)

    def save_data(self, filename, records):

        path = os.path.join(self.data_folder, filename)

        with open(path, "w", encoding="utf-8") as file:

            for record in records:
                file.write("|".join(map(str, record)) + "\n")

    def load_data(self, filename):

        path = os.path.join(self.data_folder, filename)

        if not os.path.exists(path):
            return []

        records = []

        with open(path, "r", encoding="utf-8") as file:

            for line in file:
                line = line.strip()

                if line:
                    records.append(line.split("|"))

        return records
