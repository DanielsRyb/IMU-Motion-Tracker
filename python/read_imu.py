import csv
import math
with open("data/sample.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        ax = float(row["ax"])
        ay = float(row["ay"])
        az = float(row["az"])
        asum = math.sqrt(ax**2 + ay**2 + az**2)
        print(asum)