import csv
import math
with open("data/sample.csv", "r") as file:
    reader = csv.DictReader(file)
    print(f"{'timestamp':>10} {'ax':>8} {'ay':>8} {'az':>8} {'acceleration':>15}")
    for row in reader:
        ax = float(row["ax"])
        ay = float(row["ay"])
        az = float(row["az"])
        acceleration = math.sqrt(ax**2 + ay**2 + az**2)
        print(f"{row['timestamp']:>10} {ax:>8.2f} {ay:>8.2f} {az:>8.2f} {acceleration:>15.2f}")