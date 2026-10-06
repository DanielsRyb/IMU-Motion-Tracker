import math
from  load_data import load_imu_data

def calculate_roll(ax, ay, az):#左右翻滚
    roll = math.degrees(math.atan2(ay, az))#返回弧度, 格式：atan2(y,x)，第一个参数输入张角方向，此处以az为角的固定边
    return roll

def calculate_pitch(ax, ay, az):#前后翻滚
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2))#向前俯，角度减小，向后仰，角度变大，平视时角度为0
    return math.degrees(pitch)


data = load_imu_data("data/simulated.csv")

for row in data:
    ax = row["ax"]
    ay = row["ay"]
    az = row["az"]

    roll = calculate_roll(ax, ay, az)
    pitch = calculate_pitch(ax, ay, az)

    print(
        f"t={row['timestamp']:.2f}s "
        f"roll={roll:.2f}° "
        f"pitch={pitch:.2f}°"
    )