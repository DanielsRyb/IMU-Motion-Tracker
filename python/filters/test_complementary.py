from load_data_fodler.load_data import load_imu_data
from orientation_folder.orientation import calculate_roll
from complementary_filter import complementary_filter#不只是调取这个函数，而是加载一整个模块
import math
from visualize_folder.visualize import plot_roll_comparison

data = load_imu_data("data/simulated.csv")#读数据

timestamps = []
accelerometer_rolls = []
gyro_rolls = []
filtered_rolls = []

gyro_roll = 0.0
filtered_roll = 0.0

for i, row in enumerate(data):

    ax = row["ax"]
    ay = row["ay"]
    az = row["az"]

    accelerometer_roll = calculate_roll(ax, ay, az)#Accelerometer angle

    if i == 0:
        dt = 0.0
    else:
        dt = row["timestamp"] - data[i - 1]["timestamp"]

    wx = row["wx"]#Gyroscope

    gyro_roll = gyro_roll + wx * dt


    filtered_roll = complementary_filter(#一次积分和一次加权
        filtered_roll,
        wx,
        dt,
        math.radians(accelerometer_roll)#转化为弧度制
    )

    timestamps.append(row["timestamp"])
    accelerometer_rolls.append(accelerometer_roll)
    gyro_rolls.append(math.degrees(gyro_roll))
    filtered_rolls.append(math.degrees(filtered_roll))

print("Final accelerometer roll:", accelerometer_rolls[-1])#[-1]指代最后一个#重力角度分析转向
print("Final gyro roll:", gyro_rolls[-1])#角速度测量仪分析转向
print("Final filtered roll:", filtered_rolls[-1])#两种分析方法用互补滤波

plot_roll_comparison(
    timestamps,
    accelerometer_rolls,
    gyro_rolls,
    filtered_rolls
)