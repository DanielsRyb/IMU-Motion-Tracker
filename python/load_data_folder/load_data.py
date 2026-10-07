import csv


def load_imu_data(filename):
    with open(filename, "r") as file:
        reader = csv.DictReader(file)#声明reader，csv.DictReader()意味把csv的一行变成dict（字典）类型

        data = []

        for row in reader:

            row["timestamp"] = float(row["timestamp"])#将字符串转换成浮点数类型
            row["ax"] = float(row["ax"])
            row["ay"] = float(row["ay"])
            row["az"] = float(row["az"])
            row["wx"] = float(row["wx"])
            row["wy"] = float(row["wy"])
            row["wz"] = float(row["wz"])


            data.append(row)

    return data#type: list ; elements: dict