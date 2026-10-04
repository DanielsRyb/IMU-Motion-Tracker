import csv
import math
import matplotlib.pyplot as plt #导入库并命名为plt

timestamps = []#创建一个空list用于后续存储连续的数据以便画图
accelerations = []#注意这里有“s”，以区分列表和后续使用的浮点数
angular_velocities = []
az_values = []

def moving_average(data, window_size):
    filtered_data = []

    for i in range(window_size - 1, len(data)):
        window = data[i - (window_size - 1):i + 1]#window取window_size个值，并且对齐第一个从data[0]开始的window
        average = sum(window) / window_size#取这window_size个值的平均
        filtered_data.append(average)

    return filtered_data


with open("data/simulated.csv", "r") as file:#with...as...打开一个文件并命名
    reader = csv.DictReader(file)#声明reader，csv.DictReader()意味把csv的一行变成dict（字典）类型
    print(f"{'timestamp':>10} {'ax':>8} {'ay':>8} {'az':>8} {'acceleration':>15} {'wx':>8} {'wy':>8} {'wz':>8} {'angular_velocity':>20}")#f"..."表示f-string，引号内用{}可以代入变量
    
    for row in reader:
        ax = float(row["ax"]) #将字符串转换成浮点数类型
        ay = float(row["ay"])
        az = float(row["az"])

        az_values.append(az)
        acceleration = math.sqrt(ax**2 + ay**2 + az**2)

        timestamps.append(float(row["timestamp"])) #将当前timestamp加入timestamp列表
        accelerations.append(acceleration)

        wx = float(row["wx"])
        wy = float(row["wy"])
        wz = float(row["wz"])

        angular_velocity = math.sqrt(wx**2 + wy**2 + wz**2)
        angular_velocities.append(angular_velocity)

        print(f"{row['timestamp']:>10} {ax:>8.2f} {ay:>8.2f} {az:>8.2f} {acceleration:>15.2f} {wx:>8.2f} {wy:>8.2f} {wz:>8.2f} {angular_velocity:>20.2f}")


filtered_az = moving_average(az_values, 5)#窗口为5，相当于用前2个后2个平滑处理当前的值，但是会导致最终数据从原本的len(data)个数据减少为(len(data) - window_size + 1)个，需要让时间戳对齐
filtered_timestamps = timestamps[2:-2]
print(filtered_az[:10])

#with负责打开和使用文件，我们现在已经将数据存入列表timestamp和acceleration了，于是跳出with画图
plt.subplot(3, 1, 1)
#将画布分成3行，1列，现在作第1幅图
plt.plot(timestamps, accelerations)#横轴，数轴数据，这里写变量
plt.xlabel("Time (s)")#横轴标签
plt.ylabel("Acceleration (m/s²)")#数轴标签
plt.title("Acceleration vs Time")#图像标题


plt.subplot(3, 1, 2)
#将画布分成3行，1列，现在作第2幅图
plt.plot(timestamps, angular_velocities)
plt.xlabel("Time (s)")
plt.ylabel("Angular_velocity (rad/s)")
plt.title("Angular velocity vs Time")


plt.subplot(3,1,3)

plt.plot(timestamps, az_values, label="Raw")#第一条线数据及标签
plt.plot(filtered_timestamps, filtered_az, label="Filtered")#第二条线数据及标签
plt.xlabel("Time (s)")
plt.ylabel("az (m/s²)")
plt.title("z-axis Acceleration vs Time")

plt.tight_layout() #自动调整三个图之间的间距，避免标题、坐标轴标签互相挤在一起
plt.show()#显示图像