import math
import matplotlib.pyplot as plt

from complementary_filter import complementary_filter


sample_rate = 100
duration = 10
dt = 1 / sample_rate

timestamps = []

accelerometer_rolls = []
gyro_rolls = []
filtered_rolls = []

gyro_roll = 0.0
filtered_roll = 0.0


for i in range(sample_rate * duration):

    timestamp = i * dt

    wx = 0.0#没有旋转

    az = 9.81#重力

    if 3 <= timestamp < 5:#出现加速度
        ay = 3.0
    else:
        ay = 0.0

    # Accelerometer roll
    accelerometer_roll = math.atan2(ay, az)

    # Gyroscope integration
    gyro_roll = gyro_roll + wx * dt

    filtered_roll = complementary_filter(
        filtered_roll,
        wx,
        dt,
        accelerometer_roll
    )

    timestamps.append(timestamp)
    accelerometer_rolls.append(math.degrees(accelerometer_roll))
    gyro_rolls.append(math.degrees(gyro_roll))
    filtered_rolls.append(math.degrees(filtered_roll))


plt.plot(
    timestamps,
    accelerometer_rolls,
    label="Accelerometer"
)

plt.plot(
    timestamps,
    gyro_rolls,
    label="Gyroscope"
)

plt.plot(
    timestamps,
    filtered_rolls,
    label="Complementary Filter"
)

plt.xlabel("Time (s)")
plt.ylabel("Roll (degrees)")
plt.title("Effect of Linear Acceleration")
plt.legend()

plt.tight_layout()
plt.show()