import math
from  load_data import load_imu_data
from visualize import plot_roll_comparison



def calculate_roll(ax, ay, az):#左右翻滚
    roll = math.degrees(math.atan2(ay, az))#返回弧度, 格式：atan2(y,x)，第一个参数输入张角方向，此处以az为参考方向的分量输入，而ay为垂直于参考分量的输入，本质为arctan+象限判断
    return roll

def calculate_pitch(ax, ay, az):#前后翻滚
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2))#向前俯，角度减小，向后仰，角度变大，平视时角度为0
    return math.degrees(pitch)



def simulate_gyro_drift():#积分误差
    angle = 0.0

    bias = 0.001#零点偏差：陀螺仪实际上没有旋转，它仍然会测出一个不为 0 的角速度
    dt = 0.01
    duration = 10

    angles = []
    timestamps = []

    for i in range(int(duration / dt)):
        timestamp = i * dt

        angle = integrate_gyro(angle, bias, dt)

        timestamps.append(timestamp)
        angles.append(math.degrees(angle))

    return timestamps, angles




data = load_imu_data("data/simulated.csv")

timestamps = []
acc_rolls = []
acc_pitches = []

for row in data:
    ax = row["ax"]
    ay = row["ay"]
    az = row["az"]

    acc_roll = calculate_roll(ax, ay, az)
    acc_pitch = calculate_pitch(ax, ay, az)

    timestamps.append(row["timestamp"])
    acc_rolls.append(acc_roll)
    acc_pitches.append(acc_pitch)


    print(
        f"t={row['timestamp']:.2f}s "
        f"acc_roll={acc_roll:.2f}° "
        f"acc_pitch={acc_pitch:.2f}°"
    )


def integrate_gyro(previous_angle, angular_velocity, dt):
    return previous_angle + angular_velocity * dt

angle = 0.0


gyro_roll = 0.0
gyro_pitch = 0.0

gyro_rolls = []
gyro_pitches = []


for i, row in enumerate(data):#带角标的for循环

    if i == 0:
        dt = 0.0
    else:
        dt = row["timestamp"] - data[i - 1]["timestamp"]

    wx = row["wx"]
    wy = row["wy"]

    gyro_roll = integrate_gyro(gyro_roll, wx, dt)
    gyro_pitch = integrate_gyro(gyro_pitch, wy, dt)

    gyro_rolls.append(math.degrees(gyro_roll))
    gyro_pitches.append(math.degrees(gyro_pitch))

drift_timestamps, drift_angles = simulate_gyro_drift()

print("Final gyro angle:", drift_angles[-1], "degrees")

plot_roll_comparison(timestamps, acc_rolls, gyro_rolls)