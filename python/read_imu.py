import csv
import math
with open("data/sample.csv", "r") as file:
    reader = csv.DictReader(file)
    print(f"{'timestamp':>10} {'ax':>8} {'ay':>8} {'az':>8} {'acceleration':>15} {'gx':>8} {'gy':>8} {'gz':>8} {'angular_velocity':>20}")
    for row in reader:
        ax = float(row["ax"])
        ay = float(row["ay"])
        az = float(row["az"])
        acceleration = math.sqrt(ax**2 + ay**2 + az**2)
        gx = float(row["gx"])
        gy = float(row["gy"])
        gz = float(row["gz"])
        angular_velocity = math.sqrt(gx**2 + gy**2 + gz**2)
        print(f"{row['timestamp']:>10} {ax:>8.2f} {ay:>8.2f} {az:>8.2f} {acceleration:>15.2f} {gx:>8.2f} {gy:>8.2f} {gz:>8.2f} {angular_velocity:>20.2f}")