import math
from load_data_folder.load_data import load_imu_data


def main():

    timestamps = []#创建一个空list用于后续存储连续的数据以便画图
    accelerations = []#注意这里有“s”，以区分列表和后续使用的浮点数
    angular_velocities = []
    az_values = []


    print(f"{'timestamp':>10} {'ax':>8} {'ay':>8} {'az':>8} {'acceleration':>15} {'wx':>8} {'wy':>8} {'wz':>8} {'angular_velocity':>20}")#f"..."表示f-string，引号内用{}可以代入变量
        
    data = load_imu_data("../data/simulated.csv")#数据交给load文件，返回data#根目录变成python后要先返回上一级的IMU再找data

    print(data[0])

    for row in data:
        ax = row["ax"] 
        ay = row["ay"]
        az = row["az"]

        az_values.append(az)
        acceleration = math.sqrt(ax**2 + ay**2 + az**2)

        timestamps.append(row["timestamp"]) #将当前timestamp加入timestamp列表
        accelerations.append(acceleration)

        wx = row["wx"]
        wy = row["wy"]
        wz = row["wz"]

        angular_velocity = math.sqrt(wx**2 + wy**2 + wz**2)
        angular_velocities.append(angular_velocity)

        print(f"{row['timestamp']:>10} {ax:>8.2f} {ay:>8.2f} {az:>8.2f} {acceleration:>15.2f} {wx:>8.2f} {wy:>8.2f} {wz:>8.2f} {angular_velocity:>20.2f}")

if __name__ == "__main__":
        main()