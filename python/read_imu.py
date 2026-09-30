import csv
with open("data/sample.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        ax = float(row["ax"])
        print(ax)
        print(type(ax))