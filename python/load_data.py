import csv


def load_imu_data(filename):
    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        data = []

        for row in reader:
            data.append(row)

    return data